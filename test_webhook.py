import requests
import json
url = 'http://127.0.0.1:8433/webhook'
data = {'key1': '2024', 'key2': '2025'}
data= json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
response = requests.post(url, data=data)
print(response.text)