from app.arbitration.confidence import ConfidenceArbitrator

semantic = [
    {"text": "FAISS is a vector database.", "score": 0.82, "source": "semantic"}
]

keyword = [
    {"text": "FAISS is a vector database.", "score": 0.91, "source": "keyword"}
]

contradiction = [
    {"text": "FAISS is not used for similarity search.", "score": 0.88, "source": "contradiction"}
]

arb = ConfidenceArbitrator()
results = arb.arbitrate(semantic, keyword, contradiction)

print(results)
