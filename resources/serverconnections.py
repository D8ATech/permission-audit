import requests
from time import sleep
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ServerConnections():
    def get_api(session, url, params=None, payload=None):
        while True:
            try:
                r = session.get(url, params=params)
            except requests.exceptions.SSLError:
                r = session.get(url, params=params, verify=False)
            if r.status_code == 429:  # Too many requests
                sleep(5)
            else:
                return r

    def put_api(session, url, params=None, headers=None):
        while True:
            try:
                r = session.put(url, params=params)
            except requests.exceptions.SSLError:
                r = session.put(url, params=params, verify=False)
            if r.status_code == 429:  # Too many requests
                sleep(5)
            else:
                return r

    def post_api(session, url, params=None, headers=None, payload=None):
        while True:
            try:
                r = session.post(url, params=params, payload=payload)
            except requests.exceptions.SSLError:
                r = session.post(url, params=params, payload=payload, verify=False)
            if r.status_code == 429:  # Too many requests
                sleep(5)
            else:
                return r

    def delete_api(session, url, params=None, headers=None, payload=None):
        while True:
            try:
                r = session.delete(url, params=params, payload=payload)
            except requests.exceptions.SSLError:
                r = session.delete(url, params=params, payload=payload, verify=False)
            if r.status_code == 429:  # Too many requests
                sleep(5)
            else:
                return r
