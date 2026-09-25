class GeometryAnswerExplainer:

    def explain(self, result):

        if not result:
            return "I could not produce a result."

        if not result.get("success"):
            return result.get(
                "message",
                "I could not solve this question."
            )

        method = result.get("method", "")
        answer = result.get("answer")
        unit = result.get("unit", "")
        steps = result.get("steps", [])

        lines = []

        lines.append("🤖 AI CEO")
        lines.append("")
        lines.append(f"📐 Method: {method}")
        lines.append("")

        for index, step in enumerate(steps, 1):
            lines.append(
                f"Step {index}: {step}"
            )

        lines.append("")

        if unit:
            lines.append(
                f"✅ Final Answer: {answer} {unit}"
            )
        else:
            lines.append(
                f"✅ Final Answer: {answer}"
            )

        return "\n".join(lines)


if __name__ == "__main__":

    explainer = GeometryAnswerExplainer()

    result = {
        "success": True,
        "method": "Pythagoras",
        "answer": 5,
        "unit": "cm",
        "steps": [
            "a = 3",
            "b = 4",
            "c = √(3² + 4²)",
            "c = 5"
        ]
    }

    print(explainer.explain(result))
