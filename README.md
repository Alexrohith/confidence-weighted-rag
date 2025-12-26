# Confidence-Weighted Multi-Agent Retrieval-Augmented Generation (CW-MARAG)

## Abstract

Retrieval-Augmented Generation (RAG) systems often suffer from hallucinations when retrieved evidence is incomplete, noisy, or contradictory. This repository presents **CW-MARAG**, a confidence-weighted multi-agent RAG architecture that explicitly models evidence reliability and contradiction before generation. The system employs multiple specialized retrieval agents whose outputs are evaluated, scored, and arbitrated using confidence-based fusion, enabling grounded responses and principled abstention when reliable answers cannot be determined.

---

## 1. Motivation

Conventional RAG pipelines typically aggregate retrieved documents using similarity scores alone. Such approaches fail to account for:

- Conflicting evidence across documents  
- Uneven reliability of retrieval signals  
- Overconfident generation from weak context  

CW-MARAG addresses these limitations by introducing **confidence-aware arbitration** between independent retrieval agents.

---

## 2. System Overview

The system is organized into three primary stages:

1. Multi-Agent Retrieval  
2. Confidence Scoring and Arbitration  
3. Controlled Generation  

Each stage is designed to reduce hallucination risk while preserving answer usefulness.

---

## 3. Multi-Agent Retrieval

CW-MARAG uses multiple independent retrieval agents, each optimized for a distinct perspective:

### Semantic Retriever
Captures semantic similarity using dense embeddings.

### Keyword Retriever
Identifies lexical overlap and exact term matches.

### Temporal Retriever
Incorporates time-aware relevance where applicable.

### Contradiction Retriever
Detects statements that conflict with dominant evidence.

The independence of these agents increases recall while enabling disagreement analysis.

---

## 4. Confidence Scoring and Arbitration

Each retrieved evidence chunk is evaluated along multiple dimensions, including:

- Retrieval strength  
- Cross-agent agreement  
- Presence of contradiction signals  

Evidence is classified as:

- Trusted  
- Contradictory  
- Low-confidence  

A fusion module arbitrates which evidence is safe to forward to the generation stage.

---

## 5. Controlled Generation

The generation module is explicitly constrained to:

- Use only trusted evidence  
- Abstain when evidence is insufficient or contradictory  

This design prioritizes **faithfulness over fluency**, preventing confident but unsupported outputs.

---

## 6. Implementation Details

- **Language:** Python 3.9+  
- **Retrieval:** FAISS-based indexing and custom retrievers  
- **Embeddings:** Sentence-level semantic embeddings  
- **LLM Backend:** Local LLM via Ollama  
- **Interface:** Streamlit-based user interface  

The system is modular and extensible, supporting experimentation with alternative retrieval or arbitration strategies.

---

## 7. Repository Structure

```text
confidence-weighted-rag/
├── app/
│   ├── api/                # Query and upload interfaces
│   ├── retrievers/         # Independent retrieval agents
│   ├── arbitration/        # Confidence scoring and fusion
│   ├── llm/                # Generation logic
│   └── main.py             # Application entry point
├── data/
│   ├── index/              # Vector indices
│   └── uploads/            # Uploaded documents
├── streamlit_app.py
├── test_*.py
└── README.md
