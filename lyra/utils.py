def merge_multiple_dicts(dicts):
    items = []
    for d in dicts:
        items += list(d.items())
    dicts = dict(items)
    return dicts
