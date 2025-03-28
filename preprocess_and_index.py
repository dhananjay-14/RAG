import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load dataset from Kaggle
df = pd.read_csv('The Quran Dataset.csv')

print("Dataset loaded successfully!")
print("Columns:", df.columns)
print(df.head())

# Ensure the correct column name for Quranic text
if "ayah_en" not in df.columns:
    raise ValueError("Column 'ayah_en' not found in the dataset. Check dataset structure.")

# Load embedding model (Use Arabic-compatible model)
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Preprocess and create embeddings
verses = df["ayah_en"].tolist()
embeddings = model.encode(verses, convert_to_numpy=True)

# Save embeddings with FAISS
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save index and verses
faiss.write_index(index, "quran_index.faiss")
with open("quran_verses.pkl", "wb") as f:
    pickle.dump(verses, f)

print("Indexing complete.")

