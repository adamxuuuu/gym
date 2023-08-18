from langchain import LLMChain, PromptTemplate
from langchain.llms import LlamaCpp
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
import os

template = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
Question: {question}

Answer: """
prompt = PromptTemplate(
        template=template,
    input_variables=['question']
)

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

@st.cache_resource
def init_llm(model_path, temperature, top_p, max_length):
    return LlamaCpp(
        model_path=model_path,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_length
        )

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')

    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B-q4', 'Llama2-7B-q8', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B-q4':
        llm = './models/llama-2-7b-chat.ggmlv3.q4_K_M.bin'
    elif selected_model == 'Llama2-7B-q8':
        llm = './models/llama-2-7b-chat.ggmlv3.q8_0.bin'
    else:
        llm = './models/llama-2-13b-chat.ggmlv3.q4_1.bin'
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=2048, value=512, step=8)

    model = init_llm(llm, temperature, top_p, max_length)
    llm_chain = LLMChain(
        prompt=prompt,
        llm=model
    )
    st.info(model.model_path)
    

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            stream_handler = StreamHandler(st.empty())
            response = llm_chain.run(prompt, callbacks=[stream_handler])
            
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)