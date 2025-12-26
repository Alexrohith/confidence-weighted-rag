from fastapi import FastAPI

from app.api.query import router as query_router
from app.api.upload import router as upload_router


app = FastAPI(
    title="CW-MARAG",
    description="Confidence-Weighted Multi-Agent RAG",
    version="0.1",
)

# Register API routes
app.include_router(upload_router)
app.include_router(query_router)


@app.get("/")
def root():
    return {"status": "CW-MARAG running"}
