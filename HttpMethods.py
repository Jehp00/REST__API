import requests

BASE = "http://127.0.0.1:5000/"


response = requests.delete(BASE + "Video/2")
print(response)

response = requests.get(BASE + "Video/2")
print(response.json)
