from app.retrievers.keyword import KeywordRetriever

docs = [
    "Retrieval-Augmented Generation combines retrieval and generation.",
    "FAISS is a vector database for similarity search.",
    "SBERT produces sentence embeddings."
]

retriever = KeywordRetriever()
retriever.build_index(docs)

results = retriever.retrieve("What is FAISS?")
print(results)
