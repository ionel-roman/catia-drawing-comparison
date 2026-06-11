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
                    "view": key[1],

                    "value_DRW_1": round(row1["value"], 2),
                    "upper_tol_DRW_1": round(row1["upper_tol"], 2),
                    "lower_tol_DRW_1": round(row1["lower_tol"], 2),

                    "value_DRW_2": round(g2.loc[match_row, "value"], 2),
                    "upper_tol_DRW_2": round(g2.loc[match_row, "upper_tol"], 2),
                    "lower_tol_DRW_2": round(g2.loc[match_row, "lower_tol"], 2),

                    "status": "OK"
                })

            else:
                result.append({
                    "view": key[1],

                    "value_DRW_1": round(row1["value"], 2),
                    "upper_tol_DRW_1": round(row1["upper_tol"], 2),
                    "lower_tol_DRW_1": round(row1["lower_tol"], 2),

                    "value_DRW_2": None,
                    "upper_tol_DRW_2": None,
                    "lower_tol_DRW_2": None,

                    "status": "NOT FOUND in DRW_2"
                })

        for j, row2 in g2.iterrows():
            if j not in used:
                result.append({
                    "view": key[1],

                    "value_DRW_1": None,
                    "upper_tol_DRW_1": None,
                    "lower_tol_DRW_1": None,

                    "value_DRW_2": round(row2["value"], 2),
                    "upper_tol_DRW_2": round(row2["upper_tol"], 2),
                    "lower_tol_DRW_2": round(row2["lower_tol"], 2),

                    "status": "EXTRA in Compared_Drawing"
                })

    return pd.DataFrame(result)