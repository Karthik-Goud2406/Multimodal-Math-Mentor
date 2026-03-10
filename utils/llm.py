import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"


# --------------------------------------------------
# NORMAL LLM CALL (used by agents)
# --------------------------------------------------

def call_llm(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 200
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        data = response.json()

        return data.get("response", "")

    except Exception as e:

        return f"LLM Error: {str(e)}"


# --------------------------------------------------
# STREAMING LLM CALL (used by UI)
# --------------------------------------------------

def stream_llm(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.2,
            "num_predict": 200
        }
    }

    try:

        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:

            for line in response.iter_lines():

                if line:

                    data = json.loads(line.decode("utf-8"))

                    if "response" in data:
                        yield data["response"]

    except Exception as e:

        yield f"\nLLM Error: {str(e)}"