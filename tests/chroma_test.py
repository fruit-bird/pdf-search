import json
import chromadb
# from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import (
#     SentenceTransformerEmbeddingFunction,
# )

# chroma_client = chromadb.PersistentClient() # in-disk client
# chroma_client = chromadb.HttpClient() # remote client, for prod
chroma_client = chromadb.Client()  # in-memory client
# sentence_transformer_ef = SentenceTransformerEmbeddingFunction("all-mpnet-base-v2")

test_collection = chroma_client.create_collection(
    name="test_collection",
    # embedding_function=sentence_transformer_ef,
)

test_collection.add(
    documents=[
        "This is a doc about pineapples",
        "This is a doc about oranges",
    ],
    metadatas=[
        {"source": "some file", "page": 1},
        {"source": "some file", "page": 2},
    ],
    ids=[
        "id1",
        "id2",
    ],
)

results = test_collection.query(
    query_texts=["This is a query doc about Hawaii"],
    n_results=1,
)

print(json.dumps(results))
