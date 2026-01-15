from fastapi import FastAPI

from app.routers import dictionary, spending, substring

app = FastAPI(
    title="Codewars Katas API",
    description="API para resolver katas de Codewars",
    version="1.0.0",
)

app.include_router(
    dictionary.router, prefix="/api/dictionary", tags=["dictionary"]
)
app.include_router(
    substring.router, prefix="/api/substring", tags=["substring"]
)
app.include_router(spending.router, prefix="/api/spending", tags=["spending"])


@app.get("/")
def root():
    return {
        "message": "Codewars Katas API",
        "endpoints": {
            "dictionary": "/api/dictionary",
            "substring": "/api/substring",
            "spending": "/api/spending",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
