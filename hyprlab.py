import requests
import json
import base64

# URL of the API
url = 'https://api.hyprlab.io/v1/chat/completions'



def send_image_for_captioning_and_ocr_hyprlab_gpt4o (img_byte_arr, API_KEY):
	# Headers for the request
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': f'Bearer {API_KEY}'
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




