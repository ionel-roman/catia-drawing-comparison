import os
import tkinter as tk
from tkinter import filedialog, messagebox

from extractors.dimension_extractor import extract_dimension_parameters
from core.comparator import compare_by_value_search
from catia.connection import get_catia, open_document


class App:
    def __init__(self, root):
        self.root = root

        self.folder_path = tk.StringVar()
        self.selected_ref = tk.StringVar()
        self.selected_cmp = tk.StringVar()

        # UI
        tk.Button(root, text="Select Folder", command=self.select_folder).pack(pady=5)
        tk.Label(root, textvariable=self.folder_path).pack()

        tk.Label(root, text="Reference Drawing").pack()
        self.ref_menu = tk.OptionMenu(root, self.selected_ref, "")
        self.ref_menu.pack()

        tk.Label(root, text="Compared Drawing").pack()
        self.cmp_menu = tk.OptionMenu(root, self.selected_cmp, "")
        self.cmp_menu.pack()

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
            catia = get_catia()

            doc1 = open_document(catia, path1)
            doc2 = open_document(catia, path2)

            df1 = extract_dimension_parameters(doc1)
            df2 = extract_dimension_parameters(doc2)

            df_result = compare_by_value_search(df1, df2)

            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

            if save_path:
                df_result.to_excel(save_path, index=False)
                messagebox.showinfo("Done", f"Saved to:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))