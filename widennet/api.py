from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from predict import predict_contract

app = FastAPI(title="WIDENNET Vulnerability API")

class ContractInput(BaseModel):
    source_code: str
    solc_version: str = "0.8.0"

@app.post("/predict")
def analyze(payload: ContractInput):
    try:
        result = predict_contract(payload.source_code, payload.solc_version)
        return {"status": "ok", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/file")
async def analyze_file(file: UploadFile = File(...)):
    source = (await file.read()).decode("utf-8")
    try:
        result = predict_contract(source)
        return {"filename": file.filename, "status": "ok", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "alive"}