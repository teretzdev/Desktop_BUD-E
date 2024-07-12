import subprocess
import time

def open_site(url):
    # Use subprocess.Popen to open the browser
    process = subprocess.Popen(['xdg-open', url])
    
    # Wait for 2 seconds
    time.sleep(1)
    
    # Kill the process
    process.terminate()  # Safely terminate the process
    # If terminate doesn't kill the process, you can use kill():
    # process.kill()

open_site("https://en.wikipedia.org/w/index.php?search=laion ai")
time.sleep(4)
open_site("https://en.wikipedia.org/w/index.php?search=peter puter")

time.sleep(4)
open_site("https://ask.orkg.org/search?query=are%20peanuts%20healthy?")

time.sleep(4)
open_site("https://www.google.com/search?q=math")


time.sleep(4)
open_site("https://www.youtube.com/results?search_query=trigonometry+for+dummies")
