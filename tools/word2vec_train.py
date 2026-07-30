import os
import pandas as pd

from gensim.models import Word2Vec

# ==========================
# Membaca semua dataset
# ==========================

folder = "data"

all_data = []

for file in os.listdir(folder):

    if file.endswith(".csv"):

        df = pd.read_csv(os.path.join(folder, file))

        all_data.append(df)

data = pd.concat(
    all_data,
    ignore_index=True
)

print(data.head())

print("\nJumlah data :", len(data))
print("\nLabel yang ada:")
print(data["label"].value_counts())

print("\nContoh data UKT:")
print(data[data["label"] == "ukt"].head(10))

print("\n======================")
print(data[data["label"] == "ukt"].head(20))
print("======================")

# ==========================
# Tokenisasi
# ==========================

sentences = []

for text in data["text"]:

    text = str(text).lower()

    words = text.split()

    sentences.append(words)

print("\nContoh hasil tokenisasi:\n")

for sentence in sentences[:10]:

    print(sentence)

    # ==========================
# Training Word2Vec
# ==========================

model = Word2Vec(
    sentences=sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4,
    epochs=100
)

print("\nWord2Vec berhasil dibuat!\n")

# ==========================
# Mencoba Word2Vec
# ==========================

print("Vektor kata 'dekan':\n")

print(model.wv["dekan"])

print("\nKata yang paling mirip dengan 'dekan':\n")

print(model.wv.most_similar("dekan"))

# ==========================
# Simpan Model Word2Vec
# ==========================

model.save("model/word2vec.model")

print("\nModel Word2Vec berhasil disimpan!")