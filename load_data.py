# load_data.py
# data ingestion script // to fill the vector base
import json
from vector_store import add_products_no_metadata, add_products_with_metadata

def main():
    with open("data_products.json", "r") as f:
        products = json.load(f)
    add_products_no_metadata(products)
    add_products_with_metadata(products)
    print("Data loaded successfully into ChromaDB.")

if __name__ == "__main__":
    main()