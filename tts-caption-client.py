import requests
import base64
from PIL import Image
import io
import time
from pyautogui import screenshot
import requests
import io
import sounddevice as sd
import soundfile as sf
import time

import threading

def handle_captioning(img_byte_arr, results):
    caption = send_image_for_captioning(img_byte_arr)
    results['caption'] = caption

# Function to handle OCR
def handle_ocr(img_byte_arr, results):
    ocr_result = send_image_for_ocr(img_byte_arr)
    results['ocr'] = ocr_result

def send_image_for_captioning(image_data):
    # Server URL
    url = "http://213.173.96.19:5002/caption"  # Replace with your server's IP address

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


def send_image_for_ocr(image_data):
    # Server URL
    url = "http://213.173.96.19:5002/ocr"  # Replace with your server's IP address

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



def get_caption_from_screenshot():
    # Delay execution for 3 seconds
    print("Waiting for 3 seconds before taking a screenshot...")
    time.sleep(3)

    # Take a screenshot and open it with PIL
    print("Taking a screenshot...")
    screenshot_image = screenshot()  # Uses PyAutoGUI to take a screenshot
    width, height = screenshot_image.size
    new_height = 500
    new_width = int((new_height / height) * width)
    
    # Resizing with the correct resampling filter
    resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save the resized image as JPEG
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='JPEG', quality=50)
    img_byte_arr = img_byte_arr.getvalue()

    # Send image for captioning and return the result
    #caption = send_image_for_captioning(img_byte_arr)
    ocr_result= send_image_for_ocr(img_byte_arr)
    print(ocr_result)
    #caption += "\nOCR RESULTS:\n"+ocr_result
    
    results = {}
    
    thread1 = threading.Thread(target=handle_captioning, args=(img_byte_arr, results))
    thread2 = threading.Thread(target=handle_ocr, args=(img_byte_arr, results))

    # Start threads
    thread1.start()
    #time.sleep(2)
    thread2.start()

    # Wait for threads to complete
    thread1.join()
    thread2.join()
    print(results)
    # Combine results and print
    combined_caption = results['caption'] + "\nOCR RESULTS:\n"+ results['ocr']
       
    
    return combined_caption

SERVER_URL = "http://213.173.96.19:5001"  # Replace with your server's IP and port

def synthesize_and_play(text):
    s=time.time()
    # Send the text to the server
    response = requests.post(f"{SERVER_URL}/synthesize", json={"text": text})
    
    if response.status_code == 200:
        filename = response.json()['filename']
        print(f"Audio file generated: {filename}")
        
        # Download the audio file
        audio_response = requests.get(f"{SERVER_URL}/audio/{filename}")
        
        if audio_response.status_code == 200:
            # Load the audio data
            audio_data, sample_rate = sf.read(io.BytesIO(audio_response.content))
            print("Latency:",time.time()-s)
            # Play the audio
            sd.play(audio_data, sample_rate)
            sd.wait()  # Wait until the audio is finished playing
        else:
            print(f"Failed to download audio file. Status code: {audio_response.status_code}")
    else:
        print(f"Failed to synthesize speech. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    while True:
    
        caption = get_caption_from_screenshot()

        synthesize_and_play(caption)
        

