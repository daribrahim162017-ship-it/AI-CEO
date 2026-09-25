import json
import re


class GeometryDiagramReader:

    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {
            "points": [],
            "lines": [],
            "segments": [],
            "angles": [],
            "lengths": [],
            "circles": [],
            "arcs": [],
            "coordinates": [],
            "relationships": [],
            "unknown": []
        }

    def add_point(self, name):
        if name and name not in self.data["points"]:
            self.data["points"].append(name)

    def add_line(self, start, end):
        item = {
            "start": start,
            "end": end
        }

        if item not in self.data["lines"]:
            self.data["lines"].append(item)

        self.add_point(start)
        self.add_point(end)

    def add_segment(self, start, end, length=None, unit=None):
        item = {
            "start": start,
            "end": end
        }

        if length is not None:
            item["length"] = length

        if unit:
            item["unit"] = unit

        if item not in self.data["segments"]:
            self.data["segments"].append(item)

        self.add_point(start)
        self.add_point(end)

    def add_angle(self, vertex, value=None, unit="degrees"):
        item = {
            "vertex": vertex
        }

        if value is not None:
            item["value"] = value

        if unit:
            item["unit"] = unit

        self.data["angles"].append(item)

    def add_length(self, name, value, unit=None):
        item = {
            "name": name,
            "value": value
        }

        if unit:
            item["unit"] = unit

        self.data["lengths"].append(item)

    def add_circle(self, center=None, radius=None, diameter=None):
        item = {}

        if center:
            item["center"] = center

        if radius is not None:
            item["radius"] = radius

        if diameter is not None:
            item["diameter"] = diameter

        self.data["circles"].append(item)

    def add_arc(self, name=None, radius=None, angle=None):
        item = {}

        if name:
            item["name"] = name

        if radius is not None:
            item["radius"] = radius

        if angle is not None:
            item["angle"] = angle

        self.data["arcs"].append(item)

    def add_coordinate(self, point, x, y):
        item = {
            "point": point,
            "x": x,
            "y": y
        }

        self.data["coordinates"].append(item)
        self.add_point(point)

    def add_relationship(self, relationship, objects):
        self.data["relationships"].append({
            "type": relationship,
            "objects": objects
        })

    def add_unknown(self, text):
        if text and text not in self.data["unknown"]:
            self.data["unknown"].append(text)

    def load(self, data):
        self.reset()

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return False

        if not isinstance(data, dict):
            return False

        for key in self.data:
            if key in data and isinstance(data[key], list):
                self.data[key] = data[key]

        return True

    def extract_numbers(self, text):
        if not text:
            return []

        values = re.findall(
            r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?',
            text
        )

        return [float(x) for x in values]

    def detect_units(self, text):
        if not text:
            return None

        units = [
            "cm",
            "mm",
            "m",
            "km",
            "in",
            "ft",
            "degrees",
            "degree",
            "°"
        ]

        lower = text.lower()

        for unit in units:
            if unit in lower:
                return unit

        return None

    def summary(self):
        return {
            "points": len(self.data["points"]),
            "lines": len(self.data["lines"]),
            "segments": len(self.data["segments"]),
            "angles": len(self.data["angles"]),
            "lengths": len(self.data["lengths"]),
            "circles": len(self.data["circles"]),
            "arcs": len(self.data["arcs"]),
            "coordinates": len(self.data["coordinates"]),
            "relationships": len(self.data["relationships"]),
            "unknown": len(self.data["unknown"])
        }

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(
            self.data,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":

    reader = GeometryDiagramReader()

    reader.add_point("A")
    reader.add_point("B")
    reader.add_point("C")

    reader.add_segment("A", "B", 5, "cm")
    reader.add_segment("B", "C", 4, "cm")

    reader.add_angle("B", 90)

    reader.add_relationship(
        "perpendicular",
        ["AB", "BC"]
    )

    reader.add_coordinate("A", 0, 0)
    reader.add_coordinate("B", 3, 4)

    print("GEOMETRY DIAGRAM READER TEST")
    print("============================")
    print()

    print(reader.to_json())
    print()

    print("SUMMARY")
    print(reader.summary())
