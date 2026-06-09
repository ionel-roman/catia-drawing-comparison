import win32com.client
import pandas as pd
from extractors.dimension_extractor import DimensionExtractor


def main():
    try:
        catia = win32com.client.GetActiveObject("CATIA.Application")
    except Exception:
        print("CATIA is not running.")
        return

    doc = catia.ActiveDocument

    try:
        sheet = doc.Sheets.ActiveSheet
    except Exception:
        print("No active sheet found.")
        return

    print(f"Active sheet: {sheet.Name}")
    print(f"Number of views: {sheet.Views.Count}\n")

    extractor = DimensionExtractor()

    # ✅ This will become your Excel table
    data = []

    # ✅ LOOP THROUGH ALL VIEWS
    for i in range(1, sheet.Views.Count + 1):
        view = sheet.Views.Item(i)

        print(f"Processing view {i}: {view.Name}")

        dims = extractor.extract(view)

        print(f"  → Found {len(dims)} dimensions")

        for d in dims:
            # ✅ flatten tolerance for Excel
            upper_tol = None
            lower_tol = None

            if isinstance(d.tolerance, dict):
                upper_tol = d.tolerance.get("upper")
                lower_tol = d.tolerance.get("lower")

            data.append({
                "View": view.Name,
                "Dimension Name": d.name,
                "Value": d.value,
                "Upper Tolerance": upper_tol,
                "Lower Tolerance": lower_tol
            })

    if not data:
        print("\nNo dimensions found in any view.")
        return

    # ✅ Create DataFrame
    df = pd.DataFrame(data)

    # ✅ Export to Excel
    output_file = "catia_dimensions.xlsx"
    df.to_excel(output_file, index=False, engine="openpyxl")

    print("\n============================")
    print(f"Excel file created: {output_file}")
    print("============================")


if __name__ == "__main__":
    main()