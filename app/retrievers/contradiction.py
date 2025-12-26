from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np


class ContradictionRetriever:
    def __init__(self, model_name="facebook/bart-large-mnli"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()

        # Label mapping for MNLI models
        self.label_map = {0: "contradiction", 1: "neutral", 2: "entailment"}

    def _predict(self, premise, hypothesis):
        inputs = self.tokenizer(
            premise,
            hypothesis,
            return_tensors="pt",
            truncation=True,
            padding=True,
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1).squeeze()

        return {
            "contradiction": probs[0].item(),
            "neutral": probs[1].item(),
            "entailment": probs[2].item(),
        }

    def retrieve(self, query, documents, threshold=0.6):
        """
        query      : user question or provisional claim
        documents  : list of text chunks
        threshold  : minimum contradiction probability
        """
        results = []

        for doc in documents:
            scores = self._predict(doc, query)

            if scores["contradiction"] >= threshold:
                results.append({
                    "text": doc,
                    "score": scores["contradiction"],
                    "source": "contradiction"
                })

        # Sort strongest contradictions first
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
