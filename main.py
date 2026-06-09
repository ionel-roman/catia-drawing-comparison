import win32com.client

def extract_views():
    try:
        catia = win32com.client.Dispatch("CATIA.Application")
        doc = catia.ActiveDocument

        # ✅ Fixed document type check
        if not doc.Name.lower().endswith(".catdrawing"):
            print("Active document is not a CATDrawing.")
            return

        sheets = doc.Sheets
        print(f"Number of sheets: {sheets.Count}")

        for i in range(1, sheets.Count + 1):
            sheet = sheets.Item(i)
            print(f"\nSheet {i}: {sheet.Name}")

            views = sheet.Views
            print(f"  Number of views: {views.Count}")

            for j in range(1, views.Count + 1):
                view = views.Item(j)
                print(f"    View {j}: {view.Name}")

                # Optional properties
                try:
                    print(f"      Scale: {view.Scale}")
                except:
                    pass

                try:
                    print(f"      Position: ({view.x}, {view.y})")
                except:
                    pass

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    extract_views()
