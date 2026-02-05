# %%

import subset2evaluate
import json

data = [
    line
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

with open("../data/wmt25_humeval.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)

print("Saved", len(data), "lines")
