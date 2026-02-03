import subprocess
import time
import requests
import json
import sys
import argparse
from utils import MODEL_VLLM_PARAMS

args = argparse.ArgumentParser()
args.add_argument("--model", type=str, default="Qwen/Qwen3-1.7B")
args = args.parse_args()

# Configuration
API_URL = "http://localhost:8000/v1/chat/completions"
HEALTH_URL = "http://localhost:8000/health"


def wait_for_server():
    print("Waiting for vllm server to start...")
    while True:
        try:
            response = requests.get(HEALTH_URL)
            if response.status_code == 200:
                print("Server is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)


def get_translation(text_src, lang1, lang2):
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "model": args.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Translate the text on the next line from {lang1} to {lang2}. Output only the translation in {lang2} and nothing else:\n\n{text_src}\n\n",
                        }
                    ],
                }
            ),
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error translating: {e}")
        return None


if __name__ == "__main__":
    # Ensure output directory exists
    OUTPUT_FILE = f"outputs/{args.model.split('/')[-1]}.json"

    # Launch vllm
    print(f"Launching vllm with model {args.model}...")
    # Using the command from 01-test.py / user request
    cmd = [
        "vllm",
        "serve",
        args.model,
        *[
            x
            for k, v in MODEL_VLLM_PARAMS[args.model].items()
            for x in (f"--{k}", str(v))
        ],
    ]

    process = subprocess.Popen(
        cmd,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    try:
        wait_for_server()
        translation = get_translation(
            "Efektivní online skalární anotace s ohraničenou podporou.",
            "Czech",
            "English",
        )

    finally:
        print("Shutting down vllm...")
        process.terminate()
        process.wait()
        print("Done.")
