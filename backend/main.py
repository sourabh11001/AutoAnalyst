from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.engines.data_engine import data_engine
from backend.app.engines.eda_engine import eda_engine
from backend.app.engines.ai_engine import ai_engine
from backend.app.engines.report_engine import report_engine
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    dataset_id: str
    query: str = None

@app.get("/")
def read_root():
    return {"status": "AutoAnalyst Server Online"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        return await data_engine.save_upload(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyze/{dataset_id}")
def analyze(dataset_id: str):
    try:
        return eda_engine.generate_summary(dataset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/autoscan/{dataset_id}")
def autoscan(dataset_id: str):
    try:
        insight = ai_engine.generate_autoscan(dataset_id)
        return {"response": insight}
    except Exception as e:
        return {"response": "Autoscan skipped."}

@app.post("/api/chat")
def chat_with_data(request: ChatRequest):
    try:
        response = ai_engine.generate_insight(request.dataset_id, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{dataset_id}")
def download_report(dataset_id: str):
    try:
        report_path = report_engine.generate_report(dataset_id)
        if report_path and os.path.exists(report_path):
            return FileResponse(report_path, media_type='application/pdf', filename="AutoAnalyst_Report.pdf")
        else:
            raise HTTPException(status_code=500, detail="Report generation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
