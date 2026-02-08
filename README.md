# apertus-translate
Experiments with making Apertus translate and other multilingual tasks


## Data description

Running `scripts/02-prepare_data.py` will prepare data for inference in `data/all_v1.jsonl`.
Each line is a dictionary with the following key, among others:
- `src+prompt`: Input to an LLM for translation.
- `tgt`: When you're running inference with model `XYZ`, save the output string to `item["tgt"]["XYZ"]`.

Data versions:
- `all_v1.jsonl` contains WMT24, WMT24++ and WMT25, including parts without human evaluation
- `all_v0.jsonl` contains WMT24++ and WMT25, including parts without human evaluation