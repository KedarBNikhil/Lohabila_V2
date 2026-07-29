from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import backup_sources

app = FastAPI(
    title="Lohabila API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(backup_sources.router)


@app.get("/")
def root():
    return {
        "application": "Lohabila API",
        "status": "Running"
    }