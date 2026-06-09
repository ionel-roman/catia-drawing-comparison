import win32com.client


def extract_dimension_parameters():
    catia = win32com.client.Dispatch("CATIA.Application") #initialize CATIA
    doc = catia.ActiveDocument # doc is currently opened DRW

    if not doc.Name.lower().endswith(".catdrawing"): # check if it really is a DRW
        print("❌ Not a CATDrawing")
        return

    params = doc.Parameters # extract all parameters

    print(f"\n✅ Drawing: {doc.Name}")
    print(f"✅ Total parameters: {params.Count}\n")

    dimensions = {}

    for i in range(1, params.Count + 1):   #Filter only Dimensions from all Parameters, rest is not needed
        p = params.Item(i)

        try:
            full_name = p.Name
        except:
            continue

        # Only dimension-related parameters
        if "Dimension." not in full_name:
            continue

        parts = full_name.split("\\")  #organize dimensions by Sheet, View, Dimension name

        # Extract identifiers
        sheet_name = parts[1] if len(parts) > 1 else "Unknown"
        view_name = parts[2] if len(parts) > 2 else "Unknown"

        dim_id = None
        param_type = None

        for part in parts:
            if part.startswith("Dimension."):
                dim_id = part
            elif "Measured length" in part:
                param_type = "length"
            elif "Measured angle" in part:
                param_type = "angle"
            elif "Activity" in part:
                param_type = "activity"

        if dim_id is None:
            continue

        # Create unique key per dimension
        key = f"{sheet_name} | {view_name} | {dim_id}"

        if key not in dimensions:
            dimensions[key] = {
                "sheet": sheet_name,
                "view": view_name,
                "dimension": dim_id,
                "length": None,
                "angle": None,
                "activity": None
            }

        #  Safe value extraction + rounding
        try:
            raw_value = p.Value

            if isinstance(raw_value, (int, float)):
                value = f"{float(raw_value):.2f}"   # ✅ FORCE 2 decimals
            else:
                value = raw_value

        except:
            value = None

        # Store values
        if param_type == "length":
            dimensions[key]["length"] = value

        elif param_type == "angle":
            dimensions[key]["angle"] = value

        elif param_type == "activity":
            dimensions[key]["activity"] = value

    #  Print results
    print("📏 Extracted Dimensions:\n")
    '''
    for key, data in dimensions.items():
        print(f"Sheet : {data['sheet']}")
        print(f"View  : {data['view']}")
        print(f"Dim   : {data['dimension']}")
        if data['length']:
            print(f"  Length : {data['length']}")
        if data['angle']:
            print(f"  Angle  : {data['angle']}")
        print("-" * 40)
'''
    return dimensions

if __name__ == "__main__":
    dimensions=extract_dimension_parameters()
    
    target_key = "Sheet.1 | Section view B-B | Dimension.2"

    
    if dimensions and target_key in dimensions:
        d = dimensions[target_key]
        
        print("✅ Found dimension:")
        print(f"Sheet : {d['sheet']}")
        print(f"View  : {d['view']}")
        print(f"Length: {d['length']}")
        print(f"Angle : {d['angle']}")
    else:
        print("❌ Dimension not found")
