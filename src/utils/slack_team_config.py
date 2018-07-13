import os

from dotenv import load_dotenv


class SlackTeamConfig:
    def __init__(self,
                 dotenv_path: str):
        load_dotenv(dotenv_path)

        self.oauth_access_token = os.environ["OAUTH_ACCESS_TOKEN"]
        self.team_cookie = os.environ["TEAM_COOKIE"]
