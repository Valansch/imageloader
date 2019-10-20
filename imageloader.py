import requests


def download_url(url, dest):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        print("Could not connect to server.")
        return False
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
        return True
    else:
        print("Not found.")
        return False
        

