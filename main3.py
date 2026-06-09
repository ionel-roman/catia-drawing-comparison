import win32com.client


def extract_dimensions_grouped(doc):
    params = doc.Parameters

    data = {}

    for i in range(1, params.Count + 1):
        p = params.Item(i)

        try:
            full_name = p.Name
        except:
            continue

        # Only dimension parameters
        if "Dimension." not in full_name:
            continue

        parts = full_name.split("\\")

        # Safety check
        if len(parts) < 4:
            continue

        sheet = parts[0]
        view = parts[1]

        param_type = None

        for part in parts:
            if "Measured length" in part:
                param_type = "length"
            elif "Measured angle" in part:
                param_type = "angle"

        if param_type is None:
            continue

        # ✅ Initialize structure
        if sheet not in data:
            data[sheet] = {}

        if view not in data[sheet]:
            data[sheet][view] = {
                "length": [],
                "angle": []
            }

        # ✅ Extract + round value
        try:
            val = p.Value

            if isinstance(val, (int, float)):
                val = float(f"{val:.2f}")  # numeric AND rounded
        except:
            continue

        data[sheet][view][param_type].append(val)

    return data


# ✅ Helper to print nicely
def print_grouped(data):
    for sheet, views in data.items():
        print(f"\n📄 {sheet}")

        for view, values in views.items():
            print(f"  🔎 {view}")

            print(f"    Lengths: {values['length']}")
            print(f"    Angles : {values['angle']}")


# ✅ Main test
def main():
    catia = win32com.client.Dispatch("CATIA.Application")
    doc = catia.ActiveDocument

    if not doc.Name.lower().endswith(".catdrawing"):
        print("❌ Not a CATDrawing")
        return

    grouped_data = extract_dimensions_grouped(doc)

    print_grouped(grouped_data)


if __name__ == "__main__":
    main()
