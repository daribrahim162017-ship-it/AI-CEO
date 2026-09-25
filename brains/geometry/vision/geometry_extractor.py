import json
import re
import subprocess

from brains.geometry.vision.diagram_reader import GeometryDiagramReader


class GeometryExtractor:

    def __init__(self, model="qwen2.5vl:7b"):
        self.model = model
        self.reader = GeometryDiagramReader()

    def build_prompt(self):
        return r"""
You are a geometry diagram extraction system.

Look at the supplied geometry image carefully.

Your job is ONLY to extract facts from the diagram.

DO NOT solve the question.
DO NOT calculate missing values.
DO NOT guess hidden measurements.

Return ONLY valid JSON.

Use this exact structure:

{
  "shape": "",
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

Rules:

1. Record every visible labelled point.
2. Record visible line segments.
3. Record visible numerical lengths.
4. Record units such as cm, mm, m or km.
5. Record visible angles.
6. Record right-angle marks as:
   {
     "type": "right_angle",
     "objects": ["AB","BC"]
   }
7. Record parallel marks as:
   {
     "type": "parallel",
     "objects": ["AB","CD"]
   }
8. Record perpendicular lines as:
   {
     "type": "perpendicular",
     "objects": ["AB","BC"]
   }
9. Record equal-length markings.
10. Record circle radius or diameter if explicitly shown.
11. Record coordinates if visible.
12. If something cannot be read clearly, put it inside "unknown".
13. Never invent a number.
14. Never assume a line is equal to another line unless the diagram marks it equal.
15. Never assume an angle is 90 degrees just because the drawing looks like a right angle.
16. Preserve labels exactly when possible.

Example:

{
  "shape": "right_triangle",
  "points": ["A","B","C"],
  "lines": [],
  "segments": [
    {"start":"A","end":"B","length":3,"unit":"cm"},
    {"start":"B","end":"C","length":4,"unit":"cm"}
  ],
  "angles": [
    {"vertex":"B","value":90,"unit":"degrees"}
  ],
  "lengths": [],
  "circles": [],
  "arcs": [],
  "coordinates": [],
  "relationships": [
    {
      "type":"perpendicular",
      "objects":["AB","BC"]
    }
  ],
  "unknown": []
}
"""

    def clean_response(self, text):
        if not text:
            return ""

        text = text.strip()

        # Remove markdown code fences if Qwen adds them.
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        return text.strip()

    def extract_json(self, text):
        text = self.clean_response(text)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find the first JSON object.
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]

            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                return None

        return None

    def validate(self, data):
        if not isinstance(data, dict):
            return False

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
                return False

        return True

    def run_ollama(self, image_path):
        prompt = self.build_prompt()

        command = [
            "ollama",
            "run",
            self.model,
            prompt,
            image_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or
                "Ollama failed."
            )

        return result.stdout

    def extract(self, image_path):
        raw = self.run_ollama(image_path)

        data = self.extract_json(raw)

        if data is None:
            raise ValueError(
                "Qwen did not return valid JSON."
            )

        if not self.validate(data):
            raise ValueError(
                "Geometry JSON structure is incomplete."
            )

        self.reader.load(data)

        return self.reader.to_dict()


if __name__ == "__main__":

    print("GEOMETRY EXTRACTOR")
    print("==================")
    print()
    print("This module connects Qwen Vision")
    print("to the Geometry Diagram Reader.")
    print()
    print("Usage:")
    print("python -c 'from brains.geometry.vision.geometry_extractor import GeometryExtractor; print(GeometryExtractor())'")
