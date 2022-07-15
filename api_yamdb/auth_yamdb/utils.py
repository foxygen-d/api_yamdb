import hashlib

from django.utils.encoding import force_bytes


def bland_code_hasher(*args):
    return hashlib.md5(force_bytes(''.join(args))).hexdigest()


def salty_code_hasher(code):
    return hashlib.md5(force_bytes(code + 'yourmom')).hexdigest()
