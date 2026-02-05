import subprocess
import time
import requests
import json
import os
import argparse
from utils import MODEL_VLLM_PARAMS
import tqdm

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


def get_translation(prompt):
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
                            "content": prompt,
                        }
                    ],
                }
            ),
        )
        response.raise_for_status()
        out = response.json()["choices"][0]["message"]["content"]
        return out.strip()
    except Exception as e:
        print(f"Error translating: {e}")
        return None


if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

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
        stdout=open(f"logs/{args.model.split('/')[-1]}_vllm.out", "w"),
        stderr=open(f"logs/{args.model.split('/')[-1]}_vllm.err", "w"),
    )

    try:
        wait_for_server()

        # Load data
        print("Loading data...")

        with open("data/wmt25_humeval.json", "r") as f:
            data = json.load(f)
        results = []

        print(f"Starting translation of {len(data)} items...")
        for i, item in enumerate(tqdm.tqdm(data)):
            src_text = item["src"]
            translation = get_translation(item["prompt"] + "\n\n" + item["src"])

            result_item = {
                "i": item["i"],
                "src": src_text,
                "tgt": translation,
            }
            results.append(result_item)

            if (i + 1) % 10 == 0:
                with open(OUTPUT_FILE, "w") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)

        # Save results
        print(f"Saving results to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    finally:
        print("Shutting down vllm...")
        process.terminate()
        process.wait()
        print("Done.")
