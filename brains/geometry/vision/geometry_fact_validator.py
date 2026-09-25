import math


class GeometryFactValidator:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def reset(self):
        self.errors = []
        self.warnings = []

    def error(self, message):
        self.errors.append(message)

    def warning(self, message):
        self.warnings.append(message)

    def check_number(self, value, name="value"):
        if value is None:
            self.error(f"{name} is missing.")
            return False

        if not isinstance(value, (int, float)):
            self.error(f"{name} is not a number.")
            return False

        if not math.isfinite(float(value)):
            self.error(f"{name} is not finite.")
            return False

        if float(value) < 0:
            self.error(f"{name} cannot be negative.")
            return False

        return True

    def check_points(self, data):
        points = data.get("points", [])

        if not isinstance(points, list):
            self.error("Points must be a list.")
            return

        cleaned = []

        for point in points:
            if not isinstance(point, str):
                self.error("A point label is not text.")
                continue

            point = point.strip()

            if not point:
                self.error("An empty point label was found.")
                continue

            if point not in cleaned:
                cleaned.append(point)

        if len(cleaned) != len(points):
            self.warning("Duplicate or invalid point labels detected.")

    def check_lengths(self, data):
        lengths = data.get("lengths", [])

        if not isinstance(lengths, list):
            self.error("Lengths must be a list.")
            return

        for item in lengths:

            if not isinstance(item, dict):
                self.error("Invalid length entry.")
                continue

            if "value" not in item:
                self.error("A length is missing its value.")
                continue

            self.check_number(
                item["value"],
                "length"
            )

    def check_segments(self, data):
        segments = data.get("segments", [])

        if not isinstance(segments, list):
            self.error("Segments must be a list.")
            return

        for segment in segments:

            if not isinstance(segment, dict):
                self.error("Invalid segment entry.")
                continue

            start = segment.get("start")
            end = segment.get("end")

            if not start or not end:
                self.error(
                    "A segment is missing start/end points."
                )

            if start == end and start:
                self.error(
                    f"Segment {start}{end} has identical endpoints."
                )

            if "length" in segment:
                self.check_number(
                    segment["length"],
                    f"segment {start}{end} length"
                )

    def check_angles(self, data):
        angles = data.get("angles", [])

        if not isinstance(angles, list):
            self.error("Angles must be a list.")
            return

        values = []

        for angle in angles:

            if not isinstance(angle, dict):
                self.error("Invalid angle entry.")
                continue

            if "value" not in angle:
                continue

            value = angle["value"]

            if not self.check_number(value, "angle"):
                continue

            if value > 360:
                self.error(
                    f"Angle {value}° is greater than 360°."
                )

            values.append(float(value))

        # If exactly three angles are explicitly identified,
        # check whether they form a triangle.
        if len(values) == 3:
            total = sum(values)

            if not math.isclose(total, 180.0, abs_tol=1e-9):
                self.error(
                    f"Three triangle angles add to {total}°, "
                    f"not 180°."
                )

    def check_coordinates(self, data):
        coordinates = data.get("coordinates", [])

        if not isinstance(coordinates, list):
            self.error("Coordinates must be a list.")
            return

        seen = set()

        for item in coordinates:

            if not isinstance(item, dict):
                self.error("Invalid coordinate entry.")
                continue

            point = item.get("point")

            if "x" not in item or "y" not in item:
                self.error(
                    f"Coordinate for {point} is incomplete."
                )
                continue

            x = item["x"]
            y = item["y"]

            if not self.check_number(x, f"{point} x-coordinate"):
                continue

            if not self.check_number(y, f"{point} y-coordinate"):
                continue

            if point in seen:
                self.warning(
                    f"Duplicate coordinates for point {point}."
                )

            seen.add(point)

    def check_circles(self, data):
        circles = data.get("circles", [])

        if not isinstance(circles, list):
            self.error("Circles must be a list.")
            return

        for circle in circles:

            if not isinstance(circle, dict):
                self.error("Invalid circle entry.")
                continue

            if "radius" in circle:
                self.check_number(
                    circle["radius"],
                    "circle radius"
                )

            if "diameter" in circle:
                self.check_number(
                    circle["diameter"],
                    "circle diameter"
                )

            radius = circle.get("radius")
            diameter = circle.get("diameter")

            if radius is not None and diameter is not None:

                if not math.isclose(
                    float(diameter),
                    float(radius) * 2,
                    abs_tol=1e-9
                ):
                    self.error(
                        "Circle radius and diameter "
                        "are inconsistent."
                    )

    def check_relationships(self, data):
        relationships = data.get("relationships", [])

        if not isinstance(relationships, list):
            self.error("Relationships must be a list.")
            return

        valid_types = {
            "parallel",
            "perpendicular",
            "right_angle",
            "equal",
            "equal_length",
            "equal_angle",
            "similar",
            "congruent"
        }

        for relationship in relationships:

            if not isinstance(relationship, dict):
                self.error("Invalid relationship entry.")
                continue

            relation_type = relationship.get("type")

            if relation_type not in valid_types:
                self.warning(
                    f"Unknown relationship type: "
                    f"{relation_type}"
                )

            objects = relationship.get("objects")

            if not isinstance(objects, list):
                self.error(
                    f"Objects for {relation_type} "
                    f"must be a list."
                )

    def check_shape(self, data):
        shape = data.get("shape", "")

        if shape is None:
            self.warning("Shape is missing.")
            return

        if not isinstance(shape, str):
            self.error("Shape must be text.")

    def validate(self, data):

        self.reset()

        if not isinstance(data, dict):
            self.error("Geometry data must be a dictionary.")
            return self.result()

        required = [
            "shape",
            "points",
            "lines",
            "segments",
            "angles",
            "lengths",
            "circles",
            "arcs",
            "coordinates",
            "relationships",
            "unknown"
        ]

        for key in required:
            if key not in data:
                self.error(
                    f"Missing geometry field: {key}"
                )

        self.check_shape(data)
        self.check_points(data)
        self.check_lengths(data)
        self.check_segments(data)
        self.check_angles(data)
        self.check_coordinates(data)
        self.check_circles(data)
        self.check_relationships(data)

        return self.result()

    def result(self):

        return {
            "valid": len(self.errors) == 0,
            "errors": list(self.errors),
            "warnings": list(self.warnings)
        }


def print_result(result):

    print()
    print("GEOMETRY FACT VALIDATION")
    print("========================")
    print()

    if result["valid"]:
        print("✅ FACTS PASSED VALIDATION")
    else:
        print("❌ FACT VALIDATION FAILED")

    print()

    if result["errors"]:
        print("ERRORS:")
        for error in result["errors"]:
            print("❌", error)
    else:
        print("No errors.")

    print()

    if result["warnings"]:
        print("WARNINGS:")
        for warning in result["warnings"]:
            print("⚠️", warning)
    else:
        print("No warnings.")

    print()


if __name__ == "__main__":

    validator = GeometryFactValidator()

    good_data = {
        "shape": "right_triangle",
        "points": ["A", "B", "C"],
        "lines": [],
        "segments": [
            {
                "start": "A",
                "end": "B",
                "length": 3,
                "unit": "cm"
            },
            {
                "start": "B",
                "end": "C",
                "length": 4,
                "unit": "cm"
            }
        ],
        "angles": [
            {
                "vertex": "B",
                "value": 90,
                "unit": "degrees"
            }
        ],
        "lengths": [],
        "circles": [],
        "arcs": [],
        "coordinates": [],
        "relationships": [
            {
                "type": "perpendicular",
                "objects": ["AB", "BC"]
            }
        ],
        "unknown": []
    }

    print("TEST 1 — VALID DATA")
    result = validator.validate(good_data)
    print_result(result)

    bad_data = {
        "shape": "triangle",
        "points": ["A", "B", "C"],
        "lines": [],
        "segments": [],
        "angles": [
            {"vertex": "A", "value": 90},
            {"vertex": "B", "value": 80},
            {"vertex": "C", "value": 50}
        ],
        "lengths": [],
        "circles": [],
        "arcs": [],
        "coordinates": [],
        "relationships": [],
        "unknown": []
    }

    print("TEST 2 — INVALID TRIANGLE")
    result = validator.validate(bad_data)
    print_result(result)

    circle_data = {
        "shape": "circle",
        "points": [],
        "lines": [],
        "segments": [],
        "angles": [],
        "lengths": [],
        "circles": [
            {
                "radius": 5,
                "diameter": 10
            }
        ],
        "arcs": [],
        "coordinates": [],
        "relationships": [],
        "unknown": []
    }

    print("TEST 3 — CIRCLE")
    result = validator.validate(circle_data)
    print_result(result)
