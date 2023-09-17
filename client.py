import requests

url = "https://python-vercel-test-one.vercel.app/api"
data = {"data": "Hello, Flask!"}

response = requests.post(url, data=data)
print(response.text)
