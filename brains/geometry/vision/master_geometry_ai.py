from brains.geometry.vision.geometry_pipeline import GeometryPipeline
from brains.geometry.vision.answer_explainer import GeometryAnswerExplainer


class MasterGeometryAI:

    def __init__(self, model="qwen2.5vl:7b"):
        self.pipeline = GeometryPipeline(model)
        self.explainer = GeometryAnswerExplainer()

    def solve(self, image_path, question):

        result = self.pipeline.solve(
            image_path,
            question
        )

        explanation = self.explainer.explain(
            result
        )

        return {
            "result": result,
            "answer": explanation
        }


if __name__ == "__main__":

    print()
    print("===================================")
    print("       MASTER GEOMETRY AI")
    print("===================================")
    print()

    print("✅ Qwen Vision")
    print("✅ Question Analyzer")
    print("✅ Geometry Fact Validator")
    print("✅ Geometry Solver")
    print("✅ Answer Explainer")

    print()
    print("🤖 MASTER GEOMETRY AI READY")
    print()
