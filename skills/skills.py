import clipboard
import json

from PIL import Image
from PIL import ImageGrab

from pynput import keyboard
import threading

from pyautogui import screenshot
import io
import requests
import json
import base64
import os
import re
import subprocess
import time 

from florence2 import handle_captioning_florence2
from florence2 import handle_ocr_florence2
from florence2 import send_image_for_captioning_florence2
from florence2 import send_image_for_ocr_florence2

from hyprlab import send_image_for_captioning_and_ocr_hyprlab_gpt4o

# URL of the API
url = 'https://api.hyprlab.io/v1/chat/completions'
HYPRLAB_API_KEY = "hypr-lab-dhItb5DFQctQvafMzqgKT3BlbkFJfot58G96B2VMaS4u0015" # os.getenv("HYPRLAB_API_KEY")

florence2_server_url = "http://213.173.96.19:5002/" 



def send_image_for_captioning_and_ocr_hyprlab_gpt4o (img_byte_arr):
	
	#print(HYPRLAB_API_KEY)
	# Headers for the request
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': f'Bearer {HYPRLAB_API_KEY}'
	}

	encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

	# Data to be sent
	data = {
	    "model": "gpt-4o",
	    "messages": [
		{
		    "role": "system",
		    "content": "You are ChatGPT, a large language model trained by OpenAI.\nCarefully heed the user's instructions.\nRespond using Markdown"
		},
		{
		    "role": "user",
		    "content": [
		        {
		            "type": "text",
		            "text": "Describe this image with many details including texts, equations, diagrams & tables. Describe what can be seen with many details and explain what can be seen where. If there is any excercise or problem in it, provide a brief, correct solution."
		        },
		        {
		            "type": "image_url",
		            "image_url": {
		                "url": f"data:image/jpeg;base64,{encoded_image}",
		                "detail": "high"
		            }
		        }
		    ]
		}
	    ]
	}

	# Send request and receive response
	response = requests.post(url, headers=headers, json=data)
       
	# Output response
	print(response.status_code)
	print(response.text)
	response_dict = json.loads(response.text)
	
	return response_dict["choices"][0]["message"]["content"]




# KEYWORD ACTIVATED SKILL:[ ["have a look"], [ "buddy look"], ["look buddy"], ["buddy, look" ], ["look, buddy" ]  ]
def get_caption_from_clipboard_gpt4o_hyprlab():
    # Check clipboard content

    try:
       content = ImageGrab.grabclipboard()
    except:
        content = clipboard.paste()
        print(type(content))
        if isinstance(content, str):
            if "https://www.youtu" in content and len(content)<100:
                video_metadata= download_youtube_video_info(find_first_youtube_url(content))
                subtitle_text= extract_and_concat_subtitle_text(str(video_metadata))
                print(subtitle_text)
                print(len(subtitle_text))
                return subtitle_text [:6000] 
                
            else:
              print("Returning text from the clipboard...")
              return content
    print(content)
    print(type(content))
    
    if isinstance(content, Image.Image):
        print("Processing an image from the clipboard...")
        if content.mode != 'RGB':
            content = content.convert('RGB')
            
        # Save image to a byte array
        img_byte_arr = io.BytesIO()
        content.save(img_byte_arr, format='JPEG', quality=60)
        img_byte_arr = img_byte_arr.getvalue()


        # Send image for captioning and return the result
        combined_caption = send_image_for_captioning_and_ocr_hyprlab_gpt4o(img_byte_arr)

        print(combined_caption)
   
  
        return combined_caption

    else:
        return "No image or text data found in the clipboard."

# Functions `handle_captioning` and `handle_ocr` need to be defined elsewhere in your code.
# They should update the `results` dictionary with keys 'caption' and 'ocr' respectively.

# KEYWORD ACTIVATED SKILL:[ ["have a look", "screen"], [ "buddy look at the screen"], ["look buddy at the screen"], ["buddy, look at the screen" ], ["look, buddy" , "screenshot"]  ]
def get_caption_from_screenshot_gpt4o_hyprlab():


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
    resized_image.save(img_byte_arr, format='JPEG', quality=70)
    screenshot_image.save(img_byte_arr, format='JPEG', quality=70)
    img_byte_arr = img_byte_arr.getvalue()

    # Send image for captioning and return the result
    combined_caption = send_image_for_captioning_and_ocr_hyprlab_gpt4o(img_byte_arr)

    print(combined_caption)
   
  
    return combined_caption


# KEYWORD ACTIVATED SKILL:[ ["have a look", "florence"], [ "buddy look", "florence"], ["look buddy at the screen", "florence"], ["buddy, look at the screen", "florence" ], ["look, buddy" , "screenshot", "florence"]  ]
def get_caption_from_screenshot_florence2():
    # Take a screenshot and open it with PIL
    print("Taking a screenshot...")
    screenshot_image = screenshot()  # Uses PyAutoGUI to take a screenshot
    #width, height = screenshot_image.size
    #new_height = 800
    #new_width = int((new_height / height) * width)
    
    # Resizing with the correct resampling filter
    #resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save the resized image as JPEG
    img_byte_arr = io.BytesIO()
    #resized_image.save(img_byte_arr, format='JPEG', quality=60)
    screenshot_image.save(img_byte_arr, format='JPEG', quality=60)
    img_byte_arr = img_byte_arr.getvalue()

    # Send image for captioning and return the result
    #caption = send_image_for_captioning(img_byte_arr)
    #ocr_result= send_image_for_ocr(img_byte_arr)
    #print(ocr_result)
    #caption += "\nOCR RESULTS:\n"+ocr_result
    
    results = {}
    
    thread1 = threading.Thread(target=handle_captioning_florence2, args=(img_byte_arr, results))
    thread2 = threading.Thread(target=handle_ocr_florence2, args=(img_byte_arr, results))

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








def get_caption_from_clipboard_florence2():
    # Check clipboard content

    try:
       content = ImageGrab.grabclipboard()
    except:
        content = clipboard.paste()
        print(type(content))
        if isinstance(content, str):
            print("Returning text from the clipboard...")
            return content
    print(content)
    print(type(content))
    
    if isinstance(content, Image.Image):
        print("Processing an image from the clipboard...")
        if content.mode != 'RGB':
            content = content.convert('RGB')
            
        # Save image to a byte array
        img_byte_arr = io.BytesIO()
        content.save(img_byte_arr, format='JPEG', quality=60)
        img_byte_arr = img_byte_arr.getvalue()

        results = {}
        
        # Define tasks for threads
        thread1 = threading.Thread(target=handle_captioning_florence2, args=(img_byte_arr, results))
        thread2 = threading.Thread(target=handle_ocr_florence2, args=(img_byte_arr, results))

        # Start threads
        thread1.start()
        thread2.start()

        # Wait for threads to complete
        thread1.join()
        thread2.join()

        # Combine results and return
        combined_caption = results.get('caption', '') + "\nOCR RESULTS:\n" + results.get('ocr', '')
        return combined_caption

    else:
        return "No image or text data found in the clipboard."






def open_site(url):
    # Use subprocess.Popen to open the browser
    process = subprocess.Popen(['xdg-open', url])
    
    # Wait for 2 seconds
    time.sleep(1)
    
    # Kill the process
    process.terminate()  # Safely terminate the process
    # If terminate doesn't kill the process, you can use kill():
    # process.kill()
    
def extract_urls_to_open(input_string):
    # Define a regular expression pattern to find URLs within <open-url> tags
    pattern = r"<open-url>(https?://[^<]+)</open-url>"
    
    # Use re.findall to extract all occurrences of the pattern
    urls = re.findall(pattern, input_string)
    
    return urls

# LM ACTIVATED SKILL: SKILL TITLE: Review scientific literature. DESCRIPTION: Sends a question to the Ask Open Research Knowledge Graph Service that retrieves relevant abstracts from 76+ million scientific papers. USAGE INSTRUCTIONS: Whenever the user asks you to review the scientific literature for a certain question, you reply with the question inside the tags <open-askorkg> ... </open-askorkg>, like e.g. if the user asks you to review the scientific literature for the question 'Is it possible to cure aging?', you output only: <open-askorkg>Is it possible to cure aging?</open-askorkg> and nothing more.
def extract_questions_to_send_to_askorkg(input_string):
    # Define a regular expression pattern to find content within <open-askorkg>...</open-orkg> tags
    pattern = r"<open-askorkg>(.*?)</open-askorkg>"
    
    # Use re.findall to extract all occurrences of the pattern
    contents = re.findall(pattern, input_string)
    
    # Return the content of the first tag pair, or None if there are no matches
    return contents[0] if contents else None

# LM ACTIVATED SKILL: bla
def extract_questions_to_send_to_wikipedia(input_string):
    # Define a regular expression pattern to find content within <open-askorkg>...</open-orkg> tags
    pattern = r"<open-wikipedia>(.*?)</open-wikipedia>"
    
    # Use re.findall to extract all occurrences of the pattern
    contents = re.findall(pattern, input_string)
    
    # Return the content of the first tag pair, or None if there are no matches
    return contents[0] if contents else None
    

