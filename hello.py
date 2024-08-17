from flask import Flask, request, jsonify, send_file
from io import BytesIO
from PIL import Image
import json
import random
import requests
import torch
import rembg

app = Flask(__name__)

# Data model for the "Scan face" endpoint
class ScanFaceRequest:
    def __init__(self, image):
        self.image = image

class ScanFaceResponse:
    def __init__(self, generated_image):
        self.generated_image = generated_image

# Data model for the "Matching" endpoint
class MatchingRequest:
    def __init__(self, strings):
        self.strings = strings

class MatchingResponse:
    def __init__(self, match_result):
        self.match_result = match_result

def cartoonify(img):
    # Load the models (this could be optimized by loading them outside the function if called repeatedly)
    face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", size=512)
    model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v1")

    # Resize the image (assuming 'img' is already an opened PIL Image)
    image = img.resize((512, 512))

    # Apply the cartoonification
    out = face2paint(model, image)

    return out


@app.route('/scan_face', methods=['POST'])
def scan_face():
    # Get the image from the request
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Open the image from the request
        input_image = Image.open(image_file)
        
        # Process the image (e.g., cartoonify)
        output_cartoon = cartoonify(input_image)  # Assuming cartoonify is your function

        # Remove the background
        output_no_bg = rembg.remove(output_cartoon)

        # Convert the processed image to bytes and send as a response
        img_io = BytesIO()
        output_no_bg.save(img_io, 'PNG')  # PNG format preserves transparency
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
@app.route('/matching', methods=['POST'])
def matching():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'data' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    """ 
    TODO: Add your function to calculate data from 'data' and return an integer of similarity.
    After that, pass the integer to variable match_result
    """
    
    match_result = random.randint(1, 100)

    return jsonify({"match_result": match_result})

if __name__ == '__main__':
    app.run(debug=True)