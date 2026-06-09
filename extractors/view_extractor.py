from models.view import View


class ViewExtractor:

    def extract(self, catia_view) -> View:

        view = View(
        name=self._get_name(catia_view),
        view_type=self._get_view_type(catia_view),
        scale=self._get_scale(catia_view)
        )

        return view

    def _get_name(self, catia_view) -> str:

        try:
            return catia_view.Name
        except Exception:
            return "UNKNOWN"

    def _get_scale(self, catia_view) -> float | None:

        try:
            return float(catia_view.Scale)
        except Exception:
            return None

    def _get_view_type(self, catia_view) -> str:

        name = self._get_name(catia_view).lower()

        if "front" in name:
            return "Front"

        if "top" in name:
            return "Top"

        if "bottom" in name:
            return "Bottom"

        if "left" in name:
            return "Left"

        if "right" in name:
            return "Right"

        if "section" in name:
            return "Section"

        if "detail" in name:
            return "Detail"

        if "background" in name:
            return "Background"

        return "Unknown"