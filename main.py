from fastapi import FastAPI

from app.routes import router as voluntarios_router

app = FastAPI(title="API de Voluntários - Desafio")

app.include_router(voluntarios_router, prefix="/voluntarios", tags=["voluntarios"])


@app.get("/")
async def health():
    return {"ok": True, "service": "api-certify"}
