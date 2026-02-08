# %%

import json
from comet import download_model, load_from_checkpoint

with open("../data/all_v1.jsonl", "r") as f:
    data = [json.loads(x) for x in f.readlines()]

METRIC = "COMETKiwi22"
data_missing_metric = set()
for line in data:
    for model, tgt in line["tgt"].items():
        if METRIC not in line["scores"].get(model, {}):
            data_missing_metric.add((line["src"], tgt))

data_missing_metric = list(data_missing_metric)
print(len(data_missing_metric))

model_path = download_model("Unbabel/wmt22-cometkiwi-da")
model = load_from_checkpoint(model_path)
scores = model.predict(
    [{"src": src, "mt": tgt} for src, tgt in data_missing_metric],
    batch_size=16,
    gpus=1,
).scores

data_missing_metric = {
    (src, tgt): score for (src, tgt), score in zip(data_missing_metric, scores)
}
for line in data:
    for model, tgt in line["tgt"].items():
        if METRIC not in line["scores"].get(model, {}):
            line["scores"][model][METRIC] = data_missing_metric[(line["src"], tgt)]

with open("../data/all_v1_scored.jsonl", "w") as f:
    for line in data:
        f.write(json.dumps(line) + "\n")
