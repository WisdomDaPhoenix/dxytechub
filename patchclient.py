import requests
def patchDXYData():
    url = "https://allclientsfinal.vercel.app/newclient"
    headers = {"Content-Type": "application/json"}

# CHANGE CLIENT DETAILS HERE TO PATCH CLIENT DATA IN API
    ClientName = "Myron Gaines"
    ClientCourse = "Cybersecurity"
    ClientPhone = "08033334444"
    ClientEmail = "myrongaines@tutamail.com"

    body = {"Client ID": 2,
            "Client Name": ClientName,
            "Client Course": ClientCourse,
            "Client Phone": ClientPhone,
            "Client Email": ClientEmail
            }

    response = requests.patch(url, headers=headers, json=body)
    if response.status_code == 200:
        return f"Client updated in API"
    else:
        return f"Client could not be patched"


if __name__ == "__main__":
    print(patchDXYData())