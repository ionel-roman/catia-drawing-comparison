from dataclasses import dataclass
from typing import Optional
from model.dimension import Dimension

@dataclass
class ComparisonResult:
    sheet: str
    view: str
    ref_dimension: Optional[Dimension]
    cmp_dimension: Optional[Dimension]
    difference: Optional[float]
    status: str # "OK" | "MISSING" | "EXTRA"


class DrawingComparator:
    def __init__(self, tolerance: float = 0.01):
        self.tolerance = tolerance

    def compare(self,reference: list[Dimension],compared: list[Dimension]) -> list[ComparisonResult]:
        results = []
        ref_by_view = self._group_by_view(reference)
        cmp_by_view = self._group_by_view(compared)
        all_keys = set(ref_by_view) | set(cmp_by_view)

        for key in all_keys:
            ref_dims = ref_by_view.get(key, [])
            cmp_dims = cmp_by_view.get(key, [])
            results.extend(self._compare_view(key, ref_dims, cmp_dims))

        return results

    def _group_by_view(self, dims: list[Dimension]) -> dict:
        grouped = {}
        for d in dims:
            key = (d.sheet, d.view)
            grouped.setdefault(key, []).append(d)
        return grouped

    def _compare_view(self, key, ref_dims, cmp_dims) -> list[ComparisonResult]:
        results = []
        used = set()

        for ref in ref_dims:
            match = self._find_match(ref, cmp_dims, used)
            if match:
                used.add(id(match))
                results.append(ComparisonResult(
                sheet=key[0], view=key[1],
                ref_dimension=ref, cmp_dimension=match,
                difference=round(abs(ref.value - match.value), 4),
                status="OK"
                ))
            else:
                results.append(ComparisonResult(
                sheet=key[0], view=key[1],
                ref_dimension=ref, cmp_dimension=None,
                difference=None, status="MISSING"
                ))

        for cmp in cmp_dims:
            if id(cmp) not in used:
                results.append(ComparisonResult(
                sheet=key[0], view=key[1],
                ref_dimension=None, cmp_dimension=cmp,
                difference=None, status="EXTRA"
                ))

        return results

    def _find_match(self, ref, candidates, used):
        for c in candidates:
            if id(c) not in used and abs(ref.value - c.value) <= self.tolerance:
                return c
        return None