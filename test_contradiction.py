from app.retrievers.contradiction import ContradictionRetriever

docs = [
    "FAISS is a vector database for similarity search.",
    "FAISS is not used for vector similarity and does not support embeddings.",
    "SBERT generates sentence embeddings."
]

query = "FAISS is used for similarity search."

retriever = ContradictionRetriever()
results = retriever.retrieve(query, docs)

print(results)
