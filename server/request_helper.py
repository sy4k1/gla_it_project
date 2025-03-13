def validate_request_data(data, fields):
    res = []
    for field in fields:
        value = data.get(field, None)
        if value is None:
            res.append(field)
    return res
