from flask import Flask, request, jsonify
from eleRating.pipeline.run_prediction import run_prediction
from eleRating.constant import UPLOAD_IMAGE_DIR
from eleRating.utils import is_allowed, make_dir
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import time
from io import BytesIO

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)

# Initialize ProcessPoolExecutor with a worker pool size (adjust based on your CPU)
executor = ProcessPoolExecutor(max_workers=4)  # Adjust based on CPU cores


@limiter.limit("60 per minute")  # Adjusted rate limit
@app.route("/predict", methods=["POST"])
def image_selection():
    start = time.time()
    if request.method == "POST":
        image = request.files.get("image")

        if image and is_allowed(image.filename):
            try:
                img = Image.open(BytesIO(image.read()))

                # Run prediction asynchronously
                future = executor.submit(run_prediction, img)
                rating = future.result()

                done = time.time()
                elapsed = done - start
                print(f"Time Difference: {elapsed}")
                # Return the result to the frontend
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
    make_dir(UPLOAD_IMAGE_DIR)
    app.run(host="0.0.0.0", port="5051")
