DB_PATH_512 = '/faiss/c_512'
DB_PATH_1024 = '/faiss/c_1024'

EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
LLM_13B = "./models/llama-2-13b-chat.ggmlv3.q4_1.bin"
LLM_7B = "./models/llama-2-7b-chat.ggmlv3.q8_0.bin"

# Text chunking and embedding
DIMENSION = 384 # Do not Change
CHUNK_SIZE = 1024 # [64, 128, 256, 512, 1024, 2048]
CHUNK_OVERLAP = 100 # [0, 10, 20, 50, 100, 200]
SEPARATORS = ['\n', '\n\n'] # How the splitter split text, will still try to fill the CHUNK_SIZE requirment

# Retrirver Config
SEARCH_TYPE = 'similarity' # ['similarity', 'mmr', 'similarity_score_threshold']
SEARCH_KWARGS={
    'k': 2, # Amount of documents to return (Default: 4)
    # 'score_threshold': 0.8, # Minimum relevance threshold for similarity_score_threshold
    'fetch_k': 20, # Amount of documents to pass to MMR algorithm (Default: 20)
    'lambda_mult': 0.25, # Diversity of results returned by MMR; 1 for minimum diversity and 0 for maximum. (Default: 0.5)
    # 'filter':{'filter': {'paper_title':'GPT-4 Technical Report'}} # Filter by document metadata
}

PROMPT_TEMPLATE = """Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Context: {context} 
Question: {question} 
Only return the helpful answer below and nothing else. 
Helpful answer: 
"""