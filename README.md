# confidence-weighted-rag
Confidence-Weighted Multi-Agent Retrieval-Augmented Generation (CW-MARAG) — a contradiction-aware RAG system that uses multiple retrieval agents with confidence-based arbitration to generate grounded, non-hallucinated answers from PDFs.
# CW-MARAG

**Confidence-Weighted Multi-Agent Retrieval-Augmented Generation**

CW-MARAG is a novel RAG architecture that uses multiple retrieval agents
(semantic, keyword, and contradiction detection) with confidence-based
arbitration to generate grounded, non-hallucinated answers from PDFs.

## Features
- Multi-agent retrieval
- Confidence-weighted evidence arbitration
- Contradiction-aware reasoning
- Yes/No polarity control
- PDF-based question answering
- Hallucination prevention

## Tech Stack
- FastAPI
- FAISS
- Sentence-BERT
- PyMuPDF
- Ollama (LLM)
- Streamlit (frontend)

## Use Cases
- Research document QA
- Educational assistants
- Explainable RAG systems

## Status
Working prototype – paper & patent ready.
