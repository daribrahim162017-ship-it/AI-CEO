import re


class GeometryQuestionAnalyzer:

    def analyze(self, question):

        if not question:
            return {
                "target": None,
                "quantity": None,
                "unknown": None,
                "confidence": 0
            }

        text = question.lower().strip()

        result = {
            "target": None,
            "quantity": None,
            "unknown": None,
            "confidence": 0
        }

        # Hypotenuse
        if "hypotenuse" in text:
            result["target"] = "hypotenuse"
            result["quantity"] = "length"
            result["unknown"] = "hypotenuse"
            result["confidence"] = 1.0
            return result

        # Area
        if re.search(r"\barea\b", text):
            result["target"] = "area"
            result["quantity"] = "area"
            result["unknown"] = "area"
            result["confidence"] = 1.0
            return result

        # Circumference
        if "circumference" in text:
            result["target"] = "circumference"
            result["quantity"] = "length"
            result["unknown"] = "circumference"
            result["confidence"] = 1.0
            return result

        # Perimeter
        if "perimeter" in text:
            result["target"] = "perimeter"
            result["quantity"] = "length"
            result["unknown"] = "perimeter"
            result["confidence"] = 1.0
            return result

        # Arc length
        if "arc length" in text:
            result["target"] = "arc_length"
            result["quantity"] = "length"
            result["unknown"] = "arc length"
            result["confidence"] = 1.0
            return result

        # Sector area
        if "sector area" in text:
            result["target"] = "sector_area"
            result["quantity"] = "area"
            result["unknown"] = "sector area"
            result["confidence"] = 1.0
            return result

        # Distance
        if "distance" in text:
            result["target"] = "distance"
            result["quantity"] = "length"
            result["unknown"] = "distance"
            result["confidence"] = 1.0
            return result

        # Midpoint
        if "midpoint" in text:
            result["target"] = "midpoint"
            result["quantity"] = "coordinate"
            result["unknown"] = "midpoint"
            result["confidence"] = 1.0
            return result

        # Gradient / slope
        if "gradient" in text or "slope" in text:
            result["target"] = "gradient"
            result["quantity"] = "gradient"
            result["unknown"] = "gradient"
            result["confidence"] = 1.0
            return result

        # Interior angle sum
        if "sum of the interior angles" in text:
            result["target"] = "interior_sum"
            result["quantity"] = "angle"
            result["unknown"] = "interior angle sum"
            result["confidence"] = 1.0
            return result

        # Interior angle
        if "interior angle" in text:
            result["target"] = "interior_angle"
            result["quantity"] = "angle"
            result["unknown"] = "interior angle"
            result["confidence"] = 1.0
            return result

        # Missing angle
        if "angle" in text and (
            "find" in text
            or "calculate" in text
            or "work out" in text
        ):
            result["target"] = "angle"
            result["quantity"] = "angle"
            result["unknown"] = "angle"
            result["confidence"] = 0.7
            return result

        return result


if __name__ == "__main__":

    analyzer = GeometryQuestionAnalyzer()

    tests = [
        "Find the hypotenuse.",
        "Calculate the area.",
        "Find the circumference.",
        "Work out the perimeter.",
        "Find the distance between the points.",
        "Find the midpoint.",
        "Find the gradient.",
        "Find the sum of the interior angles."
    ]

    print("GEOMETRY QUESTION ANALYZER")
    print("==========================")

    for question in tests:
        print()
        print("Question:", question)
        print("Result:", analyzer.analyze(question))
