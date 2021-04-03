import pickle
import os


def cache(path):
    def decorate_func(func):
        def decorated_func(*args, **kwargs):
            fn = '_'.join([str(arg) for arg in args])
            fn += '_'.join(['{}-{}'.format(key, kwargs[key]) for key in sorted(kwargs)])
            fn_path = os.path.join(path, '{}.pickle'.format(fn))
            if os.path.exists(fn_path):
                with open(fn_path, 'rb') as fp:
                    return pickle.load(fp)
            result = func(*args, **kwargs)
            with open(fn_path, 'wb') as fp:
                pickle.dump(result, fp)
            return result

        return decorated_func

    return decorate_func
