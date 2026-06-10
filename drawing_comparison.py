import os
import tkinter as tk
from tkinter import filedialog, messagebox
import win32com.client
import pandas as pd


# -----------------------------
# EXTRACT VALUES + TOLERANCES
# -----------------------------
def extract_dimension_parameters(doc):
    params = doc.Parameters
    dimensions = []

    for i in range(1, params.Count + 1):
        try:
            p = params.Item(i)
            full_name = p.Name
        except:
            continue

        if "Dimension." not in full_name:
            continue

        parts = full_name.split("\\")

        sheet = parts[1] if len(parts) > 1 else "Unknown"
        view = parts[2] if len(parts) > 2 else "Unknown"

        dim_id = None
        param_type = None

        for part in parts:
            if part.startswith("Dimension."):
                dim_id = part
            elif "Measured length" in part:
                param_type = "length"
            elif "Measured angle" in part:
                param_type = "angle"

        if param_type not in ["length", "angle"]:
            continue

        try:
            value = round(float(p.Value), 3)
        except:
            continue

        dimensions.append({
            "sheet": sheet,
            "view": view,
            "dimension": dim_id,
            "value": value,
            "type": param_type,
            "upper_tol": None,
            "lower_tol": None
        })

    df = pd.DataFrame(dimensions)

    # --- TOLERANCES ---
    tol_map = {}
    sheets = doc.Sheets

    for s in range(1, sheets.Count + 1):
        sheet = sheets.Item(s)

        for v in range(1, sheet.Views.Count + 1):
            view = sheet.Views.Item(v)

            dims = view.Dimensions

            for i in range(1, dims.Count + 1):
                try:
                    d = dims.Item(i)
                    name = d.Name

                    tol = d.GetTolerances()
                    upper = tol[4]
                    lower = tol[5]

                    tol_map[name] = (upper, lower)
                except:
                    continue

    for idx, row in df.iterrows():
        name = row["dimension"]
        if name in tol_map:
            df.at[idx, "upper_tol"] = tol_map[name][0]
            df.at[idx, "lower_tol"] = tol_map[name][1]

    return df


# -----------------------------
# COMPARE
# -----------------------------
def compare_by_value_search(df1, df2, tolerance=0.01):
    result = []

    grouped1 = df1.groupby(["sheet", "view"])
    grouped2 = df2.groupby(["sheet", "view"])

    all_keys = set(grouped1.groups.keys()).union(grouped2.groups.keys())

    for key in all_keys:
        g1 = grouped1.get_group(key) if key in grouped1.groups else pd.DataFrame(columns=df1.columns)
        g2 = grouped2.get_group(key) if key in grouped2.groups else pd.DataFrame(columns=df2.columns)

        used_in_d2 = set()

        for i, row1 in g1.iterrows():
            found_match = False
            match_index = None

            for j, row2 in g2.iterrows():
                if j in used_in_d2:
                    continue

                if abs(row1["value"] - row2["value"]) <= tolerance:
                    found_match = True
                    match_index = j
                    break

            if found_match:
                used_in_d2.add(match_index)

                result.append({
                    "sheet": key[0],
                    "view": key[1],

                    "dimension_Reference_DRW": row1["dimension"],
                    "value_Reference_DRW": row1["value"],
                    "upper_tol_Reference_DRW": row1["upper_tol"],
                    "lower_tol_Reference_DRW": row1["lower_tol"],

                    "dimension_Compared_Drawing": g2.loc[match_index, "dimension"],
                    "value_Compared_Drawing": g2.loc[match_index, "value"],
                    "upper_tol_Compared_Drawing": g2.loc[match_index, "upper_tol"],
                    "lower_tol_Compared_Drawing": g2.loc[match_index, "lower_tol"],

                    "difference": round(abs(row1["value"] - g2.loc[match_index, "value"]), 4),
                    "status": "OK"
                })
            else:
                result.append({
                    "sheet": key[0],
                    "view": key[1],
                    "dimension_Referece_Drawing": row1["dimension"],
                    "value_Referece_Drawing": row1["value"],
                    "upper_tol_Referece_Drawing": row1["upper_tol"],
                    "lower_tol_Referece_Drawing": row1["lower_tol"],
                    "dimension_Compared_Drawing": None,
                    "value_Compared_Drawing": None,
                    "upper_tol_Compared_Drawing": None,
                    "lower_tol_Compared_Drawing": None,
                    "difference": None,
                    "status": "NOT FOUND in Compared_Drawing"
                })

        for j, row2 in g2.iterrows():
            if j not in used_in_d2:
                result.append({
                    "sheet": key[0],
                    "view": key[1],
                    "dimension_Referece_Drawing": None,
                    "value_Referece_Drawing": None,
                    "upper_tol_Referece_Drawing": None,
                    "lower_tol_Referece_Drawing": None,
                    "dimension_Compared_Drawing": row2["dimension"],
                    "value_Compared_Drawing": row2["value"],
                    "upper_tol_Compared_Drawing": row2["upper_tol"],
                    "lower_tol_Compared_Drawing": row2["lower_tol"],
                    "difference": None,
                    "status": "EXTRA in Compared_Drawing"
                })

    return pd.DataFrame(result)


# -----------------------------
# GUI
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CATIA Drawing Comparator")

        self.folder_path = tk.StringVar()
        self.selected_ref = tk.StringVar()
        self.selected_cmp = tk.StringVar()

        # Folder selection
        tk.Button(root, text="Select Folder", command=self.select_folder).pack(pady=5)
        tk.Label(root, textvariable=self.folder_path).pack()

        # Listbox
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60)
        self.listbox.pack(pady=10)

        # Dropdowns
        tk.Label(root, text="Reference Drawing:").pack()
        self.ref_menu = tk.OptionMenu(root, self.selected_ref, "")
        self.ref_menu.pack()

        tk.Label(root, text="To Be Compared:").pack()
        self.cmp_menu = tk.OptionMenu(root, self.selected_cmp, "")
        self.cmp_menu.pack()

        # Run button
        tk.Button(root, text="Run Comparison", command=self.run).pack(pady=15)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.folder_path.set(folder)

        files = [f for f in os.listdir(folder) if f.lower().endswith(".catdrawing")]

        if not files:
            messagebox.showerror("Error", "No CATDrawing files found")
            return

        # Update dropdowns
        self.update_menu(self.ref_menu, self.selected_ref, files)
        self.update_menu(self.cmp_menu, self.selected_cmp, files)

    def update_menu(self, menu, variable, options):
        menu["menu"].delete(0, "end")
        for opt in options:
            menu["menu"].add_command(label=opt, command=lambda v=opt: variable.set(v))

        if options:
            variable.set(options[0])

    def run(self):
        folder = self.folder_path.get()
        ref = self.selected_ref.get()
        cmp = self.selected_cmp.get()

        if not folder or not ref or not cmp:
            messagebox.showerror("Error", "Selection incomplete")
            return

        path1 = os.path.join(folder, ref)
        path2 = os.path.join(folder, cmp)

        try:
            catia = win32com.client.Dispatch("CATIA.Application")
            docs = catia.Documents

            doc1 = docs.Open(path1)
            doc2 = docs.Open(path2)

            df1 = extract_dimension_parameters(doc1)
            df2 = extract_dimension_parameters(doc2)

            df_result = compare_by_value_search(df1, df2)

            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

            if save_path:
                df_result.to_excel(save_path, index=False)
                messagebox.showinfo("Done", f"Saved to:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()