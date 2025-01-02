from flask import Flask, request, jsonify, redirect, url_for
from flask import send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
app.secret_key = 'your_secret_key'  # Needed for session management

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':  # Simple check
            user = User(id=1)
            login_user(user)
            return redirect(url_for('protected'))
        return 'Invalid credentials', 401
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@app.route('/protected')
@login_required
def protected():
    return f'Logged in as: {current_user.id}'


@app.route('/synthesize', methods=['POST'])
@login_required
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