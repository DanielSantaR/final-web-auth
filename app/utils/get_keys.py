def get_right_keys(*, payload, db_keys):
    payload = {(db_keys.get(k) if k in db_keys else k): v for (k, v) in payload.items()}
    return payload
