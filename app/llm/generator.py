import requests
import re


class LLMGenerator:
    def __init__(self, model="codellama:7b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, question, evidence, max_evidence=3):
        if not evidence:
            return "Insufficient evidence to answer the question."

        trusted = [e for e in evidence if e["confidence"] > 0]
        contradictory = [e for e in evidence if e["confidence"] <= 0]

        # Case 1: Only contradiction
        if not trusted and contradictory:
            return (
                "The document contains contradictory evidence related to this question. "
                "A definitive answer cannot be determined."
            )

        if not trusted:
            return "Insufficient evidence to answer the question."

        # 🔒 YES/NO POLARITY ENFORCEMENT
        is_yes_no = question.lower().startswith(("is ", "are ", "does ", "do ", "can "))

        # Decide polarity from trusted evidence
        trusted_text = " ".join(e["text"].lower() for e in trusted)

        if is_yes_no:
            if "not suitable" in trusted_text or "unsuitable" in trusted_text:
                forced_answer = "Yes."
            else:
                forced_answer = "No."
        else:
            forced_answer = ""

        context = "\n".join(
            f"- {e['text']}" for e in trusted[:max_evidence]
        )

        prompt = f"""
You are a factual assistant.

Answer the question using ONLY the evidence below.
Explain briefly.
Do NOT contradict the forced answer.

Forced answer:
{forced_answer}

Question:
{question}

Evidence:
{context}

Answer:
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        return response.json()["response"].strip()
