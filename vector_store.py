# vector_store.py 

import chromadb
from sentence_transformers import SentenceTransformer
import json
import os

client = chromadb.PersistentClient(path="./chroma_products")
# Collections: with metadata  and woithout 
collection_no_meta = client.get_or_create_collection(name="products_no_meta")
collection_with_meta = client.get_or_create_collection(name="products_with_meta")

model = SentenceTransformer("all-MiniLM-L6-v2")

#  Embedding ==> convert the text to vectors \
def embed(texts):
    return model.encode(texts).tolist()

# add product to vector store 
# without meta data 
def add_products_no_metadata(products):
    documents = []
    ids = []
    for idx, p in enumerate(products):
        #  description for the product 
        desc = f"Product: {p['product']}. Processor: {p['processor']}. RAM: {p['ram']}. Battery: {p['battery']}. Price: {p['price']} USD."
        documents.append(desc)
        ids.append(str(idx))  
    embeddings = embed(documents)
    collection_no_meta.add(documents=documents, ids=ids, embeddings=embeddings)
    print(f"✅ Added {len(products)} products (no metadata)")


# Search without meta data 
def search_no_metadata(query, k=2):
   
    q_emb = embed([query])[0]
    results = collection_no_meta.query(query_embeddings=[q_emb], n_results=k)
    return results["documents"][0]


# add product to vector store  with meta data
def add_products_with_metadata(products):
    documents = []
    metadatas = []
    ids = []
    for idx, p in enumerate(products):
        desc = f"Product: {p['product']}. Processor: {p['processor']}. RAM: {p['ram']}. Battery: {p['battery']}. Price: {p['price']} USD."
        documents.append(desc)
        metadatas.append({
            "product": p['product'],
            "price": p['price'],
            "processor": p['processor'],
            "ram": p['ram']
        })
        ids.append(str(idx))
    embeddings = embed(documents)
    collection_with_meta.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
    print(f"✅ Added {len(products)} products (with metadata)")


def search_with_metadata(query, max_price=None, processor=None, k=2):
  # search with meta data , by filtering the price or the processor 
    q_emb = embed([query])[0]
    where_filter = {}
    if max_price is not None:
        where_filter["price"] = {"$lt": max_price}
    if processor:
        where_filter["processor"] = processor
    results = collection_with_meta.query(
        query_embeddings=[q_emb],
        n_results=k,
        where=where_filter if where_filter else None
    )
    return results["documents"][0], results["metadatas"][0]

# test 
if __name__ == "__main__":
    with open("data_products.json", "r") as f:
        data = json.load(f)
    add_products_no_metadata(data)
    add_products_with_metadata(data)
    print("\nSearch without metadata: 'laptop long battery'")
    print(search_no_metadata("laptop long battery"))
    print("\nSearch with metadata (price<1000): 'tablet'")
    docs, metas = search_with_metadata("tablet", max_price=1000)
    print(docs)
    print(metas)


