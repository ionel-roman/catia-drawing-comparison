from extractors.drawing_extractor import DrawingExtractor
import win32com.client


catia = win32com.client.GetActiveObject("CATIA.Application")
doc = catia.ActiveDocument

extractor = DrawingExtractor()

drawing = extractor.extract(doc)

print("\n=== DRAWING ===")
print("Name:", drawing.name)
print("File:", drawing.file_path)

print("\n=== METADATA ===")
print("Part Number:", drawing.metadata.part_number)
print("Revision:", drawing.metadata.revision)
print("Material:", drawing.metadata.material)
print("Mass:", drawing.metadata.mass)

print("\n=== STRUCTURE ===")
print("Sheets:", drawing.sheet_count)

for sheet in drawing.sheets:
    print(f"\nSheet: {sheet.name}")
    print("Views:", sheet.view_count)

for view in sheet.views:
    print(" -", view.name, view.view_type)


from reporting.excel_report_drawing_extractor import ExcelExporter

exporter = ExcelExporter()

exporter.export(
        drawing,
        r"E:\scripts\Catia Drawing Checker\reporting\drawing_extractor_report.xlsx"
)