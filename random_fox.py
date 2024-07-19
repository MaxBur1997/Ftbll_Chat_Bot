import requests


def fox():
    url = 'https://randomfox.ca/floof/'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        return data.get('image')
