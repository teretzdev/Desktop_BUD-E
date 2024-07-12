import requests  # For making HTTP requests
import time  # For time-related functions

import subprocess  # For running system commands
import os 
import io
import threading
import json
import base64

florence2_server_url = "http://213.173.96.19:5002/" 
def handle_captioning_florence2(img_byte_arr, results):
    caption = send_image_for_captioning_florence2(img_byte_arr)
    results['caption'] = caption

# Function to handle OCR
def handle_ocr_florence2(img_byte_arr, results):
    ocr_result = send_image_for_ocr_florence2(img_byte_arr)
    results['ocr'] = ocr_result

def send_image_for_captioning_florence2(image_data):
    # Server URL
    url = florence2_server_url+"caption"  # Replace with your server's IP address

    try:
        # Encode image data to base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        print("Image encoded to base64")

        # Prepare the request payload
        payload = {"image": encoded_image}

        # Send POST request to the server
        print("Sending request to server...")
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            caption = response.json()["caption"] ['<MORE_DETAILED_CAPTION>']
            print("Received caption from server:")
            print(caption)
            return caption
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Error message: {response.json().get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def send_image_for_ocr_florence2(image_data):
    # Server URL
    url = url = florence2_server_url+"ocr" # Replace with your server's IP address

    try:
        # Encode image data to base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        print("Image encoded to base64")

        # Prepare the request payload
        payload = {"image": encoded_image}

        # Send POST request to the server
        print("Sending request to server...")
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            print(response.json())
            caption = response.json()["ocr"]['<OCR>']
            print("Received caption from server:")
            print(caption)
            return caption
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Error message: {response.json().get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


