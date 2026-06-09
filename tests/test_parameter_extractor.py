from catia.connection import get_catia_app
from extractors.parameter_extractor import ParameterExtractor

if __name__ == "__main__":
    catia = get_catia_app()

    doc = catia.ActiveDocument

    extractor = ParameterExtractor()
    params = extractor.extract(doc)

    print ("\n=== PARAMETERS FOUND===")

    for name, param in params.items():
        print(f"{name} = {param.value}")

    print("\nTotal parameters: ", len(params))