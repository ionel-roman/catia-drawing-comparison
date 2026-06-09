from models.sheet import Sheet
from extractors.view_extractor import ViewExtractor

class SheetExtractor:

    def __init__(self) -> None:
        self.view_extractor = ViewExtractor()
    
    def extract(self, catia_sheet) -> Sheet:

        sheet = Sheet(
        name=self._get_name(catia_sheet),
        paper_size=self._get_paper_size(catia_sheet),
        scale=self._get_scale(catia_sheet),
        orientation=self._get_orientation(catia_sheet) # type: ignore
        )
        try:
            views=catia_sheet.Views
            for i in range(1, views.Count + 1):
                catia_view = views.Item(i)
                view = self.view_extractor.extract(catia_view)
                sheet.add_view(view)

        except Exception as e:
            print(f"[SheetExtractor] failed to extract views for {sheet.name}: {e}")

        return sheet
    
    def _get_name(self, catia_sheet):
        try:
            return catia_sheet.Name
        except Exception:
            return "UNKNOWN_SHEET"
    
    def _get_scale(self, catia_sheet):
        try:
            return float(catia_sheet.Scale)
        except Exception:
            return None
    def _get_paper_size(self, catia_sheet):
        try:
            return catia_sheet.PaprSize
        except Exception:
            return None
    def _get_orientation(self, catia_sheet):
        try:
            return catia_sheet.Orientation
        except Exception:
            return None