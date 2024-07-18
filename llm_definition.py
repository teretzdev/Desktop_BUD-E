from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_together import Together  #pip install langchain-together

from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
import time 

# Import configurations from a local module
from api_configs.configs import get_llm_config, get_tts_config, get_asr_config

# Get configuration for the language model
llm_config = get_llm_config()


def get_llm(llm_config):
        model_type = llm_config['default_model']

        if model_type == "together":
            # Using the TogetherAI model
            model_config = llm_config['models'][model_type]
            llm = Together(model=model_config["model"], max_tokens=model_config["max_tokens"], together_api_key=model_config["api_key"])
        elif model_type == "groq":
            # Using the Groq model
            model_config = llm_config['models'][model_type]
            llm = ChatGroq(temperature=model_config["temperature"], model_name=model_config["model_name"], groq_api_key=model_config["api_key"])
        elif model_type.startswith("openai"):
            # Using one of the OpenAI models
            model_config = llm_config['models'][model_type]
            llm = ChatOpenAI(temperature=model_config["temperature"], model_name=model_config["model_name"], openai_api_key=model_config["api_key"])
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        return llm
        
        
        
        
# Define LanguageModelProcessor class
class LanguageModelProcessor:
    def __init__(self,llm_config=llm_config):
        # Initialize the language model (LLM) using a configuration
        self.llm = get_llm(llm_config)

        # Initialize conversation memory to store chat history
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load system prompt from a file
        with open('system_prompt.txt', 'r') as file:
            system_prompt = file.read().strip()
        
        # Create a chat prompt template with system message, chat history, and user input
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        # Create a conversation chain combining the LLM, prompt, and memory
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def process(self, text):
        # Add user message to memory
        self.memory.chat_memory.add_user_message(text)

        # Record start time for performance measurement
        start_time = time.time()

        # Get response from LLM
        response = self.conversation.invoke({"text": text})
        
        # Record end time
        end_time = time.time()

        # Add AI response to memory
        self.memory.chat_memory.add_ai_message(response['text'])

        # Calculate and print elapsed time
        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']

    def llm_call_without_memory(self, text):

        # Get response from LLM
        response = self.conversation.invoke({"text": text})
    
        return response['text']

    def get_system_prompt(self):
        # Find and return the SystemMessagePromptTemplate from the prompt messages
        for message in self.prompt.messages:
            if isinstance(message, SystemMessagePromptTemplate):
                return message.prompt.template
        return None
        
    def update_system_prompt(self, new_prompt):
        # Update the system prompt with a new one
        self.system_prompt = new_prompt

        # Recreate the prompt template with the new system prompt
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        # Recreate the conversation chain with the updated prompt
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

        
