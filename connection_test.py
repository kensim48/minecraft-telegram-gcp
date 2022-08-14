import requests


def is_mc_server_online(url:str) -> bool:
    payload={}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=3)
    except requests.exceptions.ConnectionError as e:
        if "BadStatusLine" in str(e):
            return True
        else:
            return False
    return False