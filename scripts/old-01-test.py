# %%

import subset2evaluate
import subset2evaluate.utils

data = subset2evaluate.utils.load_data_wmt_all()
data = {k: v for k, v in data.items() if k[0] == "wmt25"}
print(data.keys())

# %%
import json
import requests

"""
vllm serve "swiss-ai/Apertus-8B-Instruct-2509" --quantization bitsandbytes --load-format bitsandbytes

# smaller model
vllm serve "HuggingFaceTB/SmolLM3-3B" --gpu-memory-utilization 0.6 --max-num-seqs 1

vllm serve "Qwen/Qwen3-1.7B" --gpu-memory-utilization 0.6 --max-num-seqs 1 --max-model-len 2048
"""


def get_translation(text_src):
    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "model": "Qwen/Qwen3-1.7B",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Translate the text on the next line into Czech. Output only the translation and nothing else:\n\n{text_src}\n\n",
                    }
                ],
            }
        ),
    )
    out = response.json()["choices"][0]["message"]["content"]
    out = out.split("</think>")[-1].strip()
    return out


print(get_translation("What is the capital of France?"))
