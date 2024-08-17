from flask import Flask, request, jsonify, send_file
from io import BytesIO
from PIL import Image
import json
import random
import requests

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

@app.route('/scan_face', methods=['POST'])
def scan_face():
    # Get the image from the request
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "No image provided"}), 400
    
    """ 
    TODO: Change this with your function to generate image. The file scan can be accessed from image_file. 
    You can also add response if the image does not contain face with 'no face found' but it is not truly important
    """
    # Dummy image URL
    dummy_image_url = "https://lumiere-a.akamaihd.net/v1/images/a_avatarpandorapedia_neytiri_16x9_1098_01_0e7d844a.jpeg?region=0%2C0%2C1920%2C1080"
    
    try:
        # Fetch the dummy image from the URL
        response = requests.get(dummy_image_url)
        response.raise_for_status()
        
        # Open the image from the fetched content
        dummy_image = Image.open(BytesIO(response.content))
        
        # Convert the dummy image to bytes and send as a response
        img_io = BytesIO()
        dummy_image.save(img_io, 'JPEG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch dummy image from URL: {str(e)}"}), 500

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
