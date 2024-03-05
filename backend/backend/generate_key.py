from joserfc.jwk import OKPKey


key = OKPKey.generate_key("Ed25519")

public = key.as_pem(private=False)
private = key.as_pem(private=True)

with open("key.pub", "w", encoding="utf-8") as f:
    f.write(public.decode())

with open("key.pem", "w", encoding="utf-8") as f:
    f.write(private.decode())
