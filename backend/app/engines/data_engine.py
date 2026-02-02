import pandas as pd
import os
import uuid

# Ensure the uploads folder exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DataEngine:
    def __init__(self):
        pass

    async def save_upload(self, file):
        # Create a unique name so files don't overwrite each other
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
        
        # Save the bytes to disk
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
            
        return {"dataset_id": file_id, "filename": file.filename}

    def load_data(self, dataset_id: str):
        # Locate and load the file
        file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}.csv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset {dataset_id} not found at {file_path}")
        return pd.read_csv(file_path)

data_engine = DataEngine()
