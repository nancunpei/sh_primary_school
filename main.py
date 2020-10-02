# -*- coding:utf-8 -*-
import json
from queue import Queue
import click
import threading
import pandas as pd

from config.config import LOCATION_CSV, LOCATION_JSON, LOCATION_WX_JSONL, LOCATION_WX_JSON, BASE_DATA
from tencent_map.query import query_location_tencent
from baidu_map.query import get_location as query_location_baidu
from tencent_map.translate import translate_from_others

MAX_CONNECTIONS = 5


def persist_local_csv(queue):
    header = "address lat lon tier district"
    with open(LOCATION_CSV, 'w') as f:
        f.write(header+'\n')
        for _ in range(queue.qsize()):
            data = queue.get()
            f.write(' '.join([data.get('address'), str(data.get('lat')), str(
                data.get('lon')), data.get('tier'), data.get('district'), '\n']))


def local_csv_to_json():
    df = pd.read_csv(LOCATION_CSV, delim_whitespace=True)
    df.to_json(LOCATION_JSON, orient='records', force_ascii=False)


def query_location_thread(all_addresses, target=''):
    if not target:
        return
    threads = []
    queue = Queue()
    semaphore = threading.Semaphore(MAX_CONNECTIONS)
    for (address, tier, district) in all_addresses:
        if target == 'tencent':
            t = threading.Thread(target=query_location_tencent, args=(
                tier, address, district, queue, semaphore))
        elif target == 'baidu':
            t = threading.Thread(target=query_location_baidu, args=(
                tier, address, district, queue, semaphore))
        else:
            pass
        t.start()
        threads.append(t)
    [t.join() for t in threads]

    persist_local_csv(queue)
    local_csv_to_json()


def compose_location_data():
    with open(LOCATION_JSON) as f:
        data = json.load(f)
    coordinate_list = [str(d.get('lat')) + ',' +
                       str(d.get('lon')) for d in data]
    return coordinate_list


def compose_tiered_addresses():
    with open(BASE_DATA) as f:
        sh_address = json.load(f).get('data')

    addresses_tierA = []
    addresses_tierB = []
    addresses_tierC = []
    for district_schools in sh_address:
        district = district_schools.get('district')
        for tier in ['tierA', 'tierB', 'tierC']:
            schools = list(map(lambda x:
                               ('上海市' + x, tier, district) if not x.startswith('上海') else (x, tier, district), district_schools.get(tier)))
            if tier == 'tierA':
                addresses_tierA.extend(schools)
            elif tier == 'tierB':
                addresses_tierB.extend(schools)
            else:
                addresses_tierC.extend(schools)

    tiered_list = addresses_tierA + addresses_tierB + addresses_tierC
    print(tiered_list)
    return tiered_list


@click.command()
@click.option('--target', default='', help='select the map api to run')
@click.option('--convert', default=False, help='whether need to convert location data')
def main(target, convert):
    if target:
        tiered_list = compose_tiered_addresses()
        query_location_thread(tiered_list, target)
    if convert:
        import os
        if not os.getenv('WX_KEY'):
            raise KeyError('please input wx map key')
        locations = compose_location_data()
        translate_from_others(locations)


if __name__ == '__main__':
    main()
    # json2jsonl()
