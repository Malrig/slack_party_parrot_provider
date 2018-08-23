import os

ROOT_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Hosting Config
APP_ROUTE = ""      # Base Web Route
HOST = "127.0.0.1"  # Host IP
PORT = "5000"       # Host Port
DEBUG = True        # Run in debug mode

# Slack Config
VERIFICATION_TOKEN = "[Slack App Verification Token]"
OAUTH_ACCESS_TOKEN = "xoxp-[Access Token]"
TEAM_COOKIE = "[Very Long Cookie]"
