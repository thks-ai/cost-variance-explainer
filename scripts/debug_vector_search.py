import os
print("[DEBUG] Running file:", os.path.abspath(__file__))

try:
    from app.vector_store import VectorStore
    print("[DEBUG] VectorStore import OK")
except Exception as e:
    print("[ERROR] VectorStore import failed:", e)

import numpy as np

def main():
    print("=== FAISS Search Raw Results ===")

    print("[DEBUG] VectorStore type:", type(VectorStore))

    store = VectorStore()

    dummy = np.random.rand(1536).astype("float32")
    results = store.search(dummy, top_k=5)

    for r in results:
        print(r)
        print("-----------------------------")

if __name__ == "__main__":
    main()






