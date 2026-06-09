from models.drawing import Drawing

from extractors.parameter_extractor import ParameterExtractor
from extractors.sheet_extractor import SheetExtractor


class DrawingExtractor:

    def __init__(self):
        self.parameter_extractor = ParameterExtractor()
        self.sheet_extractor = SheetExtractor()

    def extract(self, catia_document) -> Drawing:

        drawing = Drawing(
        name=catia_document.Name,
        file_path=getattr(catia_document, "FullName", None) # type: ignore
        )

        # 1. PARAMETERS
        drawing.parameters = self.parameter_extractor.extract(catia_document)

        # 2. SHEETS + VIEWS (recursive via SheetExtractor)
        sheets = catia_document.Sheets

        for i in range(1, sheets.Count + 1):

            catia_sheet = sheets.Item(i)

            sheet = self.sheet_extractor.extract(catia_sheet)

            drawing.add_sheet(sheet)

        # 3. METADATA mapping (lightweight, optional now)
        drawing.metadata = self._build_metadata(drawing.parameters)

        return drawing

    def _build_metadata(self, parameters: dict):

        from models.metadata import Metadata

        metadata = Metadata()

        for param in parameters.values():

            name = param.name.lower()

            if "d_docnr" in name:
                metadata.part_number = param.value

            elif "ptc_wm_revision" in name:
                metadata.revision = param.value

            elif "d_matnr" in name:
                metadata.material = param.value

            elif "d_weight_calc" in name and "d_weight_calc_tol" not in name:
                metadata.mass = param.value

        return metadata