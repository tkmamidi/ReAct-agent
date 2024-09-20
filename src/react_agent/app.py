import streamlit as st
from react_agent.graph import graph
from langchain_core.messages import HumanMessage
import os
# import time
import asyncio
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler
# from langfuse.decorators import observe
from react_agent.configuration import Configuration
st.set_page_config(layout="wide")
st.title("CGDS ReAct Agent")
load_dotenv()

langfuse_handler = CallbackHandler()


# @observe()
async def get_stream(prompt):
    return await graph.ainvoke(
        {"messages": [HumanMessage(content=prompt)]},
        # config={"callbacks": Configuration.callbacks},
        config={"callbacks": [langfuse_handler]},
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = asyncio.run(get_stream(prompt))
        response = stream["messages"][-1].content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
