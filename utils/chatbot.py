import tensorflow as tf
import json
import random
import pickle
import numpy as np

from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences

# menentukan folder utama (Chatbot_CNN)
BASE_DIR = Path(__file__).resolve().parent.parent


# Load Word Index
#--------------------
with open(BASE_DIR / "model" / "word_index.pkl", "rb") as f:
    word_index = pickle.load(f)


# Load Model CNN
#------------------
with open(BASE_DIR / "model/label_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

model = tf.keras.models.load_model(
    BASE_DIR / "model/chatbot_model.keras"
)


# Load Knowledge
#------------------
knowledge = {}

knowledge_folder = BASE_DIR / "knowledge"

for file in knowledge_folder.glob("*.json"):

    with open(file, "r", encoding="utf-8") as f:

        knowledge.update(json.load(f))


# Prediksi
#--------------
import re

def predict(text):

    print("MASUK KE FUNGSI PREDICT")

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip()

    # ==========================
    # Jika input adalah action button
    # ==========================

    if text in knowledge:

        data = knowledge[text]

        return {
            "title": data["title"],
            "answer": random.choice(data["answer"]),
            "button": data.get("button")
        }

    # Tokenisasi
    tokens = text.split()

    # Ubah kata menjadi index
    sequence = []

    for word in tokens:
        sequence.append(
            word_index.get(word, 0)
        )
        
    print("TOKENS :", tokens)
    print("SEQUENCE :", sequence)

    # Kalau semua kata tidak dikenal
    if sum(sequence) == 0:

        data = knowledge["unknown"]

        return {
            "title": data["title"],
            "answer": random.choice(data["answer"]),
            "button": None
        }

    # Padding
    x = pad_sequences(
        [sequence],
        maxlen=10,
        padding="post"
    )

    # Prediksi CNN
    prediction = model.predict(
        x,
        verbose=0
    )

    # Probabilitas terbesar
    confidence = float(np.max(prediction))

    # Index kelas terbesar
    predicted_index = np.argmax(prediction)

    # Label hasil CNN
    label = encoder.inverse_transform(
        [predicted_index]
    )[0]

    # Jika AI kurang yakin
    if confidence < 0.75:
        label = "unknown"

    print("========================")
    print("Input      :", text)
    print("Sequence   :", sequence)
    print("Prediksi   :", prediction)
    print("Confidence :", confidence)
    print("Label      :", label)
    print("========================")

    if label in knowledge:

        data = knowledge[label]

        return {
            "title": data["title"],
            "answer": random.choice(data["answer"]),
            "button": data.get("button")
        }

    else:

        data = knowledge["unknown"]

        return {
            "title": data["title"],
            "answer": random.choice(data["answer"]),
            "button": None
        }

# ======================================================
# ACTION BUTTON
# ======================================================

def get_action(action):

    print("ACTION DITERIMA :", action)
    print(knowledge.keys())

    if action not in knowledge:

        data = knowledge["unknown"]

        return {
            "title": data["title"],
            "answer": random.choice(data["answer"]),
            "button": None
        }

    data = knowledge[action]

    return {
        "title": data["title"],
        "answer": random.choice(data["answer"]),
        "button": data.get("button")
    }