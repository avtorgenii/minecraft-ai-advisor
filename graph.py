from dotenv import load_dotenv
load_dotenv()


from langgraph.prebuilt import ToolNode, tools_condition
from typing import List, Annotated
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START, add_messages
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from prompts import *
from tools import unified_search_tool


# Necessary definitions
# Should be passed to graph as a parameter and defined somewhere in main.py
llm = ChatOllama(
    model = "llama3-groq-tool-use",
    temperature = 0.2,
    num_predict = 256
)

# llm = ChatOpenAI(
#     model='gpt-3.5-turbo-1106',
#     max_tokens=100,
#     temperature=0.2,
# )

tools = [unified_search_tool]
llm = llm.bind_tools(tools)


memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}

def get_history():
    return memory.get(config)


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Nodes
def chatbot(state: State):
    prompt = [("system", ROLE_PROMPT)] + state['messages']

    ai_response = llm.invoke(prompt)

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



# Compilation
graph = graph_builder.compile(checkpointer=memory)


# what is blood altar
# how does blood altar look like
# give me a tutorial on how to build tier 4 blood altar


if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        user_input += ". Please use tool when user asks you about info, looks/images or videos of something."
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        res = graph.invoke({'messages': user_input}, config)['messages'][-1]
        print(res)