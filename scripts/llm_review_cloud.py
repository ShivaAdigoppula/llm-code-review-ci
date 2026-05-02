import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"

def read_code():
    with open("reports/changed_code.txt", "r", encoding="utf-8") as file:
        return file.read()

def main():
    code = read_code()

    if not code.strip():
        print("No code found for review.")
        return

    prompt = f"""
You are a senior software engineer.

Review the following code and give:
1. Code summary
2. Possible bugs
3. Security issues
4. Performance issues
5. Improvement suggestions

Code:
{code}
"""

    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    end = time.time()
    response.raise_for_status()

    review = response.json()["response"]

    with open("reports/local_review.md", "w", encoding="utf-8") as file:
        file.write(review)

    with open("reports/local_metrics.txt", "w", encoding="utf-8") as file:
        file.write(f"model={MODEL}\n")
        file.write(f"time_seconds={end - start:.2f}\n")

    print("Local LLM code review completed.")
    print(f"Time taken: {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
