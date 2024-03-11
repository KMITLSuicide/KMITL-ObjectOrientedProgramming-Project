import os
from joserfc.jwk import OKPKey

path = os.path.realpath(__file__)
directory = os.path.dirname(path)

key = OKPKey.generate_key("Ed25519")
text = key.as_pem(private=True)

# write key to pem file
with open(os.path.join(directory, "key.pem"), "wb") as f:
    f.write(text)
