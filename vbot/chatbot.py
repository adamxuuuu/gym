import os
import streamlit as st
from PIL import Image
from pprint import pprint
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.llms import LlamaCpp
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from config import (
    SEARCH_PARAMS,
    EMBEDDING_MODEL,
    PROMPT_TEMPLATE
)

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=PROMPT_TEMPLATE
)

logo = Image.open('./image/logo.png')

# Define retriever


@st.cache_resource()
def retriever():
    # Load Embedding model from local path
    # Load data from FAISS database to front end
    # TODO: Change the EMBEDDING_MODEL to local path
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vector_db = FAISS.load_local(
        './faiss',
        embeddings
    )

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 2, 'lambda_mult': 0.25}
    )

    return retriever


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container.expander("Context Retrieval")

    # def on_retriever_start(self, query: str, **kwargs):
    #     self.container.write(f"**Question:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        # self.container.write(documents)
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.container.write(f"**Document {idx} from {source}**")
            self.container.markdown(doc.page_content)


# ======================APP==========================
st.image(logo)
st.title('VW ITP Bot')

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
# memory = ConversationBufferMemory(
#     memory_key="chat_history", chat_memory=msgs, return_messages=True)

# TODO: Change the following code to RESTful and call the endpoint /v1/completion
llm = LlamaCpp(
    model_path="/workspace/gym/vbot/models/LLaMa-7B-GGML/llama-7b.ggmlv3.q4_1.bin",
    temperature=0,
    n_ctx=2048,
    streaming=True,
    # stop=['\n','\n\n','###']
)

# openai_api_key = "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"
# llm = ChatOpenAI(
#     model_name="gpt-3.5-turbo",
#     openai_api_key=openai_api_key,
#     temperature=0,
#     max_tokens=256,
#     model_kwargs={'presence_penalty': 1,
#                   'frequency_penalty': 1,
#                   'stop': ['\n', '\n\n', '###']},
#     streaming=True
# )

chain_type_kwargs = {"prompt": PROMPT}
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever(),
    chain_type_kwargs=chain_type_kwargs
)

# Sidebar
if st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me about VW policy, compliance and everything else!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())

        print(f'Start processing query: {user_query}')
        response = qa_chain.run(user_query, callbacks=[
                                retrieval_handler, stream_handler])

        pprint(response)
