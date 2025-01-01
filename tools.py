from typing import Type

from duckduckgo_search import DDGS
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from context_preparator import ContextPreparator
from prompts import *



cp = ContextPreparator()

class WebSearchInput(BaseModel):
    query: str = Field(..., description="web search query to look up")

class InfoWebSearchTool(BaseTool):
    name: str = "info_web_search_tool"
    description: str = "Use this tool when you need to find some information on certain topic."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        return cp.get_context(query)


    def _arun(self, query: str) -> str:
        return self._run(query)

class ImagesWebSearchTool(BaseTool):
    name: str = "images_web_search_tool"
    description: str = "Use this tool when you need to find some images."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        return cp.search_images(query)

    def _arun(self, query: str) -> str:
        return self._run(query)

class VideosWebSearchTool(BaseTool):
    name: str = "videos_web_search_tool"
    description: str = "Use this tool when you need to find some videos."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        return cp.search_videos(query)

    def _arun(self, query: str) -> str:
        return self._run(query)


def generate_prompt(query, custom_system_prompt, **kwargs):
    """
    :param kwargs: Additional arguments for custom_system_prompt formatting. May be 'subject' and/or 'context'
    """
    prompt = ChatPromptTemplate([
        ("system", ROLE_PROMPT),
        ("human", query),
        ("system", custom_system_prompt.format(**kwargs)), # custom prompt that determines what model should do and what it should output
    ]).format_messages(history=history)

    return prompt

# PRODUCTION
def invoke_with_custom_prompt(llm, query, custom_system_prompt):
    prompt = generate_prompt(query, custom_system_prompt)

    print(prompt)

    return llm.invoke(prompt)

# DEBUG
def stream_with_custom_prompt(llm, query, custom_system_prompt):
    prompt = generate_prompt(query, custom_system_prompt)
    # Stream the response from the model
    for chunk in llm.stream(prompt):
        print(chunk.content, end="", flush=True)






if __name__ == '__main__':
    llm = ChatOllama(
        model="cow/gemma2_tools:9b",
        temperature=0.2,
        num_predict=256
    )


    print('Model loaded')




    # history = [
    #     HumanMessage("how to craft stone axe"),
    #     AIMessage("""{"stick": 2, "cobblestone": 3}""")
    # ]
    #
    # stream_with_custom_prompt(llm, query="how does axe look like", history=history, custom_system_prompt=DETERMINE_IF_QUERY_IS_ABOUT_LOOKS_PROMPT)

    history = [
        HumanMessage("what is nether portal"),
        AIMessage("""Nether portal is a building that is used to enter Nether dimension""")
    ]

    res = invoke_with_custom_prompt(llm, query="how to build it",
                              custom_system_prompt=CONSTRUCT_WEB_SEARCH_QUERY_PROMPT)

    print(res)