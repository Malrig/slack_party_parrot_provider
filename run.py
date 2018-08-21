from flask import Flask, jsonify, request, abort
import os
import dotenv
import json
import time

from src.index import get_flask_app
from src.utils.slack_team_config import SlackTeamConfig
from src.utils.hosting_config import HostingConfig

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
slack_team_config = SlackTeamConfig(dotenv_path)
hosting_config = HostingConfig(dotenv_path)
data_dir_path = os.path.join(os.path.dirname(__file__), 'data')

app = get_flask_app(hosting_config, slack_team_config, data_dir_path)

if __name__ == "__main__":
    app.run(host=hosting_config.host,
            port=hosting_config.port,
            debug=hosting_config.debug)
