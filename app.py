from flask import Flask, request, jsonify
from mlEngine import get_prediction

app = Flask(__name__)

ALLOWED_FILE_EXTENTION = ['jpg','png','jpeg']

def is_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENTION


@app.route('/predict', methods=['GET','POST'])
def image_selection():
    if request.method == 'POST':
        image = request.files.get('image')
        if image and is_allowed(image.filename):
            try:
                prediction = get_prediction(image)
                return jsonify({'prediction': prediction})
            except Exception as e:
                return jsonify({'error': str(e)})
        return jsonify({'error': 'Invalid image file'})
    return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(port=8080, debug=True)