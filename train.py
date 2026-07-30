import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from gensim.models import Word2Vec
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.initializers import Constant
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ==========================
# Membaca Dataset
# ==========================

BASE_DIR = Path(__file__).resolve().parent

folder = BASE_DIR / "data"

all_data = []

for file in folder.glob("*.csv"):

    df = pd.read_csv(file)

    print(file.name, len(df))

    all_data.append(df)

if len(all_data) == 0:
    raise Exception("Folder data kosong! Tambahkan minimal satu file CSV.")

data = pd.concat(
    all_data,
    ignore_index=True
)

print("\n===== LABEL =====")
print(data["label"].value_counts())

print("\n===== UNIQUE =====")
print(data["label"].unique())

# ==========================
# Load Word Index
# ==========================

with open(BASE_DIR / "model" / "word_index.pkl", "rb") as f:
    word_index = pickle.load(f)

print("ukt :", word_index.get("ukt"))
print("uang :", word_index.get("uang"))
print("kuliah :", word_index.get("kuliah"))

# ==========================
# Load Embedding Matrix
# ==========================

with open(BASE_DIR / "model" / "embedding_matrix.pkl", "rb") as f:
    embedding_matrix = pickle.load(f)

# ==========================
# Ubah Kalimat ke Sequence
# ==========================

sentences = []

for text in data["text"]:
    tokens = text.lower().split()

    sequence = []

    for word in tokens:
        sequence.append(word_index.get(word, 0))

    sentences.append(sequence)

X = pad_sequences(
    sentences,
    maxlen=10,
    padding="post"
)

print("Shape X :", X.shape)
print("Shape Embedding :", embedding_matrix.shape)

# ==========================
# Tokenisasi
# ==========================

tokenized_sentences = []

for text in data["text"]:
    tokenized_sentences.append(text.lower().split())

for s in tokenized_sentences[:5]:
    print(s)


# ==========================
# Label Encoding
# ==========================
encoder = LabelEncoder()
y = encoder.fit_transform(data["label"])

# ==========================
# Membagi Dataset
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Jumlah data Training :", len(X_train))
print("Jumlah data Testing  :", len(X_test))

print("Jumlah kategori :", len(encoder.classes_))
print("Kategori :", encoder.classes_)

# ==========================
# Model CNN
# ==========================

model = tf.keras.Sequential([

    # Embedding Layer
    tf.keras.layers.Embedding(
        input_dim=embedding_matrix.shape[0],
        output_dim=embedding_matrix.shape[1],
        embeddings_initializer=Constant(embedding_matrix),
        trainable=True
    ),

    # CNN
    tf.keras.layers.Conv1D(
        filters=64,
        kernel_size=3,
        activation="relu"
    ),

    # Pooling
    tf.keras.layers.GlobalMaxPooling1D(),

    # Hidden Layer
    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    # Output Layer
    tf.keras.layers.Dense(
        len(encoder.classes_),
        activation="softmax"
    )

])

model.summary()

# ==========================
# Compile Model
# ==========================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ==========================
# Training
# ==========================

history = model.fit(
    X_train,
    y_train,
    epochs=20,
    validation_data=(X_test, y_test),
    verbose=1
)

# ==========================
# Simpan Model
# ==========================

model.save(
    BASE_DIR / "model" / "chatbot_model.keras"
)


# ==========================
# Simpan Label Encoder
# ==========================

with open(BASE_DIR / "model" / "label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Model berhasil disimpan!")

# ==========================
# Evaluasi Model
# ==========================

y_pred = model.predict(X_test)

y_pred = np.argmax(y_pred, axis=1)

accuracy = accuracy_score(y_test, y_pred)

print("\n=========================")
print("HASIL EVALUASI MODEL")
print("=========================")

print(f"Accuracy : {accuracy:.4f}")

print("\n=========================")
print("CLASSIFICATION REPORT")
print("=========================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=encoder.classes_
    )
)

# ==========================
# Confusion Matrix
# ==========================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:\n")

print(cm)


# Munculinn Grafikk
#---------------------
fig, ax = plt.subplots(1, 2, figsize=(12,5))

# Accuracy
ax[0].plot(history.history["accuracy"], label="Training")
ax[0].plot(history.history["val_accuracy"], label="Validation")
ax[0].set_title("Accuracy")
ax[0].set_xlabel("Epoch")
ax[0].set_ylabel("Accuracy")
ax[0].legend()
ax[0].grid(True)

# Loss
ax[1].plot(history.history["loss"], label="Training")
ax[1].plot(history.history["val_loss"], label="Validation")
ax[1].set_title("Loss")
ax[1].set_xlabel("Epoch")
ax[1].set_ylabel("Loss")
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()

plt.savefig(BASE_DIR / "model" / "training_result.png")

plt.show()