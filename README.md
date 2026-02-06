# apertus-translate
Experiments with making Apertus translate and other multilingual tasks


## Data description

Running `scripts/02-prepare_data.py` will prepare data for inference in `data/all_v0.jsonl`.
Each line is a dictionary with the following key, among others:
- `src+prompt`: input to an LLM for translation
When you're running inference with model `XYZ`, save the output string to `item["tgt"]["XYZ"]`.