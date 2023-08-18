# DB Config
DB_BASE = './faiss_wd/'

# Text Embeddings
EMBEDDING = './models/multi-qa-mpnet-base-cos-v1'       # Slowest
# EMBEDDING = './models/multi-qa-distilbert-cos-v1'     # OK
# EMBEDDING = './models/all-MiniLM-L12-v2'              # Fast
# How the splitter split text, will still try to fill the CHUNK_SIZE requirment
SEPARATORS = '\n{1,}|\-{1,}|\.{1,}'

# LLM Models
LLM_13B = "./models/llama-2-13b-chat.ggmlv3.q4_1.bin"   # Slow

LLM_7B = "./models/llama-2-7b-chat.ggmlv3.q8_0.bin"     # Fast

# Text chunking
CHUNK_SIZE = 2048  # [64, 128, 256, 512, 1024, 2048]
CHUNK_OVERLAP = 0  # [0,  10,  20,  50,  100,  200]

# Retrirver Config
# ['similarity', 'mmr', 'similarity_score_threshold']
SEARCH_TYPE = 'similarity'
SEARCH_KWARGS = {
    # Amount of documents to return (Default: 4)
    'k': 1,
    # 'score_threshold': 0.8,                                       # Minimum relevance threshold for similarity_score_threshold
    # Amount of documents to pass to MMR algorithm (Default: 20)
    'fetch_k': 40,
    # Diversity of results returned by MMR; 1 for minimum diversity and 0 for maximum. (Default: 0.5)
    'lambda_mult': 0.25,
    # 'filter':{'filter': {'paper_title':'GPT-4 Technical Report'}} # Filter by document metadata
}

# Prompt Config
PROMPT_TEMPLATE = """Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Context: {context} 
Question: {question} 
Only return the helpful answer below and nothing else. 
Helpful answer: 
"""
