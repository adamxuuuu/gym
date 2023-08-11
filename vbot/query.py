from pymilvus import Collection, connections
from langchain.embeddings import HuggingFaceEmbeddings

from config import (
    SEARCH_PARAMS,
    MILVUS_HOST,
    MILVUS_PORT,
    COLLECTION_NAME,
    EMBEDDING_MODEL
)


def search_with_string(embeddings, collection, query='ID'):
    return collection.search(
        data=[embeddings.embed_query(query)],
        anns_field="embedding",
        param=SEARCH_PARAMS,
        limit=10,
        expr=None,
        output_fields=['id', 'title', 'content'],
        consistency_level="Strong"
    )


embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Connect to DB and load collection
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
collection.load()

results = search_with_string(embeddings, collection)
print(len(results))
for res in results:
    for r in res:
        print(r.entity.get('title'))
        print(r.entity.get('content'))
