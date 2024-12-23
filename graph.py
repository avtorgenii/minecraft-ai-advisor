from enum import Enum

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph, START
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama

# Should be passed to graph as a parameter and defined somewhere in main.py
llm = ChatOllama(
    model = "gemma2:9b",
    temperature = 0.2,
    num_predict = 256
)

class Topic(Enum):
    LOOKS: 1
    CRAFT: 2
    BUILD: 3
    SUMMON: 4
    GENERAL_INFO: 5


class GraphState(TypedDict):
    chat_history: ChatPromptTemplate
    query: str
    subject: str
    topic: Topic