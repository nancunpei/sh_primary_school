import json
from config.config import LOCATION_WX_JSON, LOCATION_WX_JSONL
import os
import sys
c = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(c)


def json2jsonl(source=LOCATION_WX_JSON, target=LOCATION_WX_JSONL):
    if isinstance(source, list):
        json_file = source
    else:
        json_file = json.load(open(source))
    with open(target, 'w') as outfile:
        for entry in json_file:
            json.dump(entry, outfile, ensure_ascii=False)
            outfile.write('\n')
