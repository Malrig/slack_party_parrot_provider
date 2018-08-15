import os

from dotenv import load_dotenv


class SlackTeamConfig:
    def __init__(self,
                 dotenv_path: str = None):
        # Default config settings if not available
        self.oauth_access_token = "NoTokenAvailable"
        self.team_cookie = "NoCookieAvailable"
        self.verification_token = ""

        if dotenv_path is not None:
            load_dotenv(dotenv_path)

            if "OAUTH_ACCESS_TOKEN" in os.environ:
                self.oauth_access_token = os.environ["OAUTH_ACCESS_TOKEN"]
            if "TEAM_COOKIE" in os.environ:
                self.team_cookie = os.environ["TEAM_COOKIE"]
            if "VERIFICATION_TOKEN" in os.environ:
                self.verification_token = os.environ["VERIFICATION_TOKEN"]
