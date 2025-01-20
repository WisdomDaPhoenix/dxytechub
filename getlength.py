import requests

def lengthData():
    res = requests.get("http://127.0.0.1:5400/newclient")
    content = res.json()
    return len(content["data"])