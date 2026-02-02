import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "AutoAnalyst Pro"
    VERSION: str = "2.0.0"

    # Base Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    UPLOAD_DIR = DATA_DIR / "uploads"

    # Create dirs if they don't exist
    def ensure_dirs(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
