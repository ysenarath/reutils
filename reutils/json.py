import json


def _get_mode(fp, mode):
    if mode is None:
        if fp.endswith('.jsonline') or fp.endswith('.jsonl'):
            mode = 'jsonl'
        else:
            mode = 'json'
    return mode


def _get_kwargs(**kwargs):
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    return kwargs


def dump(obj, fp, mode=None, **kwargs):
    """Write json object to file

    :param obj: input object
    :param fp: path to the file {str}
    :param mode: input file type {'json', 'jsonl'}. If not provided will determine using file extension.
    :return: contents of file as dict or list
    :return:
    """
    mode = _get_mode(fp, mode)
    kwargs = _get_kwargs(**kwargs)
    if mode == 'jsonl':
        records = []
        for item in obj:
            records.append(json.dumps(item))
        if hasattr(fp, 'write'):
            fp.write('\n'.join(records))
        else:
            with open(fp, 'w', **kwargs) as file:
                file.write('\n'.join(records))
    else:
        if hasattr(fp, 'write'):
            json.dump(obj, fp)
        else:
            with open(fp, 'w', **kwargs) as file:
                json.dump(obj, file)


def load(fp, mode=None, **kwargs):
    """Load json/jsonl file.

    :param fp: path to the file {str}
    :param mode: input file type {'json', 'jsonl'}. If not provided will determine using file extension.
    :return: contents of file as dict or list
    """
    mode = _get_mode(fp, mode)
    kwargs = _get_kwargs(**kwargs)
    if mode == 'jsonl':
        records = []
        if hasattr(fp, 'read'):
            for line in fp.read().split('\n'):
                records.append(json.loads(line.strip()))
        else:
            with open(fp, 'r', **kwargs) as file:
                for line in file.read().split('\n'):
                    records.append(json.loads(line.strip()))
        return records
    else:
        if hasattr(fp, 'read'):
            return json.load(fp)
        else:
            with open(fp, 'r', **kwargs) as file:
                return json.load(file)
