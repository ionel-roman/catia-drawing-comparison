from extractors.sheet_extractor import SheetExtractor
import win32com.client

catia = win32com.client.GetActiveObject("CATIA.Application")
doc = catia.ActiveDocument

extractor = SheetExtractor()

for i in range(1, doc.Sheets.Count + 1):
    catia_sheet = doc.Sheets.Item(i)

    sheet = extractor.extract(catia_sheet)

    print("\nSheet: ", sheet.name)
    print("Paper: ", sheet.paper_size)
    print("Scale: ", sheet.scale)
    print("Views: ", sheet.view_count)

    for v in sheet.views:
        print(" -", v.name, v.view_type)