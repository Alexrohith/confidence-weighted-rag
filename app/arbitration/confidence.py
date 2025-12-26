from collections import defaultdict


class ConfidenceArbitrator:
    def __init__(
        self,
        alpha=0.6,
        beta=0.4,
        gamma=0.5,     # softer contradiction
        delta=0.2
    ):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

    def arbitrate(self, semantic_results, keyword_results, contradiction_results):
        evidence_map = defaultdict(lambda: {
            "semantic": 0.0,
            "keyword": 0.0,
            "contradiction": 0.0,
            "sources": set()
        })

        for r in semantic_results:
            evidence_map[r["text"]]["semantic"] = r["score"]
            evidence_map[r["text"]]["sources"].add("semantic")

        for r in keyword_results:
            evidence_map[r["text"]]["keyword"] = r["score"]
            evidence_map[r["text"]]["sources"].add("keyword")

        for r in contradiction_results:
            evidence_map[r["text"]]["contradiction"] = r["score"]
            evidence_map[r["text"]]["sources"].add("contradiction")

        final_results = []

        for text, d in evidence_map.items():

            # Agreement bonus ONLY if semantic + keyword
            agreement_bonus = (
                self.delta
                if {"semantic", "keyword"}.issubset(d["sources"])
                else 0.0
            )

            # 🔥 CRITICAL CHANGE
            # Soften contradiction if no keyword support exists
            contradiction_penalty = (
                self.gamma * d["contradiction"]
                if d["keyword"] > 0
                else 0.2 * d["contradiction"]
            )

            confidence = (
                self.alpha * d["semantic"]
                + self.beta * d["keyword"]
                - contradiction_penalty
                + agreement_bonus
            )

            final_results.append({
                "text": text,
                "confidence": round(confidence, 4),
                "breakdown": {
                    "semantic": d["semantic"],
                    "keyword": d["keyword"],
                    "contradiction": d["contradiction"],
                    "agreement_bonus": agreement_bonus
                }
            })

        final_results.sort(key=lambda x: x["confidence"], reverse=True)
        return final_results
