def serialize_sets_as_lists(obj):
    """Enable json.dumps to serialize set as list"""
    if isinstance(obj, set):
        return list(obj)

    return obj