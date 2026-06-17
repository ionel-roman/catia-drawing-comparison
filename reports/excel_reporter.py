import pandas as pd
from core.comparator import ComparisonResult

class ExcelReporter:

    def generate(self, results: list[ComparisonResult], output_path: str):
        rows = [self._to_row(r) for r in results]
        df = pd.DataFrame(rows)
        df.to_excel(output_path, index=False)

    def _to_row(self, r: ComparisonResult) -> dict:
        return {
            "Sheet": r.sheet,
            "View": r.view,
            "Reference Dimension": r.ref_dimension.name if r.ref_dimension else None,
            "Reference Value": r.ref_dimension.value if r.ref_dimension else None,
            "Reference Upper Tol": r.ref_dimension.upper_tol if r.ref_dimension else None,
            "Reference Lower Tol": r.ref_dimension.lower_tol if r.ref_dimension else None,
            "Compared Dimension": r.cmp_dimension.name if r.cmp_dimension else None,
            "Compared Value": r.cmp_dimension.value if r.cmp_dimension else None,
            "Compared Upper Tol": r.cmp_dimension.upper_tol if r.cmp_dimension else None,
            "Compared Lower Tol": r.cmp_dimension.lower_tol if r.cmp_dimension else None,
            "Difference": r.difference,
            "Status": r.status,
    }