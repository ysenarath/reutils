import os
import tempfile

from reutils import json

if __name__ == '__main__':
    obj = [{}, {}]
    with tempfile.TemporaryDirectory() as tmp:
        fp = os.path.join(tmp, 'test.jsonl')
        json.dump(obj, fp)
        assert obj == json.load(fp), 'Objects are different'
        os.remove(fp)
