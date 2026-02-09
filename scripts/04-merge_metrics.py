import argparse
import json

args = argparse.ArgumentParser()
args.add_argument("--input", "-i", type=str, required=True, nargs="+")
args.add_argument("--output", "-o", type=str, required=True)
args = args.parse_args()

data_all = []
for fname in args.input:
    with open(fname, "r") as f:
        data_all.append([json.loads(x) for x in f.readlines()])


def merge_dicts(dict1, dict2):
    """
    Inplace merge dict2 into dict1 recursively.
    Keys are strings but values are either numbers, strings, or other dictionaries.
    Some dictionaries might have some keys missing at any level.
    """

    for k, v in dict2.items():
        if k in dict1:
            if isinstance(v, dict):
                merge_dicts(dict1[k], v)
            else:
                dict1[k] = v
        else:
            dict1[k] = v

    return dict1


# reduce
data_out = data_all.pop(0)
for data in data_all:
    assert len(data) == len(data_out)
    # TODO: in the future we might have a different number of lines
    data_out = [merge_dicts(data_out[i], data[i]) for i in range(len(data_out))]

with open(args.output, "w") as f:
    for line in data_out:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
