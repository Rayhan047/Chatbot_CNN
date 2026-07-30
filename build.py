import subprocess
import sys

print("=" * 60)
print(" NOVA AI BUILD SYSTEM ")
print("=" * 60)

steps = [
    ("Training Word2Vec", "tools/word2vec_train.py"),
    ("Generating Embedding", "tools/embedding.py"),
    ("Training CNN", "train.py")
]

for title, script in steps:

    print(f"\n🚀 {title}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:
        print(f"\n❌ Gagal saat menjalankan {script}")
        sys.exit(1)

print("\n" + "=" * 60)
print("✅ BUILD SELESAI")
print("Model terbaru siap digunakan.")
print("=" * 60)