# %%

import json
import collections
import statistics

with open("../data/all_v0_scored.jsonl", "r") as f:
    data = [json.loads(x) for x in f.readlines()]

data_by_dataset = collections.defaultdict(list)
for line in data:
    dataset = line["dataset"]
    data_by_dataset[dataset].append(line)

out = {}
for dataset, lines in data_by_dataset.items():
    models = set(lines[0]["scores"])
    models_scores = [
        (m, statistics.mean([x["scores"][m]["COMETKiwi22"] for x in lines]))
        for m in models
    ]
    models_scores.sort(key=lambda x: x[1], reverse=True)
    out[dataset] = {m: s for m, s in models_scores}

with open("../outputs/04-metrics.json", "w") as f:
    json.dump(out, f, indent=2)
