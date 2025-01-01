from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()


from langgraph.prebuilt import ToolNode, tools_condition
from enum import Enum
from typing import List, Annotated
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START, add_messages
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from prompts import *
from tools import ImagesWebSearchTool, VideosWebSearchTool, InfoWebSearchTool


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

tools = [ImagesWebSearchTool(), VideosWebSearchTool(), InfoWebSearchTool()]
llm = llm.bind_tools(tools)


memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}

def get_history():
    return memory.get(config)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    subject: str
    retrieved_context: str
    retrieved_images: List[str]
    retrieved_videos: List[str]

    web_search_query: str

    output: str


# Nodes
def chatbot(state: State):
    prompt = [("system", ROLE_PROMPT)] + state['messages']

    ai_response = llm.invoke(prompt)

    new_messages = state['messages'] + [ai_response]

    return {**state, 'messages': new_messages}

# def determine_query_subject(state: State):
#     res = invoke_with_custom_prompt(llm, state['query'], get_history(), DETERMINE_QUERY_SUBJECT_PROMPT)
#
#     return {**state, 'subject': res}
#
# def select_node_after_subject_determination(state: State):
#     if state['subject'] == unsuccessful_subject_determination_placeholder:
#         return END
#     else:
#         return 'history'
#
# def get_answer_from_history(state: State):
#     new_state = state.copy()
#     res = invoke_with_custom_prompt(llm, new_state['query'], get_history(), FIND_ANSWER_IN_CHAT_HISTORY_PROMPT)
#
#     answer_is_in_history = (res != answer_does_not_exists_placeholder)
#
#     new_state['answer_is_in_history'] = answer_is_in_history
#
#     if answer_is_in_history:
#         new_state['answer_from_history'] = res
#
#     return new_state
#
# def select_node_after_history(state: State):
#     if state['answer_is_in_history']:
#         return END
#     else:
#         state['web_search_query'] = invoke_with_custom_prompt(llm, state['query'], get_history(), CONSTRUCT_WEB_SEARCH_QUERY_PROMPT)
#         return 'search web'



# def final_answer(state: State):





# Graph compiling
graph_builder = StateGraph(State)

# Nodes
# graph_builder.add_node("determine_query_subject", determine_query_subject)
# graph_builder.add_node("get_answer_from_history", get_answer_from_history)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))



# Edges
# graph_builder.add_edge(START, "determine_query_subject")
# graph_builder.add_conditional_edges(
#     "determine_query_subject",
#     select_node_after_subject_determination,
#     {"history": "get_answer_from_history", END: END},
# )
# graph_builder.add_conditional_edges(
#     "get_answer_from_history",
#     select_node_after_history,
#     {"search web": "tools", END: END},
# )

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")



# Compilation
graph = graph_builder.compile(checkpointer=memory)




if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        res = graph.invoke({'messages': user_input}, config)
        print(res)