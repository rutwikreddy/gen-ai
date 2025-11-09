import requests

def generate_completion():
    url = "https://api.euron.one/api/v1/euri/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer abkjbkjfdf"
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "How to do multithreading using GIL in python"
            }
        ],
        "model": "gpt-4.1-nano",
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print(data)

if __name__ == "__main__":
  generate_completion()
