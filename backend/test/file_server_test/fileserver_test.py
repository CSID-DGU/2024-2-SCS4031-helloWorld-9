from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

app = FastAPI()

# 디렉토리 설정 (예: 파일 저장 디렉토리)
BASE_DIR = Path("files")
BASE_DIR.mkdir(exist_ok=True)  # 디렉토리가 없으면 생성

# 샘플 파일 생성
sample_file = BASE_DIR / "example.txt"
if not sample_file.exists():
    sample_file.write_text("This is a sample file for testing FastAPI.")

@app.get("/files")
async def list_files():
    """
    파일 리스트 반환
    """
    files = [file.name for file in BASE_DIR.iterdir() if file.is_file()]
    return {"files": files}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fileserver_test:app", host="127.0.0.1", port=8000, reload=True)