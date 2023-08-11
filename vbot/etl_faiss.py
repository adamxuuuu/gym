import os
from tqdm import tqdm
import pprint

from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from config import (
    DIMENSION,
    EMBEDDING_MODEL
)


embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
# Get all the text files in the text directory
docs = []
po_path = './data/policies'
def load_from_dir(dir_path):
    for file in tqdm(os.listdir(dir_path)):
        doc = load_single(os.path.join(dir_path, file))
        if doc:
            docs.extend(doc)
    return docs

def load_single(file_path):
    try:
        loader = UnstructuredFileLoader(file_path)
        docs = loader.load()
        chunks = text_splitter.split_documents(docs)
        return chunks
    except Exception as e:
        print(file_path, end='')

def _file_name(path):
    return os.path.basename(path).replace('_', ' ')

def save_local():
    print(f'Extract and Transform documents from {po_path}...')
    policies = load_from_dir(po_path)
    print(f'Embedding document chunks...')
    vector_db = FAISS.from_documents(
        policies,
        embeddings
    )
    vector_db.save_local('./faiss')

if __name__ == '__main__':
    # save_local()
    vector_db = FAISS.load_local('./faiss', embeddings)
    hits = vector_db.search('environment friendly policy', search_type='mmr', k=5)
    pprint.pprint(hits)