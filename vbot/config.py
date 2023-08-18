# DB Config
DB_BASE = '/workspace/gym/vbot/faiss'

# Text Embeddings
EMBEDDING = './models/multi-qa-mpnet-base-cos-v1'       # Slowest
# EMBEDDING = './models/multi-qa-distilbert-cos-v1'     # OK
# EMBEDDING = './models/all-MiniLM-L12-v2'              # Fast
SEPARATORS = '\n{1,}'       #   How the splitter split text, will still try to fill the CHUNK_SIZE requirment

# LLM Models
LLM_13B = "/workspace/gym/vbot/models/llama-2-13b-chat.ggmlv3.q4_1.bin"   # Slow
LLM_7B = "/workspace/gym/vbot/models/llama-2-7b-chat.ggmlv3.q8_0.bin"     # Fast

# Text chunking
CHUNK_SIZE = 2048           #  [64, 128, 256, 512, 1024, 2048]
CHUNK_OVERLAP = 0           #  [0,  10,  20,  50,  100,  200]

# Retrirver Config
SEARCH_TYPE = 'similarity'                                          # ['similarity', 'mmr', 'similarity_score_threshold']
SEARCH_KWARGS={
    'k': 2,                                                         # Amount of documents to return (Default: 4)
    # 'score_threshold': 0.8,                                       # Minimum relevance threshold for similarity_score_threshold
    'fetch_k': 40,                                                  # Amount of documents to pass to MMR algorithm (Default: 20)
    'lambda_mult': 0.25,                                            # Diversity of results returned by MMR; 1 for minimum diversity and 0 for maximum. (Default: 0.5)
    # 'filter':{'filter': {'paper_title':'GPT-4 Technical Report'}} # Filter by document metadata
}

# Prompt Config
PROMPT_TEMPLATE = """Answer the question based on the context below. If the
question cannot be answered using the information provided answer with "I don't know".

Context: {context} 

Question: {question} 

Answer: """
