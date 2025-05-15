from fastapi import FastAPI
from backend.routes import scan

app = FastAPI(
    title="OSINT Harvester API",
    version="1.0.0",
    description="FastAPI backend for OSINT gathering"
)

app.include_router(scan.router)
