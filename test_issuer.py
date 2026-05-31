import os
import sys

sys.path.append(os.path.abspath('addons/taller_mecanico/models/xades_bes_sri_ec'))
from cryptography.hazmat.primitives.serialization import pkcs12

with open('test.p12', 'rb') as f:
    p12_data = f.read()

private_key, cert, _ = pkcs12.load_key_and_certificates(p12_data, b'123456')

print("rfc4514:", cert.issuer.rfc4514_string())

# Let's see what PyOpenSSL did:
import OpenSSL
p12 = OpenSSL.crypto.load_pkcs12(p12_data, b'123456')
issuer = p12.get_certificate().get_issuer()
issuer_parts = []
for component in issuer.get_components():
    issuer_parts.append(f"{component[0].decode('utf-8')}={component[1].decode('utf-8')}")
print("PyOpenSSL components joined:", ",".join(issuer_parts))

