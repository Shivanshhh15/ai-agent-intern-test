from app.rag.retriever import RAGRetriever


class SupportAgent:

    def __init__(self):
        self.retriever = RAGRetriever()

    def answer(self, question: str) -> dict:

        results = self.retriever.search(
            question,
            n_results=5,
        )

        if not results:
            return {
                "answer": (
                    "I couldn't find a relevant answer "
                    "in the knowledge base."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        selected = self._select_best_result(
            question,
            results,
        )


        distance = selected["distance"]

        if distance > 1.5:
            return {
                "answer": (
                    "I couldn't find a reliable answer "
                    "to that question in the knowledge base."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        metadata = selected["metadata"]
        text = selected["text"]

        answer = self._generate_answer(
            question,
            text,
        )

        source = {
            "filename": metadata.get(
                "filename",
                "Unknown",
            ),
            "heading": metadata.get(
                "heading",
                "Unknown",
            ),
        }

        
        confidence = max(
            0.0,
            min(
                1.0,
                1.0 - (distance / 1.5),
            ),
        )

        return {
            "answer": answer,
            "sources": [source],
            "confidence": round(
                confidence,
                2,
            ),
        }

    def _select_best_result(
        self,
        question: str,
        results: list[dict],
    ) -> dict:

        question_lower = question.lower()

        
        if any(
            word in question_lower
            for word in [
                "return",
                "returns",
                "refund",
                "unused",
            ]
        ):

            policy_results = [
                result
                for result in results
                if "returns-policy-current"
                in result["metadata"].get(
                    "filename",
                    "",
                )
            ]

            if policy_results:
                return policy_results[0]

        if any(
            word in question_lower
            for word in [
                "ship",
                "shipping",
                "delivery",
            ]
        ):

            shipping_results = [
                result
                for result in results
                if "shipping"
                in result["metadata"].get(
                    "filename",
                    "",
                )
            ]

            if shipping_results:
                return shipping_results[0]

        
        if any(
            word in question_lower
            for word in [
                "warranty",
                "warrant",
                "covered",
            ]
        ):

            warranty_results = [
                result
                for result in results
                if "warranty"
                in result["metadata"].get(
                    "filename",
                    "",
                )
            ]

            if warranty_results:
                return warranty_results[0]

        return results[0]

    @staticmethod
    def _generate_answer(
        question: str,
        context: str,
    ) -> str:

        return context.strip()