import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "Where are the laptops?"}
res = requests.post(url, json=data)

print(res.status_code)
print(res.json())