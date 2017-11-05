import json
import os

dataset = {}

def read_dataset():
    with open('dataset/dataset.json') as json_data:
        dataset = json.load(json_data)

if __name__ == '__main__':
    read_dataset()
