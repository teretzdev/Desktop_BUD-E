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

import json
from pynput import keyboard

from threading import Event


import re
import random
import requests
import time
from pyautogui import screenshot
import sounddevice as sd
import soundfile as sf
import importlib.util
from types import ModuleType

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





llm_config = get_llm_config()

tts_config = get_tts_config()

tts_api = tts_config["default_api"]

tts_model= tts_config["apis"][tts_api]["model"]

tts_api_key= tts_config["apis"][tts_api]["api_key"]


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
def conditional_execution(function_name, transcription_response, conversation, scratch_pad, conditions_list=[], LMGeneratedParameters=""):
    """
    Executes a function based on a list of conditions, passing additional parameters
    and handling return values.

    Args:
    function_name (str): The name of the function to execute.
    transcription_response (str): The current transcription response.
    conversation (object): Current state or context of the conversation.
    scratch_pad (dict): A dictionary to store data across function calls.
    conditions_list (list of list of str): Conditions that trigger the function execution.
    LMGeneratedParameters (str): Additional parameters generated by the language model.

    Returns:
    tuple: A tuple containing updated conversation, scratch_pad, and skill_response from the executed function.
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
    
    if len(conditions_list)>0:
      # Check each group of conditions in the conditions_list.
      for condition in conditions_list:
        # Check if all conditions in the inner list are present in the transcription_response as substrings.
        if all(substring.lower() in transcription_response.lower() for substring in condition):
            # Executes the function if the condition is met.
            skill_response, updated_conversation, updated_scratch_pad = function_to_run(transcription_response, conversation, scratch_pad,  LMGeneratedParameters)
            return skill_response, updated_conversation, updated_scratch_pad
    else:
    
            skill_response, updated_conversation, updated_scratch_pad = function_to_run(transcription_response, conversation, scratch_pad,  LMGeneratedParameters)
            return skill_response, updated_conversation, updated_scratch_pad    
    
    
    
    
    # If no conditions are met, return the unchanged objects and None for skill_response
    return "", conversation, scratch_pad            
            
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
#load_dotenv()



# Define LanguageModelProcessor class
class LanguageModelProcessor:
    def __init__(self):
        # Initialize the language model (LLM)

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


  
def save_scratch_pad_to_file(scratch_pad, filename="ScratchPad.json"):
        """
        Saves the dictionary 'scratch_pad' to a file specified by 'filename'.
        """
        with open(filename, "w") as file:
            json.dump(scratch_pad, file, indent=4)

def load_scratch_pad_from_file(filename="ScratchPad.json"):
        """
        Loads a dictionary from a file specified by 'filename'.
        """
        with open(filename, "r") as file:
            return json.load(file)


def extract_opening_and_closing_tags(input_string):
    """
    Extracts the first opening and closing tags from the input string.

    Args:
    input_string (str): The string to search for tags.

    Returns:
    tuple: A tuple containing the first opening tag and the first closing tag.
    """
    # Regex to find tags
    tags = re.findall(r'<[^>]+>', input_string)
    
    if not tags:
        return None, None  # Return None if no tags are found

    # Find the first opening tag
    opening_tag = next((tag for tag in tags if not tag.startswith('</')), None)
    # Find the first closing tag after the first opening tag
    closing_tag = next((tag for tag in tags if tag.startswith('</') and tag[2:-1] in opening_tag), None)

    return opening_tag, closing_tag




class ConversationManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = LanguageModelProcessor()
        self.tts = TextToSpeech()
        self.stop_event = asyncio.Event()
        self.conversation_active = False
        self.ScratchPad = {}  # scratch pad for skill functions to store persistent variables that can be accessed in consecutive skill calls 

        #save_scratch_pad_to_file(self.ScratchPad )
        try:
          self.ScratchPad = load_scratch_pad_from_file()
        except:
           pass


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


            # system prompt needs to be updated with llm activated skill descriptions
            # with 1. SKILL TITLE , 2. DESCRIPTION , 3. HOW TO TRIGGER IT WITH A FEW EXAMPLES
            # LLM activated skills need to have keywords or other parameters within a tag following the format 
            # <SUPER COOL SKILL> Keywords or other Parameters </SUPER COOL SKILL> 
            # Next the parameters get parsed out and passed to the according function
            '''
            
            Inputs of every skill function are the 

            1) self.transcription_response, 
            2) conversation chain self.llm.conversation, 
            3) the ScratchPad dict & 
            4) a) in case of LM Activated skills: LMGeneratedParameters like keywords or search strings ( the stuff between tags like <SUPER COOL SKILL> Keywords or other Parameters </SUPER COOL SKILL>  ) or 
            4) b) in case of Keyword activated skill: keyword condition_list 

            self.transcription_response, self.llm.conversation, ScratchPad , condition_list

            Reminder:
            
            the Conversation Chain includes the Chat Memory self.memory
            self.llm.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
            )
            
            And the Chat Memory self.memory includes 1) what the User has said so far and 2) what the AI had said so far.
            
            
            Outputs of every skill are the 
            1) updated Conversation Chain self.llm.conversation, 
            2) the updated ScratchPad dict & skill_response, that 
              a) in the case of a Keyword Activated Skill will be a string that gets fed into the LM instead of the self.transcription_response  and that 
              b) in the case of a LM Activated Skill will be the text that gets passed to the TTS.
            '''

             
  
            all_skill_responses=""
            for keyword_activated_function in keyword_activated_skills_dict:
               skill_response=""
               print(keyword_activated_function)
               keyword_activated_skills_dict [keyword_activated_function]
               condition_list = parse_list_of_lists(keyword_activated_skills_dict [keyword_activated_function])
               try:
                 skill_response, updated_conversation, updated_scratch_pad = conditional_execution(keyword_activated_function, self.transcription_response, self.llm.conversation, self.ScratchPad , condition_list )
                 
                 self.llm.conversation= updated_conversation
                 self.ScratchPad= updated_scratch_pad
                 
                 all_skill_responses += "\n" + skill_response
                 
                 
                 
               except:
                  pass
     
            print(self.transcription_response+ all_skill_responses)
            system_prompt = self.llm.get_system_prompt()
            #print(system_prompt)
            
            #self.llm.update_system_prompt("You are a baby lion.")
            #system_prompt = self.llm.get_system_prompt()
            #print(system_prompt)
            
            #loading LM Activated Skills into system prompt
            for lm_activated_skill in lm_activated_skills_dict:
               system_prompt += "\n" + lm_activated_skills_dict[lm_activated_skill]
            #print(system_prompt)   
            self.llm.update_system_prompt(system_prompt)
                                    

            
            # Process the transcription and generate a response
            llm_response = self.llm.process(self.transcription_response+ all_skill_responses)   # the input and the output get added to conversation chain within this function call to the self.llm.memory.chat_memory
            
            print("llm_response", str(llm_response))








            for lm_activated_function in lm_activated_skills_dict:
               skill_response=""
               print(lm_activated_function)
               opening_tag, closing_tag =  extract_opening_and_closing_tags( lm_activated_skills_dict [lm_activated_function] )
               print(opening_tag, closing_tag )
               perform_lm_skill=False
               if (opening_tag and closing_tag and 
                   opening_tag.lower() in llm_response.lower() and 
                   closing_tag.lower() in llm_response.lower()):  
                 perform_lm_skill=True
                 opening_tag_name = re.escape(opening_tag[1:-1])
                 closing_tag_name = re.escape(closing_tag[2:-1])

                 # Define a regular expression pattern dynamically based on opening_tag and closing_tag
                 pattern = rf"<{opening_tag_name}>(.*?)</{closing_tag_name}>"

                 # Use re.findall to extract all occurrences of the pattern
                 LMGeneratedParameters  = re.findall(pattern, llm_response) 
                 LMGeneratedParameters = LMGeneratedParameters[0]
                 print("LMGeneratedParameters", LMGeneratedParameters)
               
                 try:
                   skill_response, updated_conversation, updated_scratch_pad = conditional_execution(lm_activated_function, self.transcription_response, self.llm.conversation, self.ScratchPad , [], LMGeneratedParameters )
                   #print("skill_response",skill_response ) 
                   self.llm.conversation= updated_conversation
                   self.ScratchPad= updated_scratch_pad
                 

                   self.llm.conversation= updated_conversation
                   self.ScratchPad= updated_scratch_pad
                 
                 
                   break # allow only 1 LM activated function to get executed, otherwise it got get confusing
                 
                 
                 
                 except:
                    pass
     

            if perform_lm_skill:
               print(f"AI: {skill_response}")
               await self.speak_response(skill_response)
            else:
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
   
   
