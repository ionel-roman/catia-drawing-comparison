import pandas as pd


def compare_by_value_search(df1, df2, tolerance=0.01):
    result = []

    grouped1 = df1.groupby(["sheet", "view"])
    grouped2 = df2.groupby(["sheet", "view"])

    keys = set(grouped1.groups.keys()).union(grouped2.groups.keys())

    for key in keys:
        g1 = grouped1.get_group(key) if key in grouped1.groups else pd.DataFrame(columns=df1.columns)
        g2 = grouped2.get_group(key) if key in grouped2.groups else pd.DataFrame(columns=df2.columns)

        used = set()

        for _, row1 in g1.iterrows():
            found = False
            match_row = None

            for j, row2 in g2.iterrows():
                if j in used:
                    continue

                if abs(row1["value"] - row2["value"]) <= tolerance:
                    found = True
                    match_row = j
                    break

            if found:
                used.add(match_row)

                result.append({
                    "sheet": key[0],
                    "view": key[1],

                    "dimension_Reference_DRW": row1["dimension"],
                    "value_Reference_DRW": row1["value"],
                    "upper_tol_Reference_DRW": row1["upper_tol"],
                    "lower_tol_Reference_DRW": row1["lower_tol"],

                    "dimension_Compared_Drawing": g2.loc[match_row, "dimension"],
                    "value_Compared_Drawing": g2.loc[match_row, "value"],
                    "upper_tol_Compared_Drawing": g2.loc[match_row, "upper_tol"],
                    "lower_tol_Compared_Drawing": g2.loc[match_row, "lower_tol"],

                    "difference": round(abs(row1["value"] - g2.loc[match_row, "value"]), 4),
                    "status": "OK"
                })

            else:
                result.append({
                    "sheet": key[0],
                    "view": key[1],

                    "dimension_Reference_DRW": row1["dimension"],
                    "value_Reference_DRW": row1["value"],
                    "upper_tol_Reference_DRW": row1["upper_tol"],
                    "lower_tol_Reference_DRW": row1["lower_tol"],

                    "dimension_Compared_Drawing": None,
                    "value_Compared_Drawing": None,
                    "upper_tol_Compared_Drawing": None,
                    "lower_tol_Compared_Drawing": None,

                    "difference": None,
                    "status": "NOT FOUND in Compared_Drawing"
                })

        for j, row2 in g2.iterrows():
            if j not in used:
                result.append({
                    "sheet": key[0],
                    "view": key[1],

                    "dimension_Reference_DRW": None,
                    "value_Reference_DRW": None,
                    "upper_tol_Reference_DRW": None,
                    "lower_tol_Reference_DRW": None,

                    "dimension_Compared_Drawing": row2["dimension"],
                    "value_Compared_Drawing": row2["value"],
                    "upper_tol_Compared_Drawing": row2["upper_tol"],
                    "lower_tol_Compared_Drawing": row2["lower_tol"],

                    "difference": None,
                    "status": "EXTRA in Compared_Drawing"
                })

    return pd.DataFrame(result)