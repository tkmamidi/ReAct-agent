import streamlit as st
from react_agent.graph import graph
from langchain_core.messages import HumanMessage
import asyncio
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler

st.set_page_config(layout="wide")
load_dotenv()

langfuse_handler = CallbackHandler() # Callback handler for langfuse

st.title("CGDS ReAct Agent")
st.markdown("This is a simple `Re`ason and `Act` chatbot that can answer questions about proteins, drugs, pathways, phenotypes, diseases and their relationships. ")

async def get_stream(prompt):
    """Get the response stream from the agent."""

    return await graph.ainvoke(
        {"messages": [HumanMessage(content=prompt)]},
        config={"callbacks": [langfuse_handler]},
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ask the user for a prompt
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt}) # Save the user's message
    with st.chat_message("user"):
        st.markdown(prompt)

# Get the response from the agent
    with st.chat_message("assistant"):
        stream = asyncio.run(get_stream(prompt))
        response = stream["messages"][-1].content
        st.write(response) # Display the response

    st.session_state.messages.append({"role": "assistant", "content": response}) # Save the assistant's message
