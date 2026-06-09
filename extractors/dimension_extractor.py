from models.dimension import Dimension


class DimensionExtractor:

    def extract(self, catia_view):

        dimensions = []

        try:
            dims = catia_view.Dimensions
        except Exception:
            print("No dimensions found.")
            return dimensions

        for i in range(1, dims.Count + 1):
            try:
                dim = dims.Item(i)

                name = getattr(dim, "Name", None)

                # ✅ ✅ MAIN FIX: extract from PARAMETERS
                value = self._get_measured_length(dim)

                # ✅ tolerance (optional)
                tolerance = self._extract_tolerance(dim)

                dimensions.append(
                    Dimension(
                        name=name,
                        value=value,
                        tolerance=tolerance
                    )
                )

            except Exception as e:
                print(f"Skipping dim {i}: {e}")
                continue

        return dimensions


    # ======================================================
    # ✅ CORE: GET "Measured length"
    # ======================================================
    def _get_measured_length(self, dim):

        try:
            params = dim.Parameters

            for i in range(1, params.Count + 1):
                p = params.Item(i)

                pname = p.Name.lower()

                # ✅ this matches your case exactly
                if "measured length" in pname:
                    return p.Value  # ✅ numeric value

        except Exception:
            pass

        return None


    # ======================================================
    # ✅ OPTIONAL: tolerance
    # ======================================================
    def _extract_tolerance(self, dim):

        try:
            tol = dim.Tolerance

            if not tol:
                return None

            return {
                "upper": getattr(tol, "UpperValue", None),
                "lower": getattr(tol, "LowerValue", None)
            }

        except Exception:
            return None