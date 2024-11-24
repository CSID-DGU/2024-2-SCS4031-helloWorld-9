from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/files")
async def test():
    dummy_data = [
        {
            "id": "/Code",
            "size": 4096,
            "date": datetime(2023, 12, 2, 17, 25).isoformat(),  # ISO 8601 형식으로 날짜 직렬화
            "type": "folder",
        },
        {
            "id": "/Music",
            "size": 4096,
            "date": datetime(2023, 12, 1, 14, 45).isoformat(),
            "type": "folder",
        },
        {
            "id": "/Info.txt",
            "size": 1000,
            "date": datetime(2023, 11, 30, 6, 13).isoformat(),
            "type": "file",
        },
        {
            "id": "/Code/Datepicker/Year.svelte",
            "size": 1595,
            "date": datetime(2023, 12, 7, 15, 23).isoformat(),
            "type": "file",
        },
        {
            "id": "/Pictures/162822515312968813.png",
            "size": 510885,
            "date": datetime(2023, 12, 1, 14, 45).isoformat(),
            "type": "file",
        },
    ]

    return JSONResponse(content=dummy_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fileserver_test:app", host="127.0.0.1", port=8000, reload=True)