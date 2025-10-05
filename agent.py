from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
import classes as cls
import graph as grp
import pickle

def init_prompt() -> ChatPromptTemplate:
    system_message = open("prompt.md", "r").read()
    user_prompt = "Question: {question}"

    return ChatPromptTemplate(
        [("system", system_message), ("user", user_prompt)]
    )

def init_llm(model: str) -> ChatOllama:
    # DeepSeek models like DeepSeek-R1 or V3 are generally better for complex reasoning
    # and multi-step analysis, making them more suitable for providing detailed positional insights.
    # Llama models are better for general language tasks and offer speed and flexibility but 
    # lack the depth for complex reasoning required in detailed chess analysis.

    # return ChatOllama(model="llama3.1")
    # return ChatOllama(model="deepseek-r1:8b")
    return ChatOllama(model=model)

def init_db() -> SQLDatabase:
    db = SQLDatabase.from_uri("sqlite:///database.sqlite")
    db._sample_rows_in_table_info = 0
    return db

def init_state(prompt: ChatPromptTemplate, llm: ChatOllama, db: SQLDatabase) -> cls.State:
    with open("model.pkl", "rb") as pklfile:
        rf = pickle.load(pklfile)

        return cls.State(
            prompt_template = prompt,
            llm = llm,
            limit = 50000,
            question = "",
            query = "",
            result = "",
            answer = "",
            count = 0,
            database = db,
            model = rf
        )