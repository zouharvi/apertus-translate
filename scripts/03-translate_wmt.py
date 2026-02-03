import subprocess
import time
import requests
import json
import os
import subset2evaluate
import subset2evaluate.utils
import argparse
from utils import LANG_TO_NAME, MODEL_VLLM_PARAMS
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
        out = response.json()["choices"][0]["message"]["content"]
        # Basic parsing based on 01-test.py logic, assuming </think> might be present
        if "</think>" in out:
            out = out.split("</think>")[-1].strip()
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
        data = subset2evaluate.utils.load_data_wmt_all()
        data = {k: v for k, v in data.items() if k[0] == "wmt25"}
        data = [
            line
            | {
                "lang1": LANG_TO_NAME[k[1].split("-")[0]],
                "lang2": LANG_TO_NAME[k[1].split("-")[1]],
            }
            for k, v in data.items()
            for line in v
        ]
        results = []

        print(f"Starting translation of {len(data)} items...")
        for i, item in enumerate(tqdm.tqdm(data)):
            src_text = item["src"]
            translation = get_translation(src_text, item["lang1"], item["lang2"])

            result_item = {
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
