from flask import Flask, request, jsonify
from flask import send_from_directory
import threading
import time
import json
import os  # Import the os module

import time
import random
import yaml
from munch import Munch
import numpy as np

import requests

from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM 


model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True)

prompt = "<MORE_DETAILED_CAPTION>"   #<OCR>

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=prompt, images=image, return_tensors="pt")

generated_ids = model.generate(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    max_new_tokens=512,
    do_sample=True,
    num_beams=3
)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

parsed_answer = processor.post_process_generation(generated_text, task=prompt, image_size=(image.width, image.height))

print(parsed_answer)





app = Flask(__name__)


@app.route('/add', methods=['GET'])
def add_item():
    """Adds an item to the list received via a GET request."""
    item = request.args.get('item')
    if item:
        items.append(item)
        return jsonify(success=True, message="Item added successfully."), 200
    else:
        return jsonify(success=False, message="No item provided."), 400


@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    text = request.json.get('text')
    print("received request:", text)
    if not text:
        return jsonify(success=False, message="No text provided."), 400

    try:
        # Generate speech
        noise = torch.randn(1,1,256).to(device)
        s= time.time()
        audio = inference(text, noise, diffusion_steps=3, embedding_scale=1.2)
        print("Time for inference:",time.time()-s)
        # Generate a random filename
        random_number = random.randint(10000, 99999)
        filename = f"speech_{random_number}.wav"

        # Ensure the 'audio' directory exists
        os.makedirs('audio', exist_ok=True)

        # Save the audio file
        sf.write(os.path.join('audio', filename), audio, 24000)

        return jsonify(success=True, filename=filename), 200

    except Exception as e:
        return jsonify(success=False, message=f"An error occurred: {str(e)}"), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    try:
        return send_from_directory('audio', filename)
    except FileNotFoundError:
        return jsonify(success=False, message="Audio file not found"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    
os.system("curl ifconfig.me")

if __name__ == '__main__':

    # Starts the Flask web server
    app.run(host='0.0.0.0', port=5002)



