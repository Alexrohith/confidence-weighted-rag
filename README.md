Confidence-Weighted Multi-Agent RAG (CW-MARAG)

A contradiction-aware, confidence-driven Retrieval-Augmented Generation architecture for grounded question answering from documents.

📌 Overview

Confidence-Weighted Multi-Agent Retrieval-Augmented Generation (CW-MARAG) is a novel RAG architecture designed to reduce hallucinations and handle contradictory evidence in document-based question answering systems.

Unlike conventional RAG pipelines that rely on a single retriever or naive score aggregation, CW-MARAG employs multiple specialized retrieval agents whose outputs are evaluated, weighted, and arbitrated using confidence-aware fusion before generation.

The system is particularly suited for:

Academic & legal documents

Policy PDFs

Technical manuals

Any domain where contradictions and uncertainty matter

🧠 Core Idea

Not all retrieved evidence deserves equal trust.

CW-MARAG explicitly models this by:

Using multiple retrieval perspectives

Assigning confidence scores to each evidence chunk

Detecting contradictions

Allowing the generator to abstain when evidence is insufficient or conflicting

🏗️ System Architecture
🔹 Multi-Agent Retrieval Layer

Independent agents retrieve evidence using different strategies:

Semantic Retriever – dense embeddings (semantic similarity)

Keyword Retriever – lexical / term-based matching

Temporal Retriever – time-aware relevance

Contradiction Retriever – detects conflicting statements

Each agent operates independently, improving coverage and robustness.

🔹 Confidence Scoring & Arbitration

Each retrieved chunk is evaluated on:

Retrieval strength

Agreement with other agents

Contradiction signals

Chunks are labeled as:

Trusted evidence

Contradictory evidence

Low-confidence evidence

A fusion module arbitrates which evidence is safe to use.

🔹 Controlled Generation

The LLM is guided with:

Only trusted evidence

Explicit instructions to abstain when confidence is low

This prevents:

Hallucinated answers

Overconfident responses from weak evidence

🔬 Key Features

✅ Multi-agent retrieval (semantic, keyword, contradiction-aware)

✅ Confidence-weighted evidence fusion

✅ Explicit contradiction handling

✅ Abstention on insufficient evidence

✅ Local LLM support (Ollama-compatible)

✅ Streamlit-based interactive interface

📂 Project Structure
confidence-weighted-rag/
│
├── app/
│   ├── api/                # Upload & query endpoints
│   ├── retrievers/         # Multi-agent retrievers
│   ├── arbitration/        # Confidence scoring & fusion
│   ├── llm/                # LLM generator interface
│   └── main.py             # Application entry
│
├── data/
│   ├── index/              # Vector indices
│   └── uploads/            # Uploaded documents
│
├── streamlit_app.py        # UI
├── test_*.py               # Evaluation tests
└── README.md

⚙️ Tech Stack

Language: Python 3.9+

LLM: Ollama (CodeLLaMA / compatible models)

Retrieval: FAISS, custom retrievers

Embeddings: Sentence-level embeddings

Frontend: Streamlit

Backend: Modular Python architecture

🚀 How It Works (High Level)

User uploads PDFs

Documents are indexed

Query triggers parallel retrieval agents

Evidence is scored & arbitrated

LLM generates:

an answer or

an abstention if confidence is low

📊 Example Behavior
Scenario	System Response
Strong agreement across agents	Confident answer
Conflicting evidence	Abstains with explanation
Insufficient evidence	“Insufficient evidence to answer”
🧪 Evaluation Philosophy

CW-MARAG prioritizes:

Correct abstention over wrong answers

Faithfulness over fluency

Explainability over blind confidence

This aligns with emerging best practices in trustworthy AI and responsible RAG systems.

📚 Research & Novelty
What makes CW-MARAG different?

Confidence-weighted arbitration (not simple ranking)

Explicit contradiction modeling

Multi-agent evidence disagreement handling

Generator-level abstention logic

These aspects make CW-MARAG suitable for:

Research publication

Patent filing

High-stakes QA systems

🔒 License

MIT License — open for research and extension.

👤 Author

Alex Rohith
AI & ML Engineer
Focus areas: RAG systems, LLM reliability, trustworthy AI
