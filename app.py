from flask import Flask, request, jsonify
from eleRating.pipeline.run_prediction import run_prediction
from eleRating.utils import is_allowed

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def image_selection():
    """
    API route for handling image uploads and returning the prediction result.
    """
    if request.method == "POST":
        # Check if image file is part of the request
        image = request.files.get("image")

        # Validate the uploaded file
        if image and is_allowed(image.filename):
            try:

                rating = run_prediction(image)
                return jsonify({"prediction": rating})

            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return (
                jsonify(
                    {"error": "Invalid image file. Allowed file types: jpg, jpeg, png."}
                ),
                400,
            )

    return jsonify({"error": "Invalid request method. Use POST."}), 405


if __name__ == "__main__":
    app.run(port=8181, debug=True)
