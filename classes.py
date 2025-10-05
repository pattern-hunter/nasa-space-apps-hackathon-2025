from typing_extensions import Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_ollama.chat_models import ChatOllama
from sklearn.ensemble import RandomForestClassifier
from typing import List

class State(TypedDict):
    prompt_template: ChatPromptTemplate
    llm: ChatOllama 
    question: str
    result: str
    answer: str
    count: int
    query: str
    database: SQLDatabase
    model: RandomForestClassifier
    prediction_data: List[float]

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]