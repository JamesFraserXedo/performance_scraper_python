import json
import os
from shutil import move

import time


def clear_hars():
    list_of_files = os.listdir('har')
    for f in list_of_files:
        os.remove('har\\' + f)


def analyse(filename):
    with open('har\\' + filename + '.har', encoding='utf-8') as data_file:
        data = json.load(data_file)

    entries = (data['log']['entries'])
    total = 0
    for entry in entries:
        total += int(entry['response']['bodySize'])

    return {
        "requests": len(entries),
        "transferred": get_file_size(total)
    }

def analyse_unknown():
    list_of_files = []

    t_end = time.time() + 30
    while len(list_of_files) == 0 and time.time() < t_end:
        list_of_files = os.listdir('har')

    details = {}

    if len(list_of_files) == 1:
        move('har\\' + list_of_files[0], 'har\\testing.har')
        details = analyse('testing')
    else:
        print("Error in finding file")

    os.remove('har\\testing.har')
    return details


def get_file_size(byts):
    units = 'B'
    if byts >= 1000:
        byts /= 1000
        units = 'KB'
    if byts >= 1000:
        byts /= 1000
        units = 'MB'
    if byts >= 1000:
        byts /= 1000
        units = 'GB'

    return "{} {}".format(str(round(byts, 1)), units)