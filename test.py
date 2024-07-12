import requests
from bs4 import BeautifulSoup
import re

def extract_questions_to_send_to_wikipedia(input_string):
    # Define a regular expression pattern to find content within <open-wikipedia>...</open-wikipedia> tags
    pattern = r"<open-wikipedia>(.*?)</open-wikipedia>"
    
    # Use re.findall to extract all occurrences of the pattern
    queries = re.findall(pattern, input_string)
    
    if not queries:
        return None

    # Set to store unique Wikipedia URLs without duplicates
    wikipedia_urls = set()

    # Send a request to Wikipedia for each extracted query
    for query in queries:
        # URL encoding the query
        url_encoded_query = requests.utils.quote(query)
        
        # Sending request to Wikipedia's search page
        response = requests.get(f"https://en.wikipedia.org/w/index.php?search={url_encoded_query}")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parsing the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting all <a> tags with href attribute containing '/wiki/'
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                # Check if the link is a valid Wikipedia article link, does not contain ':', and is not the main page
                if '/wiki/' in href and ':' not in href and "Main_Page" not in href:
                    full_url = f"https://en.wikipedia.org{href}"
                    wikipedia_urls.add(full_url)  # Adding to a set automatically deduplicates

    # Convert the set back to a list before returning
    return list(wikipedia_urls)

# Example usage
input_string = "Some text <open-wikipedia>Python, programming</open-wikipedia> more text."
result = extract_questions_to_send_to_wikipedia(input_string)
print(result)




import requests
import time
from bs4 import BeautifulSoup

def fetch_and_clean_wikipedia_pages(url_list):
    # Check if the list has at least 5 URLs, if not, use the length of the list
    num_urls = min(5, len(url_list))
    
    # Process each of the first 5 URLs
    for url in url_list[:num_urls]:
        # Send a request to the URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content and remove all script and style elements
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(["script", "style"]):  # remove all script and style elements
                script_or_style.decompose()
            
            # Get text and clean it up
            text = soup.get_text()
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk).split("From Wikipedia, the free encyclopedia")[1]
            
            # Print the first 1000 characters of the cleaned text
            print(text[:2000])
        
        # Sleep for 0.1 seconds before the next request
        time.sleep(0.05)

# Example usage
url_list = result
fetch_and_clean_wikipedia_pages(url_list)
