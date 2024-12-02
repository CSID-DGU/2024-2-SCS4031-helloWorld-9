import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "vectorDB"
UPLOAD_PATH = BASE_DIR / "uploads"

if __name__ == "__main__":
    print("Configuration Settings:")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"DB_PATH: {DB_PATH}")
    print(f"DB_PATH: {UPLOAD_PATH}")
