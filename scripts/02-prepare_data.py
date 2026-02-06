# %%

import subset2evaluate
import json

data = [
    line | {"dataset": f"{k[0]}/{k[1]}"}
    for k, v in subset2evaluate.utils.load_data_wmt_all().items()
    if k[0] == "wmt25"
    for line in v
]
print("Loaded", len(data), "lines")

with open("../data/wmt25_blind.jsonl", "r") as f:
    data_prompts = [json.loads(x) for x in f.readlines()]
    data_prompts = {line["doc_id"]: line["prompt_instruction"] for line in data_prompts}

for line in data:
    line["prompt"] = data_prompts[line["doc"]]
    print(line["prompt"])

# TODO: rest of WMT25
# TODO: WMT24++
# TODO: SwissGov-RSD

with open("../data/all_v0.jsonl", "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

print("Saved", len(data), "lines")
