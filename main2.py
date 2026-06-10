import os
import win32com.client
import pandas as pd


# -----------------------------
# EXTRACT ONLY LENGTH + ANGLE
# -----------------------------
def extract_dimension_parameters(doc):
    params = doc.Parameters
    dimensions = []

    for i in range(1, params.Count + 1):
        p = params.Item(i)

        try:
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

        # ✅ ignore Activity and everything else
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
            "type": param_type
        })

    return pd.DataFrame(dimensions)


# -----------------------------
# COMPARE BY SEARCHING VALUES
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

        # ✅ LOOP: each dimension in Drawing 1
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
                    "dimension_D1": row1["dimension"],
                    "value_D1": row1["value"],
                    "dimension_D2": g2.loc[match_index, "dimension"],
                    "value_D2": g2.loc[match_index, "value"],
                    "difference": round(abs(row1["value"] - g2.loc[match_index, "value"]), 4),
                    "status": "OK"
                })

            else:
                result.append({
                    "sheet": key[0],
                    "view": key[1],
                    "dimension_D1": row1["dimension"],
                    "value_D1": row1["value"],
                    "dimension_D2": None,
                    "value_D2": None,
                    "difference": None,
                    "status": "NOT FOUND in D2"
                })

        # ✅ Remaining values only in Drawing 2
        for j, row2 in g2.iterrows():
            if j not in used_in_d2:
                result.append({
                    "sheet": key[0],
                    "view": key[1],
                    "dimension_D1": None,
                    "value_D1": None,
                    "dimension_D2": row2["dimension"],
                    "value_D2": row2["value"],
                    "difference": None,
                    "status": "EXTRA in D2"
                })

    df = pd.DataFrame(result)

    # Sort nicely
    df = df.sort_values(by=["sheet", "view", "value_D1"])

    return df


# -----------------------------
# PICK FILES
# -----------------------------
def pick_drawings(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".catdrawing")]

    if len(files) < 2:
        print("❌ Not enough files")
        return None, None

    print("\n📂 Available Drawings:\n")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")

    try:
        i1 = int(input("\nSelect first drawing: ")) - 1
        i2 = int(input("Select second drawing: ")) - 1
    except:
        return None, None

    return os.path.join(folder_path, files[i1]), os.path.join(folder_path, files[i2])


# -----------------------------
# MAIN
# -----------------------------
def compare_drawings():
    folder = r"C:\CAx\Usr\uig56981\CatiaV5\B32\WGM_13_0_2_0-AUTO\WISE-PROD\.ws\wise-prod.automotive-wan.com443\MB EAL"   # 🔧 CHANGE HERE

    path1, path2 = pick_drawings(folder)
    if not path1 or not path2:
        return

    catia = win32com.client.Dispatch("CATIA.Application")
    docs = catia.Documents

    print("\n📂 Opening drawings...")

    doc1 = docs.Open(path1)
    doc2 = docs.Open(path2)

    print(f"\n✅ Comparing:\n- {doc1.Name}\n- {doc2.Name}")

    df1 = extract_dimension_parameters(doc1)
    df2 = extract_dimension_parameters(doc2)

    if df1.empty or df2.empty:
        print("❌ No dimensions found")
        return

    df_result = compare_by_value_search(df1, df2)

    output_path = r"E:\scripts\Catia Drawing Comparison\comparison.xlsx"
    df_result.to_excel(output_path, index=False)

    print(f"\n✅ Exported to: {output_path}")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    compare_drawings()