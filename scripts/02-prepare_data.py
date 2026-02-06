# %%

import subset2evaluate
import json

data = [
    line | {"dataset": f"{k[0]}/{k[1]}"}
    for k, v in subset2evaluate.utils.load_data_wmt_all(
        require_human=False, name_filter=lambda k: k[0] in {"wmt25", "wmt24pp"}
    ).items()
    for line in v
]
print("Loaded", len(data), "lines")

with open("../data/wmt25_blind.jsonl", "r") as f:
    data_prompt = [json.loads(x) for x in f.readlines()]
    data_prompt = {line["doc_id"]: line["prompt_instruction"] for line in data_prompt}


def langcode_to_long(lang, script=True):
    from babel import Locale

    try:
        if script:
            return Locale.parse(lang, sep="_").get_display_name("en")
        else:
            return Locale.parse(lang, sep="_").get_language_name("en")
    except:
        return Locale.parse(lang.split("_")[0], sep="_").get_language_name("en")


def get_prompt(src, doc, dataset):
    dataset, langs = dataset.split("/")
    if dataset == "wmt25":
        return data_prompt[doc] + "\n\n" + src
    elif dataset == "wmt24pp":
        lang1, lang2 = langs.split("-")
        lang1_long = langcode_to_long(lang1, script=False)
        lang2_long = langcode_to_long(lang2, script=True)

        return (
            f"You are a professional {lang1_long} to {lang2_long} translator, tasked with providing translations suitable for use in {lang2_long} ({lang2}). Your goal is to accurately convey the meaning and nuances of the original {lang1_long} text while adhering to {lang2_long} grammar, vocabulary, and cultural sensitivities. "
            f"Produce only the {lang2_long} translation, without any additional explanations or commentary. "
            f"Please translate the following {lang1_long} text into {lang2_long} ({lang2}):\n\n"
            f"{src}"
        )
    else:
        raise ValueError(f"Unknown dataset: {dataset}")


data = [
    {"src+prompt": get_prompt(line["src"], line["doc"], line["dataset"])} | line
    for line in data
]

with open("../data/all_v0.jsonl", "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

print("Saved", len(data), "lines")


# %%
import gzip

with open("../data/all_v0.jsonl", "rb") as f:
    with gzip.open("../data/all_v0.jsonl.gz", "wb") as g:
        g.write(f.read())

print("g-zipped")
