import os
from flask import Flask, request, jsonify, render_template
from eleRating.pipeline.run_prediction import run_prediction
from eleRating.constant import (
    UPLOAD_IMAGE_DIR,
    IMAGE_SAVE_DIR,
    IMAGE_SAVE_PATH,
    IMAGE_SAVE_NAME,
)
from eleRating.utils import is_allowed, make_dir, delete_previous_files

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    """
    Renders the upload form page.
    """
    return render_template("index.html")


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
                # Delete the previous images (uploaded and result)
                delete_previous_files(UPLOAD_IMAGE_DIR, IMAGE_SAVE_PATH)
                # Save the uploaded image to a folder
                image_path = os.path.join(UPLOAD_IMAGE_DIR, image.filename)
                image.save(image_path)

                # Run the prediction
                rating = run_prediction(image_path)

                # Return the result to the frontend
                return jsonify(
                    {
                        "prediction": rating,
                        "image_path": f"/static/uploads/{image.filename}",  # URL relative to the static directory
                        "result_image": f"/static/results/{IMAGE_SAVE_NAME}",  # Result image URL relative to static directory
                    }
                )

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
    make_dir(UPLOAD_IMAGE_DIR)
    make_dir(IMAGE_SAVE_DIR)
    app.run(host="0.0.0.0", port=8181, debug=True)
