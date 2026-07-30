import pickle
import numpy as np

from gensim.models import Word2Vec

# ==========================
# Load Word2Vec
# ==========================

word2vec = Word2Vec.load(
    "model/word2vec.model"
)

print("Word2Vec berhasil dimuat!")

# ==========================
# Vocabulary
# ==========================

vocab = word2vec.wv.index_to_key

print("\nJumlah kosakata :", len(vocab))

print("\n10 kata pertama:\n")

print(vocab[:10])

print("\nApakah 'ukt' ada?", "ukt" in vocab)
print("Apakah 'uang' ada?", "uang" in vocab)
print("Apakah 'kuliah' ada?", "kuliah" in vocab)

print("\nSemua kata yang mengandung 'ukt':")
print([w for w in vocab if "ukt" in w])

# ==========================
# Word Index
# ==========================

word_index = {}

for i, word in enumerate(vocab):

    word_index[word] = i + 1

print("\nContoh Word Index:\n")

for word in list(word_index.keys())[:10]:

    print(word, "->", word_index[word])

# ==========================
# Embedding Matrix
# ==========================

embedding_dim = word2vec.vector_size

embedding_matrix = np.zeros(
    (len(word_index) + 1, embedding_dim)
)

for word, index in word_index.items():

    embedding_matrix[index] = word2vec.wv[word]

print("\nEmbedding Matrix berhasil dibuat!")

print("Shape :", embedding_matrix.shape)

print("\nVektor kata pertama:\n")

print(embedding_matrix[1])

# ==========================
# Simpan Word Index
# ==========================

with open("model/word_index.pkl", "wb") as f:

    pickle.dump(word_index, f)

print("\nWord Index berhasil disimpan!")

# ==========================
# Simpan Embedding Matrix
# ==========================

with open("model/embedding_matrix.pkl", "wb") as f:

    pickle.dump(embedding_matrix, f)

print("Embedding Matrix berhasil disimpan!")