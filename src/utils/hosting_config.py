import os

from dotenv import load_dotenv


class HostingConfig:
    def __init__(self,
                 dotenv_path: str = None):
        # Default config settings if not available
        self.app_route = ""
        self.host = "0.0.0.0"
        self.port = 5000
        self.debug = False

        if dotenv_path is not None:
            load_dotenv(dotenv_path)

            if "APP_ROUTE" in os.environ:
                self.app_route = os.environ["APP_ROUTE"]
            if "HOST" in os.environ:
                self.host = os.environ["HOST"]
            if "PORT" in os.environ:
                self.port = int(os.environ["PORT"])
            if "DEBUG" in os.environ:
                self.debug = (os.environ["DEBUG"].lower() == "true")
