import os
import re
import requests
# /import urllib
# from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

URL = "https://{team_name}.slack.com/customize/emoji"


class EmojiUploader():
    def __init__(self,
                 team_name: str,
                 team_cookie: str,
                 emoji_url: str,
                 emoji_name: str):
        self.session = self._session(team_name, team_cookie)
        self.emoji_url = emoji_url
        self.emoji_name = emoji_name

    def _session(self,
                 team_name: str,
                 team_cookie: str,):
        session = requests.session()
        session.headers = {"Cookie": team_cookie}
        session.url = URL.format(team_name=team_name)
        return session

    def upload_emoji(self):
        # Fetch the form first, to generate a crumb.
        r = self.session.get(self.session.url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        crumb = soup.find("input", attrs={"name": "crumb"})["value"]

        data = {
            'add': 1,
            'crumb': crumb,
            'name': self.emoji_name,
            'mode': 'data',
        }

        files = {'img': BytesIO(requests.get(self.emoji_url).content)}
        r = self.session.post(self.session.url, data=data,
                              files=files, allow_redirects=False)
        r.raise_for_status()

        # Slack returns 200 OK even if upload fails, so check for status of 'alert_error' info box
        if b'alert_error' in r.content:
            soup = BeautifulSoup(r.text, "html.parser")
            crumb = soup.find("p", attrs={"class": "alert_error"})
            print("Error with uploading %s: %s" %
                  (self.emoji_name, crumb.text))
        else:
            print("Success")
