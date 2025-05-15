from fastapi import APIRouter, HTTPException
from backend.models.scan_request import ScanRequest
from backend.services.scanner import run_scan

router = APIRouter(prefix="/api", tags=["scan"])

@router.post("/scan")
async def start_scan(payload: ScanRequest):
    try:
        return run_scan(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
