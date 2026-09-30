from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router


app = FastAPI(
    title="J.A.R.V.I.S.",
    description="Just A Rather Very Intelligent System",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "name": "J.A.R.V.I.S.",
        "status": "online",
        "version": "0.1.0",
        "message": "Good morning. Systems are online."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }