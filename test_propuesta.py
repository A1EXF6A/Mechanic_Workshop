import requests
import json

s = requests.Session()
# first we need to login to get session
res = s.get('http://localhost:8070/taller/login')
res = s.post('http://localhost:8070/taller/login/submit', data={
    'email': 'maria.garcia@example.com',
    'password': '123',
    'csrf_token': ''
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
r = s.post('http://localhost:8070/taller/orden/propuesta/crear', json=payload)
print(r.json())
