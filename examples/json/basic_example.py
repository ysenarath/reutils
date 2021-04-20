import os
import tempfile

from reutils import json


def assert_equal(a, b):
    for ai, bi in zip(a, b):
        for key in ai:
            if (key not in bi) or (ai[key] != bi[key]):
                return False
    return True


if __name__ == '__main__':
    obj = [{'one': 1}, {'two': 2}]
    with tempfile.TemporaryDirectory() as tmp:
        fp = os.path.join(tmp, 'test.jsonl')
        json.dump(obj, fp)
        assert assert_equal(obj, json.load(fp)), 'Objects are different'
        os.remove(fp)
