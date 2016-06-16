import pickle
import requests
import json

import time

from config import base_url
from codec import *


def backup_datasets(data):
    with open('graph_data.txt', 'wb') as f:
        pickle.dump(data, f)


def restore_datasets():
    try:
        with open('graph_data.txt', 'rb') as f:
            return pickle.load(f)
    except:
        return {}

datasets = restore_datasets()


def update_dom_load(mil, page):
    update_millis(mil, page, MetricsTypes.dom_load)


def update_page_load(mil, page):
    update_millis(mil, page, MetricsTypes.page_load)


def update_millis(mil, page, metrics_type):
    url = generate_url(page, metrics_type, WidgetTypes.millis)

    payload = json.loads(
        json.dumps(
            {
                "auth_token": "XEDO_GRAPHING",
                "current": mil
            }
        )
    )
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)


def get_datasets_key(page, metrics_type):
    return base_url['dashboard_id'] + '_' + page['dashboard_id'] + '_' + metrics_type


def update_dataset(x, y, page, metrics_type):
    key = get_datasets_key(page, metrics_type)
    if key not in datasets:
        datasets[key] = [{
            "x": time.time()-((60-i)*60),
            "y": 0
        } for i in range(60)]

    dataset = datasets[key]
    dataset.append(
        {
            "x": x,
            "y": y
        }
    )

    if len(dataset) > 60:
        del dataset[0]

    datasets[key] = dataset
    backup_datasets(datasets)


def update_graph(x, y, page, metrics_type):
    update_dataset(x, y, page, metrics_type)
    url = generate_url(page, metrics_type, WidgetTypes.graph)

    payload = json.loads(
        json.dumps(
            {
                "auth_token": "XEDO_GRAPHING",
                "points": datasets[get_datasets_key(page, metrics_type)],
                "displayedValue": y
            }
        )
    )
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)


def generate_url(page, metrics_type, widget_type):
    url = 'http://localhost:3030/widgets/'

    url += base_url['dashboard_id'] + '_'
    url += page['dashboard_id'] + '_'
    url += metrics_type + '_'
    url += widget_type

    return url


