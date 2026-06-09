import win32com.client

def get_catia_app():
    try:
        catia = win32com.client.GetActiveObject("CATIA.Application")
        print("✅ Connected to running CATIA")
        return catia
    except Exception as e:
        raise RuntimeError(
            "❌ CATIA is not running via CAD_Workbench. Start it manually."
        ) from e

