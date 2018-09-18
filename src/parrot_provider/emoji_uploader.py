import requests
import logging
import re
from io import BytesIO
from bs4 import BeautifulSoup
from collections import namedtuple

URL_CUSTOMIZE = "https://{team_name}.slack.com/customize/emoji"
URL_ADD = "https://{team_name}.slack.com/api/emoji.add"
URL_LIST = "https://{team_name}.slack.com/api/emoji.adminList"

API_TOKEN_REGEX = r"api_token: \"(.*)\","
API_TOKEN_PATTERN = re.compile(API_TOKEN_REGEX)

EmojiUploadTask = namedtuple('EmojiUploadTask', [
    "team_name",
    "team_cookie",
    "username",
    "emoji_url",
    "emoji_name",
    "notify_url"
])

logger = logging.getLogger()


class UploadError(Exception):
    def __init__(self, emoji_name: str, message: str) -> None:
        self.emoji_name = emoji_name
        self.message = message


class EmojiUploader:
    def __init__(self,
                 emoji_upload_task: EmojiUploadTask) -> None:
        self.emoji_url = emoji_upload_task.emoji_url
        self.emoji_name = emoji_upload_task.emoji_name
        self.team_cookie = emoji_upload_task.team_cookie
        self.team_name = emoji_upload_task.team_name
        self.session = self._session()

    def _session(self):
        logger.debug("Set up session for EmojiUploader.")
        session = requests.session()
        session.headers = {"Cookie": self.team_cookie}
        session.url_customize = URL_CUSTOMIZE.format(team_name=self.team_name)
        session.url_add = URL_ADD.format(team_name=self.team_name)
        session.url_list = URL_LIST.format(team_name=self.team_name)
        session.api_token = self._fetch_api_token(session)
        return session

    def _fetch_api_token(self, session):
        # Fetch the form first, to get an api_token.
        r = session.get(session.url_customize)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        all_script = soup.findAll("script")

        for script in all_script:
            for line in script.text.splitlines():
                if 'api_token' in line:
                    # api_token: "xoxs-12345-abcdefg....",
                    return API_TOKEN_PATTERN.match(line.strip()).group(1)
        raise Exception('api_token not found. response status={}'.format(r.status_code))

    def upload_emoji(self):
        data = {
            'mode': 'data',
            'name': self.emoji_name,
            'token': self.session.api_token
        }
        files = {'image': BytesIO(requests.get(self.emoji_url).content)}
        r = self.session.post(self.session.url_add, data=data, files=files, allow_redirects=False)
        r.raise_for_status()

        # Slack returns 200 OK even if upload fails, so check for status.
        response_json = r.json()
        if not response_json['ok']:
            print("Error with uploading %s: %s" % (self.emoji_name, response_json))
            logger.debug("Hit error when uploading emoji to slack %s: %s.", self.emoji_name, response_json)

            raise UploadError(self.emoji_name, response_json)
        else:
            logger.debug("Successfully uploaded emoji %s.", self.emoji_name)
            return
