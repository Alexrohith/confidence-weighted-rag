from fastapi import APIRouter
from pydantic import BaseModel
import re

from app.retrievers.semantic import SemanticRetriever
from app.retrievers.keyword import KeywordRetriever
from app.retrievers.contradiction import ContradictionRetriever
from app.arbitration.confidence import ConfidenceArbitrator
from app.llm.generator import LLMGenerator

router = APIRouter(prefix="/query", tags=["CW-MARAG"])


class QueryRequest(BaseModel):
    question: str


# ✅ Initialize agents ONCE
# SemanticRetriever auto-loads FAISS + docs from disk
semantic_retriever = SemanticRetriever()
keyword_retriever = KeywordRetriever()
contradiction_retriever = ContradictionRetriever()
arbitrator = ConfidenceArbitrator()
llm = LLMGenerator()


# -------------------------------
# 🧠 Utility: extract main entity
# -------------------------------
def extract_entity(question: str) -> str:
    """
    Works for:
    - What is SBERT?
    - What is FAISS used for?
    - Define Retrieval Augmented Generation
    """
    q = question.lower()

    patterns = [
        r"what is ([a-z0-9\- ]+)",
        r"define ([a-z0-9\- ]+)",
        r"explain ([a-z0-9\- ]+)"
    ]

    for p in patterns:
        match = re.search(p, q)
        if match:
            return match.group(1).strip()

    # fallback: longest capital-like token
    tokens = re.findall(r"[a-zA-Z]{3,}", question)
    return tokens[0].lower() if tokens else ""


@router.post("/")
def query_cw_marag(req: QueryRequest):
    query = req.question

    # 1️⃣ Retrieve
    semantic_results = semantic_retriever.retrieve(query)
    keyword_results = keyword_retriever.retrieve(query)

    # Merge results
    combined = semantic_results + keyword_results

    # 2️⃣ ENTITY-CONSTRAINED FILTER (SAFE)
    entity = extract_entity(query)

    if entity:
        filtered_results = [
            r for r in combined
            if entity in r["text"].lower()
        ]
    else:
        filtered_results = combined

    # Remove duplicate texts
    candidate_texts = list({r["text"] for r in filtered_results})

    # 3️⃣ Contradiction retrieval (ONLY on candidates)
    contradiction_results = contradiction_retriever.retrieve(
        query=query,
        documents=candidate_texts
    )

    # 4️⃣ Arbitration
    final_evidence = arbitrator.arbitrate(
        semantic_results=filtered_results,
        keyword_results=filtered_results,
        contradiction_results=contradiction_results
    )

    # 5️⃣ LLM Generation (strictly grounded)
    answer = llm.generate(
        question=query,
        evidence=final_evidence
    )

    return {
        "question": query,
        "answer": answer,
        "evidence": final_evidence
    }
