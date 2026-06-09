import requests
import re

s = requests.Session()
r0 = s.get('http://localhost:8070/taller/login')
match = re.search(r'name="csrf_token"\s+value="([^"]+)"', r0.text)
csrf = match.group(1) if match else ''

r1 = s.post('http://localhost:8070/taller/login/submit', data={
    'email': 'maria.garcia@example.com',
    'password': '123',
    'csrf_token': csrf
})

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "orden_id": 1,
        "notas": "test nota",
        "servicios": [{"producto_id": 1, "cantidad": 1}],
        "repuestos": []
    }
}
r2 = s.post('http://localhost:8070/taller/orden/propuesta/crear', json=payload)
print("Response:", r2.text)
