import requests

def lengthData():
    res = requests.get("https://allclientsfinal.vercel.app/newclient")
    content = res.json()
    return len(content["data"])