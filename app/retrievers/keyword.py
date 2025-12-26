from rank_bm25 import BM25Okapi
import re


class KeywordRetriever:
    def __init__(self):
        self.corpus = []
        self.tokenized_corpus = []
        self.bm25 = None

    def _tokenize(self, text):
        # simple, fast tokenizer
        return re.findall(r"\w+", text.lower())

    def build_index(self, texts):
        self.corpus = texts
        self.tokenized_corpus = [self._tokenize(t) for t in texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query, top_k=5):
        if self.bm25 is None:
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for idx, score in ranked[:top_k]:
            if score <= 0:
                continue

            results.append({
                "text": self.corpus[idx],
                "score": float(score),
                "source": "keyword"
            })

        return results
