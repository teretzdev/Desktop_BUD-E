import subprocess  # For running system commands
import os  # For environment variables and file operations
import signal  # For handling signals (not used in this script, but imported for potential use)
import asyncio  # For asynchronous programming
from dotenv import load_dotenv  # For loading environment variables
import shutil  # For file operations
import requests  # For making HTTP requests
import time  # For time-related functions
import threading
import clipboard
import json
import base64
import io
import threading
from PIL import Image
from PIL import ImageGrab
import shutil  # Import shutil for checking executables

from pynput import keyboard

from threading import Event


import re
import random
import requests
import time
from pyautogui import screenshot
import sounddevice as sd
import soundfile as sf


from api_configs.configs import *

from stream_tts import stream_audio_from_text
from stream_asr import get_transcript
from wake_words import get_wake_words, WakeWordEngine

# Import LangChain components
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_together import Together  #pip install langchain-together
from llm_definition import get_llm
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain



from dl_yt_subtitles import download_youtube_video_info, extract_and_concat_subtitle_text, find_first_youtube_url




llm_config = get_llm_config()

tts_config = get_tts_config()

tts_api = tts_config["default_api"]

tts_model= tts_config["apis"][tts_api]["model"]

tts_api_key= tts_config["apis"][tts_api]["api_key"]

import os
import re
import importlib.util

import importlib.util
from types import ModuleType
import os
import importlib.util
def import_all_functions_from_directory(directory: str) -> dict:
    activated_skills = {}

    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]  # Strip off the .py extension
            filepath = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Iterate over all attributes of the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Check if the attribute is a function
                if callable(attr) and not attr_name.startswith('__'):
                    activated_skills[attr_name] = attr
                    globals()[attr_name] = attr  # Make the function globally accessible
                    
                    print(f"Imported function: {attr_name} from module {module_name}")

    return activated_skills
    


  
def extract_activated_skills_from_directory(directory: str, keyword: str = "KEYWORD ACTIVATED SKILL:") -> dict:
    # Dictionary zum Speichern der Funktionsnamen und zugehörigen Kommentare
    activated_skills = {}

    # Gehe durch alle Dateien im angegebenen Verzeichnis
    for filename in os.listdir(directory):
        # Prüfe, ob es sich um eine Python-Datei handelt
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)

            # Lese den Inhalt der Datei
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Durchsuche die Datei nach Funktionen mit dem entsprechenden Kommentar
            for i in range(len(lines) - 1):
                # Suche nach dem Kommentar in der aktuellen Zeile
                if keyword.lower() in lines[i].lower():  # Falls der Kommentar in Kleinbuchstaben geschrieben ist
                    # Prüfe, ob die nächste Zeile eine Funktionsdefinition ist
                    if re.match(r'^\s*def\s+\w+\s*\(', lines[i + 1]):
                        # Extrahiere den Funktionsnamen
                        function_name = re.findall(r'def\s+(\w+)\s*\(', lines[i + 1])[0]
                        # Extrahiere den Kommentartext nach dem Keyword
                        comment = lines[i].strip().split(keyword)[-1].strip()

                        # Speichere den Funktionsnamen und den Kommentar im Dictionary
                        activated_skills[function_name] = comment

    return activated_skills




def execute_functions_in_order(activated_skills: dict):
    # Sortieren der Funktionsnamen nach numerischer und alphabetischer Reihenfolge
    sorted_function_names = sorted(activated_skills.keys(), key=lambda x: [int(y) if y.isdigit() else y for y in re.split('([0-9]+)', x)])

    for function_name in sorted_function_names:
        print(f"Executing {function_name}...")
        activated_skills[function_name]()

# Beispielaufruf der Funktionen
skills_directory = 'skills'
skills_dict = import_all_functions_from_directory(skills_directory)

#print(get_caption_from_screenshot_gpt4o_hyprlab())

keyword_activated_skills_dict = extract_activated_skills_from_directory(skills_directory, "KEYWORD ACTIVATED SKILL:")    
print(keyword_activated_skills_dict)

lm_activated_skills_dict = extract_activated_skills_from_directory(skills_directory, "LM ACTIVATED SKILL:")    
print(lm_activated_skills_dict)

import sys

def conditional_execution(conditions_list, function_name, input_text):
    """
    Executes a function based on a list of conditions.
    
    Args:
    conditions_list: List of lists of strings. Each inner list contains strings,
                     which all must be present as substrings in the input_text for
                     the specified function to be executed.
    function_name: The name of the function to execute as a string.
    input_text: The text in which to search for the substrings.

    Returns:
    None, executes the specified function if the conditions are met.
    """

    # Try to get the function from the global namespace
    function_to_run = globals().get(function_name)
    
    if function_to_run is None:
        # If not found in globals, try to get it from the current module
        current_module = sys.modules[__name__]
        function_to_run = getattr(current_module, function_name, None)
    
    if function_to_run is None:
        raise ValueError(f"The specified function '{function_name}' is not defined.")
    
    if not callable(function_to_run):
        raise ValueError(f"The function '{function_name}' is not callable.")
    
    # Check each group of conditions in the list of lists.
    for condition in conditions_list:
        # Check if all conditions in the inner list are present in the input_text as substrings.
        if all(substring.lower() in input_text.lower() for substring in condition):
            # Executes the function if the condition is met.
            result = function_to_run()
            return result
            break  # Break the loop after execution to avoid multiple executions.
#print(get_caption_from_clipboard_gpt4o_hyprlab()) 



def parse_list_of_lists(input_str):
    """
    Parses a string representing a list of lists, where each sublist contains strings.
    The function handles irregular spacing and variations in quote usage.
    
    Args:
    input_str (str): A string representation of a list of lists.
    
    Returns:
    list of list of str: The parsed list of lists.
    """
    # Normalize the string by replacing single quotes with double quotes
    normalized_str = re.sub(r"\'", "\"", input_str)

    # Extract the sublists using a regular expression that captures contents inside brackets
    sublist_matches = re.findall(r'\[(.*?)\]', normalized_str)
    
    # Process each match to extract individual string elements
    result = []
    for sublist in sublist_matches:
        # Extract string elements inside the quotes
        strings = re.findall(r'\"(.*?)\"', sublist)
        result.append(strings)

    return result



# print(get_caption_from_screenshot_florence2())



# Load environment variables from .env file
load_dotenv()


# Define LanguageModelProcessor class
class LanguageModelProcessor:
    def __init__(self):
        # Initialize the language model (LLM)
        
        #self.llm =Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1", max_tokens=400, together_api_key=os.getenv("TOGETHER_API_KEY"))#  ChatGroq(temperature=0, model_name="llama3-8b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))
        # Alternatively, use OpenAI models (commented out)
        # self.llm = ChatOpenAI(temperature=0.5, model_name="gpt-4-0125-preview", openai_api_key=os.getenv("OPENAI_API_KEY"))
        # self.llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-0125", openai_api_key=os.getenv("OPENAI_API_KEY"))

        # Determine which language model to use based on the configuration
        
        self.llm= get_llm(llm_config)
        



        # Initialize conversation memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load system prompt from file
        with open('system_prompt.txt', 'r') as file:
            system_prompt = file.read().strip()
        
        # Create chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        # Create conversation chain
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def process(self, text):
        # Add user message to memory
        self.memory.chat_memory.add_user_message(text)

        # Record start time
        start_time = time.time()

        # Get response from LLM
        response = self.conversation.invoke({"text": text})
        
        # Record end time
        end_time = time.time()

        # Add AI response to memory
        self.memory.chat_memory.add_ai_message(response['text'])

        # Calculate elapsed time
        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']

    def get_system_prompt(self):
        # Find the SystemMessagePromptTemplate in the messages
        for message in self.prompt.messages:
            if isinstance(message, SystemMessagePromptTemplate):
                # Return the template string
                return message.prompt.template
        
        # Return None if no SystemMessagePromptTemplate is found
        return None
        
    def update_system_prompt(self, new_prompt):
        # Update the system prompt text
        self.system_prompt = new_prompt

        # Update the prompt template in the conversation chain
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        # Create conversation chain
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )


class TextToSpeech:

    def __init__(self):
        self.player_process = None
        self.should_stop = False
        self.listener = None

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        """Check if a command exists in the system's path"""
        return shutil.which(lib_name) is not None

    def stop(self):
        self.should_stop = True
        if self.player_process:
            self.player_process.terminate()
            self.player_process = None
        if self.listener:
            self.listener.stop()  # Stop the keyboard listener

    def on_activate(self):
        print("Hotkey activated - stopping TTS.")
        self.stop()

    def speak(self, text, stop_event: Event):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        # Setup hotkey listener
        with keyboard.GlobalHotKeys({
                '<ctrl>+<shift>': self.on_activate}) as self.listener:
            player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
            self.player_process = subprocess.Popen(
                player_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            try:
                audio_stream_generator = stream_audio_from_text(text, tts_api_key, tts_model)
                for chunk in audio_stream_generator:
                    if stop_event.is_set() or self.should_stop:
                        break
                    if chunk:
                        try:
                            self.player_process.stdin.write(chunk)
                            self.player_process.stdin.flush()
                        except BrokenPipeError:
                            print("TTS playback stopped.")
                            break
            finally:
                if self.player_process and self.player_process.stdin:
                    self.player_process.stdin.close()
                if self.player_process:
                    self.player_process.wait()
                self.player_process = None




class ConversationManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = LanguageModelProcessor()
        self.tts = TextToSpeech()
        self.stop_event = asyncio.Event()
        self.conversation_active = False

    async def start_conversation(self):
        self.conversation_active = True
        await self.main()

    async def speak_response(self, response):
        tts_task = asyncio.to_thread(self.tts.speak, response, self.stop_event)
        try:
            await tts_task
        except Exception as e:
            print(f"TTS error: {e}")

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        while self.conversation_active:
            self.stop_event.clear()
            self.tts = TextToSpeech()  # Create a new TTS instance for each response
            
            print("Listening for your command...")
            await get_transcript(handle_full_sentence)
            
            if "goodbye" in self.transcription_response.lower():
                self.conversation_active = False
                break


             
            what_buddy_sees = ""

            for keyword_activated_function in keyword_activated_skills_dict:
               
               keyword_activated_skills_dict [keyword_activated_function]
               condition_list = parse_list_of_lists(keyword_activated_skills_dict [keyword_activated_function])
               try:
                 what_buddy_sees += "\n[BUD-E is seeing this: " +  conditional_execution(condition_list, keyword_activated_function, self.transcription_response.lower() )
               except:
                 pass
     

            system_prompt = self.llm.get_system_prompt()
            print(system_prompt)
            #self.llm.update_system_prompt("You are a baby lion.")
            #system_prompt = self.llm.get_system_prompt()
            #print(system_prompt)
            for lm_activated_skill in lm_activated_skills_dict:
               system_prompt += "\n" + lm_activated_skills_dict[lm_activated_skill]
            print(system_prompt)   
            self.llm.update_system_prompt(system_prompt)
                                    
            # system prompt needs to be updated with llm activated skill descriptions
            # with 1. SKILL TITLE , 2. DESCRIPTION , 3. HOW TO TRIGGER IT WITH A FEW EXAMPLES
            # LLM activated skills need to have keywords or other parameters within a tag following the format 
            # <SUPER COOL SKILL> Keywords or other Parameters </SUPER COOL SKILL> 
            # Next the parameters get parsed out and passed to the according function
            
            
            # Process the transcription and generate a response
            llm_response = self.llm.process(self.transcription_response+ what_buddy_sees)   
            
            # Handle URL opening
            extracted_url_to_open = extract_urls_to_open(llm_response)
            if extracted_url_to_open:
                open_site(extracted_url_to_open[0])
                llm_response = random.choice([
                    "Sure! Let me know if there's anything else you need.",
                    "All set! Anything else you'd like to explore?",
                    "The site has been opened! Feel free to ask more questions.",
                    "Done! Can I assist you with anything else today?",
                    "The link is now open! Let me know if you need further assistance."
                ])

            # Handle Ask ORKG
            question_for_askorkg = extract_questions_to_send_to_askorkg(llm_response)
            if question_for_askorkg:
                open_site(f"https://ask.orkg.org/search?query={question_for_askorkg}")
                llm_response = random.choice([
                    "Sure! I will use the Ask Open Knowledge Graph service to analyze the question: {0}",
                    "Got it! Let's see what Ask Open Knowledge Graph has on: {0}",
                    "I'm on it! Checking Ask Open Knowledge Graph for information about: {0}",
                    "Excellent question! I'll consult Ask Open Knowledge Graph about: {0}",
                    "One moment! I'll look that up on Ask Open Knowledge Graph for you about: {0}"
                ]).format(question_for_askorkg)

            # Handle Wikipedia
            question_for_wikipedia = extract_questions_to_send_to_wikipedia(llm_response)
            if question_for_wikipedia:
                open_site(f"https://en.wikipedia.org/w/index.php?search={question_for_wikipedia}")
                llm_response = random.choice([
                    "Sure! Here are the Wikipedia search results for: {0}",
                    "Let me pull up Wikipedia for you to explore: {0}",
                    "Checking Wikipedia for: {0}. Here's what I found!",
                    "I'll search Wikipedia for that. Hold on: {0}",
                    "One moment, I'm getting the information from Wikipedia on: {0}"
                ]).format(question_for_wikipedia)

            print(f"AI: {llm_response}")
            await self.speak_response(llm_response)
            
            self.transcription_response = ""

        print("Conversation ended. Listening for wake words again...")


async def main():
    conversation_manager = ConversationManager()
    wake_words = get_wake_words()
    wake_word_engine = WakeWordEngine(wake_words, conversation_manager.start_conversation)
    wake_word_engine.initialize()
    print("Listening for wake words...")
    await wake_word_engine.detect()

if __name__ == "__main__":
    asyncio.run(main()) 
    
'''
To dos:

- move skills to skills folder
'''
