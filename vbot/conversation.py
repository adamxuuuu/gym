from langchain.llms import LlamaCpp
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory


llm = LlamaCpp(
    model_path="/workspace/gym/vbot/models/LLaMa-7B-GGML/llama-7b.ggmlv3.q4_1.bin",
    temperature=0.8,
    n_ctx = 2048,
    streaming = True,
    stop=[]
)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

msgs = StreamlitChatMessageHistory()

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?"),
    
avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        response = llm(user_query, callbacks=[stream_handler])