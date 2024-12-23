from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from prompts import *


def generate_prompt(query, history, custom_system_prompt, **kwargs):
    """
    :param kwargs: Additional arguments for custom_system_prompt formatting. May be 'subject' and/or 'context'
    """
    prompt = ChatPromptTemplate([
        ("system", ROLE_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", query),
        ("system", custom_system_prompt.format(**kwargs)), # custom prompt that determines what model should do and what it should output
    ]).format_messages(history=history)

    return prompt

# PRODUCTION
def invoke_with_custom_prompt(llm, query, history, custom_system_prompt):
    prompt = generate_prompt(query, history, custom_system_prompt)

    return llm.invoke(prompt)

# DEBUG
def stream_with_custom_prompt(llm, query, history, custom_system_prompt):
    prompt = generate_prompt(query, history, custom_system_prompt)
    # Stream the response from the model
    for chunk in llm.stream(prompt):
        print(chunk.content, end="", flush=True)






if __name__ == '__main__':
    llm = ChatOllama(
        model="gemma2:9b",
        temperature=0.2,
        num_predict=256
    )

    print('Model loaded')

    history = [
        HumanMessage("how to craft stone axe"),
        AIMessage("""{"stick": 2, "cobblestone": 3}""")
    ]

    stream_with_custom_prompt(llm, query="how does axe look like", history=history, custom_system_prompt=DETERMINE_IF_QUERY_IS_ABOUT_LOOKS_PROMPT)
