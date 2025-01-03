from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import ThreadDict

from graph import get_graph, load_memory

import chainlit as cl
import chainlit.data as cl_data

graph = get_graph()
# Correct SQLAlchemy connection string
DATABASE_URL = "sqlite+aiosqlite:///checkpoints.sqlite"  # Ensure this is your correct SQLite database path

# Initialize data layer with proper configuration
cl_data._data_layer = SQLAlchemyDataLayer(
    conninfo=DATABASE_URL,
    ssl_require=False  # SQLite doesn't use SSL; this can be omitted
)

@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    final_answer = cl.Message(content="")

    res = graph.stream({'messages': msg.content}, config=config, stream_mode="updates")

    # print(res)

    for chunk in res:
        if 'chatbot' in chunk:
            last_message = chunk['chatbot']['messages'][-1]
            if last_message.additional_kwargs['final']:
                final_answer.content = last_message.content

    await final_answer.send()


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    cl.user_session.set("chat_history", [])

    # user_session = thread["metadata"]

    for message in thread["steps"]:
        if message["type"] == "user_message":
            cl.user_session.get("chat_history").append({"role": "user", "content": message["output"]})
        elif message["type"] == "assistant_message":
            cl.user_session.get("chat_history").append({"role": "assistant", "content": message["output"]})

import chainlit as cl

@cl.password_auth_callback
def auth():
    return cl.User()
