import os
from json import JSONDecodeError

from reutils import json

path_jsonl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file.jsonl')

if __name__ == '__main__':
    try:
        for tweet in json.load(path_jsonl):
            print(tweet)
    except JSONDecodeError as e:
        print('Unable to parse the file at {}'.format(path_jsonl))
