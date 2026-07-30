import pandas as pd
import os

folder = "data"

all_data = []

for file in os.listdir(folder):

    if file.endswith(".csv") and file != "dataset.csv":

        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        all_data.append(df)

dataset = pd.concat(
    all_data,
    ignore_index=True
)

dataset.to_csv(
    os.path.join(folder, "dataset.csv"),
    index=False,
    encoding="utf-8-sig"
)

print("=" * 40)
print("Dataset berhasil dibuat!")
print("Jumlah data :", len(dataset))
print("=" * 40)