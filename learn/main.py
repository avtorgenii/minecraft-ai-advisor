from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver



class State(TypedDict):
    messages: Annotated[list, add_messages]



llm = ChatOpenAI(
    model='gpt-3.5-turbo-1106',
    max_tokens=100,
    temperature=0.2,
)


tool = TavilySearchResults(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

memory = MemorySaver() # for persistence should be declared once, like in jupyter notebook. In production replace with PostgresSaver
graph = graph_builder.compile(checkpointer=memory, interrupt_before=["tools"])

config = {"configurable": {"thread_id": "2"}}

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": ["user", user_input]}, config, stream_mode="values"):
        event["messages"][-1].pretty_print()


if __name__ == '__main__':
    # snapshot = graph.get_state(config)
    # print(snapshot)

    # while True:
    #     try:
    #         user_input = input("> ")
    #         if user_input.lower() in ["quit", "exit", "q"]:
    #             print("Goodbye!")
    #             break
    #
    #         stream_graph_updates(user_input)
    #         snapshot = graph.get_state(config)
    #         print(snapshot.next)
    #     except:
    #         user_input = "What do you know about LangGraph?"
    #         print("User: " + user_input)
    #         stream_graph_updates(user_input)
    #         break

    user_input = "I'm learning LangGraph. Could you do some research on it for me?"
    config = {"configurable": {"thread_id": "1"}}
    events = graph.stream({"messages": [("user", user_input)]}, config)
    for event in events:
        print(event)

    snapshot = graph.get_state(config)
    existing_message = snapshot.values["messages"][-1]
    existing_message.pretty_print()