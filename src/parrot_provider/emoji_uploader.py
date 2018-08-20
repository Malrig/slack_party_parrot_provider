import requests
from io import BytesIO
from bs4 import BeautifulSoup
from collections import namedtuple

URL = "https://{team_name}.slack.com/customize/emoji"

EmojiUploadTask = namedtuple('EmojiUploadTask', [
    "team_name",
    "team_cookie",
    "username",
    "emoji_url",
    "emoji_name",
    "notify_url"
])


class UploadError(Exception):
    def __init__(self, emoji_name: str, message: str):
        self.emoji_name = emoji_name
        self.message = message


class EmojiUploader:
    def __init__(self,
                 emoji_upload_task: EmojiUploadTask):
        self.emoji_url = emoji_upload_task.emoji_url
        self.emoji_name = emoji_upload_task.emoji_name
        self.team_cookie = emoji_upload_task.team_cookie
        self.team_name = emoji_upload_task.team_name
        self.session = self._session()

    def _session(self):
        session = requests.session()
        session.headers = {"Cookie": self.team_cookie}
        session.url = URL.format(team_name=self.team_name)
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

            raise UploadError(self.emoji_name, crumb.text)
        else:
            return
