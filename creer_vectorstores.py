from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

# Fonction de création des Vector Stores
def create_faiss_index(input_json_path, output_faiss_path):
    # Charger les données
    df = pd.read_json(input_json_path)

    # Extraire les contenus des documents
    documents = df['content'].tolist()

    # Créer les embeddings avec OpenAI
    embeddings = OpenAIEmbeddings()

    # Créer le vectorstore FAISS
    vectorstore = FAISS.from_texts(documents, embeddings)

    # Sauvegarder le vectorstore localement
    vectorstore.save_local(output_faiss_path)

    print(f"✅ FAISS Vector Store créé et sauvegardé : {output_faiss_path}")


# Créer les dossiers pour sauvegarder les vecteurs si nécessaire
os.makedirs('vectors/programmes_faiss', exist_ok=True)
os.makedirs('vectors/pratiques_faiss', exist_ok=True)
os.makedirs('vectors/etudes_faiss', exist_ok=True)

# Chemins des fichiers JSON d'entrée
json_paths = [
    ("data/programmes.json", 'vectors/programmes_faiss'),
    ("data/pratiques.json", 'vectors/pratiques_faiss'),
    ("data/etudes.json", 'vectors/etudes_faiss')
]

# Création des Vector Stores pour chaque corpus
for input_json, output_faiss in json_paths:
    create_faiss_index(input_json, output_faiss)

print("🎉 Tous les Vector Stores FAISS ont été générés avec succès.")