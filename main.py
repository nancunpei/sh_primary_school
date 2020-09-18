# -*- coding:utf-8 -*-
import json
from queue import Queue

import plotly.io as pio
import threading
import pandas as pd

from config.config import LOCATION_CSV
from tencent_map.query import query_location_tencent
from baidu_map.query import get_location as query_location_baidu
from tencent_map.translate import translate_from_others

pio.renderers.default = "firefox"


MAX_CONNECTIONS = 4


def persist_local_csv(queue):
    header = "address lat lon tier"
    with open(LOCATION_CSV, 'w') as f:
        f.write(header+'\n')
        for q in range(queue.qsize()):
            data = queue.get()
            f.write(' '.join([data.get('address'), str(data.get('lat')), str(data.get('lon')), data.get('tier'), '\n']))


def local_csv_to_json():
    df = pd.read_csv(LOCATION_CSV, delim_whitespace=True)
    df.to_json('location.json', orient='records', force_ascii=False)


def query_location_thread(all_addresses, target=''):
    threads = []
    queue = Queue()
    semaphore = threading.Semaphore(MAX_CONNECTIONS)
    for (tier, address) in all_addresses:
        if target == 'tencent':
            t = threading.Thread(target=query_location_tencent, args=(tier, address, queue, semaphore))
        else:
            t = threading.Thread(target=query_location_baidu, args=(tier, address, queue, semaphore))
        t.start()
        threads.append(t)
    [t.join() for t in threads]

    persist_local_csv(queue)
    local_csv_to_json()


def compose_location_data():
    with open('location.json') as f:
        data = json.load(f)
    coordinate_list = [str(d.get('lat')) + ',' + str(d.get('lon')) for d in data]
    return coordinate_list


if __name__ == '__main__':
    with open('data.json') as f:
        sh_address = json.load(f).get('data')

    addresses_tierA = []
    addresses_tierB = []
    addresses_tierC = []
    for item in sh_address:
        for tier in ['tierA', 'tierB', 'tierC']:
            l = list(map(lambda x: '上海市' + x if not x.startswith('上海') else x, item.get(tier)))
            if tier == 'tierA':
                addresses_tierA.extend(l)
            elif tier == 'tierB':
                addresses_tierB.extend(l)
            else:
                addresses_tierC.extend(l)

    addresses_tierA = [('tierA', i) for i in addresses_tierA]
    addresses_tierB = [('tierB', i) for i in addresses_tierB]
    addresses_tierC = [('tierC', i) for i in addresses_tierC]
    tiered_list = addresses_tierA + addresses_tierB + addresses_tierC
    query_location_thread(tiered_list)
    # locations = compose_location_data()
    # translate_from_others(locations)


