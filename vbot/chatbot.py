import os
import streamlit as st
from PIL import Image
from pprint import pprint
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.llms import LlamaCpp, CTransformers
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from config import (
    EMBEDDING,
    PROMPT_TEMPLATE,
    LLM_13B,
    LLM_7B,
    SEARCH_KWARGS,
    SEARCH_TYPE,
    CHUNK_SIZE
)

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=PROMPT_TEMPLATE
)

logo = Image.open('./image/logo.png')

@st.cache_resource()
def retriever(db_path: str):
    # Load Embedding model from local path
    # Load data from FAISS database to front end
    # TODO: Change the EMBEDDING_MODEL to local path
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING)

    vector_db = FAISS.load_local(
        folder_path=db_path,
        embeddings=embeddings,
        normalize_L2=True,
    )

    retriever = vector_db.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs=SEARCH_KWARGS
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
            pprint(doc.metadata)
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
    model_path=LLM_7B,
    temperature=0,
    n_ctx=4000,
    streaming=True,
    max_tokens=512
    # stop=['\n','\n\n']
)

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
model_base = os.path.basename(EMBEDDING)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever(f'./faiss/cs{CHUNK_SIZE}/{model_base}'),
    chain_type_kwargs=chain_type_kwargs
)

# Sidebar
with st.sidebar:
    st.info("""Here are some tips when using the system\n
    1. Please use natural language to ask the bot
    """)

if st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "😊", "ai": "🐱‍👤"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me about VW policy, compliance and everything else!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())

        pprint(f'Start processing query: "{user_query}"')
        response = qa_chain.run(user_query, callbacks=[
                                retrieval_handler, stream_handler])

        pprint(f'Finish generation: {response}')
