import os
from joserfc.jwk import OKPKey

path = os.path.realpath(__file__)
directory = os.path.dirname(path)

def get_key():
    f = open(directory + "/key.pem", "r", encoding='utf-8')
    key = OKPKey.import_key(f.read())
    return key

# print(get_key().as_dict())
