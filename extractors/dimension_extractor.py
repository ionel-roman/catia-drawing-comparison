import pandas as pd


def extract_dimension_parameters(doc):
    params = doc.Parameters
    dimensions = []

    # --- STEP 1: Nominal values ---
    for i in range(1, params.Count + 1):
        try:
            p = params.Item(i)
            full_name = p.Name
        except:
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

        if param_type not in ["length", "angle"]:
            continue

        try:
            value = round(float(p.Value), 3)
        except:
            continue

        dimensions.append({
            "sheet": sheet,
            "view": view,
            "dimension": dim_id,
            "value": value,
            "type": param_type,
            "upper_tol": None,
            "lower_tol": None
        })

    df = pd.DataFrame(dimensions)

    # --- STEP 2: Tolerances ---
    tol_map = {}

    sheets = doc.Sheets

    for s in range(1, sheets.Count + 1):
        try:
            sheet = sheets.Item(s)
        except:
            continue

        views = sheet.Views

        for v in range(1, views.Count + 1):
            try:
                view = views.Item(v)
                dims = view.Dimensions
            except:
                continue

            for i in range(1, dims.Count + 1):
                try:
                    d = dims.Item(i)

                    tol = d.GetTolerances()
                    upper = tol[4]
                    lower = tol[5]

                    tol_map[d.Name] = (upper, lower)

                except:
                    continue

    # --- STEP 3: Merge ---
    for idx, row in df.iterrows():
        name = row["dimension"]

        if name in tol_map:
            df.at[idx, "upper_tol"] = tol_map[name][0]
            df.at[idx, "lower_tol"] = tol_map[name][1]

    return df