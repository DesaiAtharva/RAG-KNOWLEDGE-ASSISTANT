import requests
import json

base_url = "http://localhost:8000"

def test_flow():
    # 1. Upload
    print("Testing Upload...")
    with open("test_doc.txt", "rb") as f:
        files = {"file": ("test_doc.txt", f, "text/plain")}
        r = requests.post(f"{base_url}/upload-document", files=files)
        print("Upload Response:", r.json())

    # 2. Ask question
    print("\nTesting Ask...")
    query = {"question": "What is the secret password?"}
    r = requests.post(f"{base_url}/ask", json=query)
    print("Ask Response (Password):", r.json())

    # 3. Ask unrelated
    print("\nTesting Unrelated...")
    query = {"question": "What is the capital of France?"}
    r = requests.post(f"{base_url}/ask", json=query)
    print("Ask Response (Unrelated):", r.json())

    # 4. Ask about "central figure" (tests query rewriting)
    print("\nTesting Semantic Rewrite (Central Figure)...")
    query = {"question": "Who is the central figure?"}
    r = requests.post(f"{base_url}/ask", json=query)
    print("Ask Response (Central Figure):", r.json())

if __name__ == "__main__":
    test_flow()
