from app.retrievers.semantic import SemanticRetriever

docs = [
    "Retrieval-Augmented Generation combines retrieval and generation.",
    "FAISS is a vector database for similarity search.",
    "SBERT produces sentence embeddings."
]

retriever = SemanticRetriever()
retriever.build_index(docs)

results = retriever.retrieve("What is RAG?")
print(results)
