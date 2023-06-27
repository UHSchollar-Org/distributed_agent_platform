import requests

a = {"format": "json"}
params = dict(a)
print(params)
resp = requests.get("https://api.ipify.org", params)  #
# resp = requests.get("https://www.uuidtools.com/api/generate/v1")
print(resp.text)
# print(params)
