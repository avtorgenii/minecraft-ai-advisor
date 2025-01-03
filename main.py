import json

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from torch.fx.experimental.unification.dispatch import dispatch

from graph import get_graph, load_memory

import chainlit as cl
import chainlit.data as cl_data


graph = get_graph()

# # Correct SQLAlchemy connection string
# DATABASE_URL = "sqlite+aiosqlite:///checkpoints.sqlite"  # Ensure this is your correct SQLite database path
#
# # Initialize data layer with proper configuration
# cl_data._data_layer = SQLAlchemyDataLayer(
#     conninfo=DATABASE_URL,
#     ssl_require=False  # SQLite doesn't use SSL; this can be omitted
# )



@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="What is blood altar?",
            message="What is blood altar?",
            icon="/public/write.svg",
        ),

        cl.Starter(
            label="How does a quarry look like in BuildCraft?",
            message="How does a quarry look like in BuildCraft?",
            icon="/public/image.svg",
        ),
        cl.Starter(
            label="Find a video tutorial on how to summon Asorah the Fallen.",
            message="Find a video tutorial on how to summon Asorah the Fallen.",
            icon="/public/video.svg",
        )
    ]


@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    final_answer = cl.Message(content="")

    res = graph.stream({'messages': msg.content}, config=config, stream_mode="updates")

    for chunk in res:
        if 'chatbot' in chunk:
            last_message = chunk['chatbot']['messages'][-1]
            if last_message.additional_kwargs['final']:
                final_answer.content = last_message.content
        elif 'tools' in chunk:
            images = json.loads(chunk['tools']['messages'][0].content).get('images', [])
            videos = json.loads(chunk['tools']['messages'][0].content).get('videos', [])

            elements = []


            for image in images:
                elements.append(cl.Image(url=image, display="inline"))
            for video in videos:
                elements.append(cl.Video(url=video, size='large'))

            final_answer.elements = elements



    await final_answer.send()



# @cl.on_chat_resume
# async def on_chat_resume(thread: ThreadDict):
#     cl.user_session.set("chat_history", [])
#
#     # user_session = thread["metadata"]
#
#     for message in thread["steps"]:
#         if message["type"] == "user_message":
#             cl.user_session.get("chat_history").append({"role": "user", "content": message["output"]})
#         elif message["type"] == "assistant_message":
#             cl.user_session.get("chat_history").append({"role": "assistant", "content": message["output"]})
#
# import chainlit as cl
#
# @cl.password_auth_callback
# def auth():
#     return cl.User()
