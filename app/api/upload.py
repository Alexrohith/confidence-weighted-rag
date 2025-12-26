from fastapi import APIRouter, UploadFile, File
from app.retrievers.semantic import SemanticRetriever
from app.retrievers.keyword import KeywordRetriever
import fitz  # PyMuPDF

router = APIRouter(prefix="/upload", tags=["Upload"])

semantic = SemanticRetriever()
keyword = KeywordRetriever()


def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    texts = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            texts.append(text)
    return texts


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    chunks = extract_text_from_pdf(contents)

    semantic.build_index(chunks)
    keyword.build_index(chunks)

    return {
        "status": "success",
        "message": "PDF indexed successfully",
        "chunks_indexed": len(chunks)
    }
