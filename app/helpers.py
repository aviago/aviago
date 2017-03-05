import random
import hashlib


def generate_api_key():
    return hashlib.sha224(str(random.getrandbits(256))).hexdigest()

