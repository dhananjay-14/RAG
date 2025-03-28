import faiss
import pickle
import numpy as np
import sys
import traceback

# Ensure proper UTF-8 output
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

from sentence_transformers import SentenceTransformer

def main():
    try:
        # Load FAISS index
        index = faiss.read_index("quran_index.faiss")

        # Load verses
        with open("quran_verses.pkl", "rb") as f:
            verses = pickle.load(f)

        # Load embedding model
        model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

        # Get query from command line arguments
        query = sys.argv[1] if len(sys.argv) > 1 else input("Enter your query: ")
        
        # Encode query
        query_embedding = model.encode([query], convert_to_numpy=True)
        
        # Search Quran
        distances, indices = index.search(query_embedding, 3)
        results = [verses[i] for i in indices[0]]
        
        # Print results
        print("\n".join(results))
        sys.stdout.flush()

    except Exception as e:
        print(f"Error in retrieve_context.py: {str(e)}")
        print(traceback.format_exc())
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    main()