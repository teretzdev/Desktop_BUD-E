from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_together import Together  #pip install langchain-together


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
