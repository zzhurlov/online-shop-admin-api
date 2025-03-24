# utils


def set_dict_attr(obj, data):
    for attr, value in data.items():
        setattr(obj, attr, value)  # Или obj.attr = value для каждого атрибута
    return obj
