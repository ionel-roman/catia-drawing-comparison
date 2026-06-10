import win32com.client

def get_catia():
    try:
        return win32com.client.Dispatch("CATIA.Application")
    except Exception as e:
        raise Exception("Cannot connect to CATIA. Make sure CATIA is running.") from e


def open_document(catia, path):
    try:
        return catia.Documents.Open(path)
    except Exception as e:
        raise Exception(f"Failed to open document:\n{path}") from e