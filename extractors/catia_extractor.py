from model.dimension import Dimension

class CatiaExtractor:


    def __init__(self, doc):
        self.doc = doc

    def extract(self) -> list[Dimension]:
        dimensions = self._extract_values()
        tol_map = self._extract_tolerances()
        for dim in dimensions:
            if dim.name in tol_map:
                dim.upper_tol, dim.lower_tol = tol_map[dim.name]
        return dimensions

    def _extract_values(self) -> list[Dimension]:
        dimensions = []
        params = self.doc.Parameters
        for i in range(1, params.Count + 1):
            try:
                p = params.Item(i)
                full_name = p.Name
            except Exception:
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
            if param_type not in ("length", "angle"):
                continue
            try:
                value = round(float(p.Value), 3)
            except Exception:
                continue
            dimensions.append(Dimension(
                sheet=sheet, view=view, name=dim_id,
                value=value, dim_type=param_type
                ))
        return dimensions

    def _extract_tolerances(self) -> dict:
        tol_map = {}
        sheets = self.doc.Sheets
        for s in range(1, sheets.Count + 1):
            sheet = sheets.Item(s)
            for v in range(1, sheet.Views.Count + 1):
                view = sheet.Views.Item(v)
                for i in range(1, view.Dimensions.Count + 1):
                    try:
                        d = view.Dimensions.Item(i)
                        tol = d.GetTolerances()
                        tol_map[d.Name] = (tol[4], tol[5])
                    except Exception:
                        continue
        return tol_map