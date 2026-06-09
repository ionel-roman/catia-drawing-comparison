import os

def open_drawing(catia, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    try:
        for doc in catia.Documents:
            if doc.FullName.lower() == file_path.lower():
                print("⚠️ Drawing already open:", doc.Name)
                return doc

        doc = catia.Documents.Open(file_path)
        print("✅ Opened:", doc.Name)
        return doc

    except Exception as e:
        raise RuntimeError(f"❌ Failed to open drawing: {file_path}") from e
