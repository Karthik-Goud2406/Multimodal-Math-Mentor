import json
import os

MEMORY_FILE = "memory/memory.json"


def save_memory(record):

    data = []

    if os.path.exists(MEMORY_FILE):

        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)

        except:
            data = []

    data.append(record)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)