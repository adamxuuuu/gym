MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
COLLECTION_NAME = 'documentqa'  # Collection name

EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
LLM="LLaMa-7B-GGML/llama-7b.ggmlv3.q4_1.bin"

DIMENSION = 384

# Define search params
SEARCH_PARAMS = {
    "metric_type": "L2", 
    "offset": 5, 
    "ignore_growing": False, 
    "params": {"nprobe": 10}
}

PROMPT_TEMPLATE = """\n\n###Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}###\n
Helpful Answer:"""