import math
import re

from brains.geometry.vision.geometry_extractor import GeometryExtractor
from brains.geometry.vision.geometry_fact_validator import GeometryFactValidator
from brains.geometry.vision.question_analyzer import GeometryQuestionAnalyzer

from brains.geometry.triangles.triangle_brain import (
    pythagoras_hypotenuse,
    triangle_area,
)

from brains.geometry.circles.circle_brain import (
    circle_area,
    circumference,
)

from brains.geometry.coordinates.coordinate_brain import (
    distance,
    midpoint,
    gradient,
)

from brains.geometry.angles.angle_brain import polygon_interior_sum


class GeometryPipeline:

    def __init__(self, model="qwen2.5vl:7b"):
        self.extractor = GeometryExtractor(model)
        self.validator = GeometryFactValidator()
        self.question_analyzer = GeometryQuestionAnalyzer()

    def clean_number(self, value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    def target_segment(self, question):
        if not question:
            return None

        match = re.search(
            r"\b([A-Z])\s*([A-Z])\b",
            question.upper()
        )

        if match:
            return match.group(1) + match.group(2)

        match = re.search(
            r"\b([A-Z]{2})\b",
            question.upper()
        )

        if match:
            return match.group(1)

        return None

    def segment_name(self, segment):
        start = segment.get("start")
        end = segment.get("end")

        if not start or not end:
            return None

        return f"{start}{end}".upper()

    def get_segments(self, facts):
        result = []

        for segment in facts.get("segments", []):

            if not isinstance(segment, dict):
                continue

            if "length" not in segment:
                continue

            name = self.segment_name(segment)

            if not name:
                continue

            try:
                value = float(segment["length"])
            except (TypeError, ValueError):
                continue

            result.append({
                "name": name,
                "start": segment.get("start"),
                "end": segment.get("end"),
                "length": value,
                "unit": segment.get("unit", "")
            })

        return result

    def detect_unit(self, facts):

        for item in facts.get("segments", []):
            if item.get("unit"):
                return item["unit"]

        for item in facts.get("lengths", []):
            if item.get("unit"):
                return item["unit"]

        return ""

    def area_unit(self, facts):
        unit = self.detect_unit(facts)
        return f"{unit}²" if unit else ""

    def solve_right_triangle(self, facts, target):

        segments = self.get_segments(facts)

        if len(segments) < 2:
            return None

        if target == "hypotenuse":

            a = segments[0]["length"]
            b = segments[1]["length"]

            answer = pythagoras_hypotenuse(a, b)

            return {
                "method": "Pythagoras",
                "answer": self.clean_number(answer),
                "unit": self.detect_unit(facts),
                "steps": [
                    f"a = {self.clean_number(a)}",
                    f"b = {self.clean_number(b)}",
                    f"c = √({self.clean_number(a)}² + {self.clean_number(b)}²)",
                    f"c = {self.clean_number(answer)}"
                ]
            }

        if target == "area":

            answer = triangle_area(
                segments[0]["length"],
                segments[1]["length"]
            )

            return {
                "method": "Triangle area",
                "answer": self.clean_number(answer),
                "unit": self.area_unit(facts),
                "steps": [
                    "Area = ½ × base × height",
                    f"Area = ½ × {segments[0]['length']:g} × {segments[1]['length']:g}",
                    f"Area = {self.clean_number(answer)}"
                ]
            }

        return None

    def solve_circle(self, facts, target):

        circles = facts.get("circles", [])

        if not circles:
            return None

        circle = circles[0]

        radius = circle.get("radius")

        if radius is None and circle.get("diameter") is not None:
            radius = float(circle["diameter"]) / 2

        if radius is None:
            return None

        radius = float(radius)

        if target == "area":

            answer = circle_area(radius)

            return {
                "method": "Circle area",
                "answer": self.clean_number(answer),
                "unit": self.area_unit(facts),
                "steps": [
                    "Area = πr²",
                    f"Area = π × {radius:g}²",
                    f"Area = {self.clean_number(answer)}"
                ]
            }

        if target == "circumference":

            answer = circumference(radius)

            return {
                "method": "Circle circumference",
                "answer": self.clean_number(answer),
                "unit": self.detect_unit(facts),
                "steps": [
                    "Circumference = 2πr",
                    f"Circumference = 2π × {radius:g}",
                    f"Circumference = {self.clean_number(answer)}"
                ]
            }

        return None

    def solve_coordinates(self, facts, target):

        coordinates = facts.get("coordinates", [])

        if len(coordinates) < 2:
            return None

        p1 = coordinates[0]
        p2 = coordinates[1]

        point1 = (float(p1["x"]), float(p1["y"]))
        point2 = (float(p2["x"]), float(p2["y"]))

        if target == "distance":
            answer = distance(point1, point2)

            return {
                "method": "Distance formula",
                "answer": self.clean_number(answer),
                "unit": "units",
                "steps": [
                    "d = √((x₂-x₁)² + (y₂-y₁)²)",
                    f"d = {self.clean_number(answer)}"
                ]
            }

        if target == "midpoint":
            answer = midpoint(point1, point2)

            return {
                "method": "Midpoint formula",
                "answer": answer,
                "unit": "",
                "steps": [
                    "M = ((x₁+x₂)/2, (y₁+y₂)/2)",
                    f"M = {answer}"
                ]
            }

        if target == "gradient":
            answer = gradient(point1, point2)

            return {
                "method": "Gradient formula",
                "answer": self.clean_number(answer),
                "unit": "",
                "steps": [
                    "m = (y₂-y₁)/(x₂-x₁)",
                    f"m = {self.clean_number(answer)}"
                ]
            }

        return None

    def solve_polygon(self, facts, target):

        points = facts.get("points", [])

        if target != "interior_sum":
            return None

        sides = len(points)

        if sides < 3:
            return None

        answer = polygon_interior_sum(sides)

        return {
            "method": "Polygon interior angle sum",
            "answer": self.clean_number(answer),
            "unit": "degrees",
            "steps": [
                f"Number of sides = {sides}",
                f"Sum = ({sides} - 2) × 180°",
                f"Sum = {self.clean_number(answer)}°"
            ]
        }

    def solve(self, image_path, question):

        print()
        print("================================")
        print("       GEOMETRY AI PIPELINE")
        print("================================")
        print()

        print("1. Reading diagram...")
        facts = self.extractor.extract(image_path)

        print("✅ Diagram extracted.")
        print()

        print("2. Understanding question...")
        question_info = self.question_analyzer.analyze(question)

        print("Target:", question_info["target"])
        print("Confidence:", question_info["confidence"])
        print()

        if not question_info["target"]:

            return {
                "success": False,
                "stage": "question",
                "facts": facts,
                "question": question_info,
                "message": "I could not determine what must be calculated."
            }

        print("3. Validating diagram facts...")
        validation = self.validator.validate(facts)

        if not validation["valid"]:

            return {
                "success": False,
                "stage": "validation",
                "facts": facts,
                "question": question_info,
                "validation": validation,
                "message":
                    "The diagram information is inconsistent. "
                    "I will not guess."
            }

        print("✅ Facts passed validation.")
        print()

        target = question_info["target"]
        shape = str(facts.get("shape", "")).lower()

        result = None

        if (
            "right" in shape
            or any(
                isinstance(a, dict)
                and float(a.get("value", 0)) == 90
                for a in facts.get("angles", [])
            )
        ):
            result = self.solve_right_triangle(
                facts,
                target
            )

        if result is None and (
            "circle" in shape
            or facts.get("circles")
        ):
            result = self.solve_circle(
                facts,
                target
            )

        if result is None and facts.get("coordinates"):
            result = self.solve_coordinates(
                facts,
                target
            )

        if result is None:
            result = self.solve_polygon(
                facts,
                target
            )

        if result is None:

            return {
                "success": False,
                "stage": "solver",
                "facts": facts,
                "question": question_info,
                "validation": validation,
                "message":
                    "The diagram was understood, but this "
                    "problem type is not yet supported."
            }

        return {
            "success": True,
            "stage": "complete",
            "facts": facts,
            "question": question_info,
            "validation": validation,
            "method": result["method"],
            "answer": result["answer"],
            "unit": result["unit"],
            "steps": result["steps"]
        }


if __name__ == "__main__":
    print("Geometry Pipeline loaded successfully.")
