# =========================
# LIST PARAMETERS FROM DOC
# =========================
def list_drawing_parameters(doc):
    params = doc.Parameters
    param_list = []

    for i in range(1, params.Count + 1):
        p = params.Item(i)
        param_list.append(p)

    return param_list


# =========================
# PARAMETER NAME MAPPING
# =========================
checker = {
    "partnumber": ["partnumber", "pn", "D_DOCNR"],
    "materialnumber": ["D_MATNR"],
    "weight": ["D_WEIGHT_CALC"],
    "general_tolerances": ["D_TOLERANCE_GENERAL"],
    "tolerance_principle": ["D_TOLERANCE_PRINCIPLE"],
    "material": ["D_MATERIAL"],
    "surface": ["D_SURFACE_TEXT"]
}


# =========================
# FIND PARAMETER VALUE
# =========================
def find_params(param_list, possible_names):
    for p in param_list:
        name = p.Name.lower()

        for variant in possible_names:
            if variant.lower() in name:
                try:
                    return p.Value
                except:
                    return None

    return None


# =========================
# EXTRACT TITLEBLOCK DATA
# =========================
def extract_titleblock_data(param_list):
    data = {
        "part_number": find_params(param_list, checker["partnumber"]),
        "material_number": find_params(param_list, checker["materialnumber"]),
        "material": find_params(param_list, checker["material"]),
        "weight": find_params(param_list, checker["weight"]),
        "surface": find_params(param_list, checker["surface"]),
        "general_tolerance": find_params(param_list, checker["general_tolerances"]),
        "tolerance_principle": find_params(param_list, checker["tolerance_principle"])
    }

    return data