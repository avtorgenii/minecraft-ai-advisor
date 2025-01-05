import json

from dotenv import load_dotenv
load_dotenv()


from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START, add_messages
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from prompts import *
from tools import unified_search_tool

# import sqlite3
# from langgraph.checkpoint.sqlite import SqliteSaver


# Necessary definitions
llm = ChatOllama(
    model = "llama3-groq-tool-use",
    temperature = 0,
    num_predict = 600
)

# llm = ChatOpenAI(
#     model='gpt-3.5-turbo-1106',
#     max_tokens=100,
#     temperature=0.2,
# )

tools = [unified_search_tool]
llm = llm.bind_tools(tools)





class State(TypedDict):
    messages: Annotated[list, add_messages]


# Nodes
def chatbot(state: State):
    prompt = [("system", ROLE_PROMPT)] + state['messages']

    ai_response = llm.invoke(prompt)

    if len(ai_response.tool_calls) > 0:
        ai_response.additional_kwargs['final'] = False
    else:
        ai_response.additional_kwargs['final'] = True

    new_messages = state['messages'] + [ai_response]

    return {**state, 'messages': new_messages}


# Graph compiling
graph_builder = StateGraph(State)

# Nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))



# Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)



# Memory
# def load_memory():
#     conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
#     return SqliteSaver(conn)

def load_memory():
    return MemorySaver()

# Compilation
def get_graph():
    return graph_builder.compile(checkpointer=load_memory())


# what is blood altar
# how does blood altar look like
# give me a tutorial on how to build tier 4 blood altar


if __name__ == '__main__':
    graph = get_graph()
    config = {"configurable": {"thread_id": 1}}

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        res = graph.stream({'messages': user_input}, config=config, stream_mode="updates")

        # print(res)

        for chunk in res:
            if 'chatbot' in chunk:
                last_message = chunk['chatbot']['messages'][-1]
                if last_message.additional_kwargs['final']:
                    print(last_message)
            elif 'tools' in chunk:
                print(chunk)
                images = json.loads(chunk['tools']['messages'][0].content).get('images', [])
                videos = json.loads(chunk['tools']['messages'][0].content).get('videos', [])
                print(images)