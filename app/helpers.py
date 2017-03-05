import random
import hashlib
import datetime


def generate_api_key():
    return hashlib.sha224(str(random.getrandbits(256))).hexdigest()


def parse_to_dict(data):
    r = {}
    ignored_global_keys = [
        '_sa_instance_state',
        'console_vnc_password',
        'console_vnc_port'
    ]

    try:
        if not g.user.is_admin:
            ignored_global_keys.append('audit_updated_by')
            ignored_global_keys.append('audit_created_by')
            ignored_global_keys.append('audit_deleted_by')
            ignored_global_keys.append('audit_created_on')
            ignored_global_keys.append('audit_deleted_on')
            ignored_global_keys.append('audit_updated_on')
            ignored_global_keys.append('audit_is_deleted')
            ignored_global_keys.append('api_key')
    except (AttributeError, RuntimeError):
        pass

    for key, value in data.__dict__.iteritems():
        if key not in ignored_global_keys:
            if type(value) is datetime.datetime:
                r[key] = str(value)
            else:
                r[key] = value
    return r


def division_helper(field1, field2):
    try:
        return int(round(100 * field1 / field2))
    except ZeroDivisionError:
        return 0

def subnet_calculator(c):
    mask = [0, 0, 0, 0]
    for i in range(c):
        mask[i/8] += (1 << (7 - i % 8))
    return ".".join(map(str, mask))
