import win32com.client
from extractors.view_extractor import ViewExtractor

catia = win32com.client.GetActiveObject("CATIA.Application")
doc = catia.ActiveDocument
sheet = doc.Sheets.ActiveSheet

views = sheet.Views

extractor = ViewExtractor()

for i in range(1, views.Count + 1):
    catia_view = views.Item(i)

    view = extractor.extract(catia_view)

    print(
        view.name,
        view.view_type,
        view.scale)