import os
from flask import Flask, request, jsonify, render_template
from eleRating.pipeline.run_prediction import run_prediction
from eleRating.constant import UPLOAD_IMAGE_DIR, IMAGE_SAVE_DIR, TEMP_FILE_MAX_AGE
from eleRating.utils import (
    is_allowed,
    make_dir,
    unique_filenameuni,
    create_temp_directory_with_age_limit,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder="static", template_folder="templates")

limiter = Limiter(get_remote_address, app=app)  # Initialize rate limiter


@app.route("/")
def index():
    """
    Renders the upload form page.
    """
    return render_template("index.html")


@limiter.limit("20 per minute")  # Apply rate limit
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
                # Save the uploaded image to a folder
                tem_folder = create_temp_directory_with_age_limit(
                    UPLOAD_IMAGE_DIR, max_age=TEMP_FILE_MAX_AGE
                )
                unique_filename = unique_filenameuni(image.filename)
                image_path = os.path.join(tem_folder, unique_filename)
                image.save(image_path)

                # Run the prediction
                rating, result_image_path = run_prediction(image_path)

                # Return the result to the frontend
                return jsonify(
                    {
                        "prediction": rating,
                        "image_path": f"{tem_folder}/{unique_filename}",
                        "result_image": f"{result_image_path}",
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
    app.run()
