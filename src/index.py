from flask import Flask, jsonify, request, abort
import os
import sys
import json

from src.utils.slack_team_config import SlackTeamConfig
from src.utils.hosting_config import HostingConfig
from src.party_parrot_provider import PartyParrotProvider
from src.parrot_blame.parrot_blame import ParrotBlame, ParrotBlameInfo


def get_flask_app(hosting_config: HostingConfig,
                  slack_team_config: SlackTeamConfig,
                  data_dir_path: str):

    app = Flask(__name__)

    # Very bad way to open a file but who cares it works
    with open(os.path.join(data_dir_path,
                           'emoji_image_locations.json')) as default_file:
        default_slack_emoji_mapping = json.load(default_file)

    parrot_blame = ParrotBlame(data_dir_path)

    @app.route(hosting_config.app_route + '/', methods=['GET'])
    @app.route(hosting_config.app_route + '/hello_world', methods=['GET'])
    def hello_world():
        print("Received command")
        payload = {
            "text": "Hello World!"
        }

        return jsonify(payload)

    @app.route(hosting_config.app_route + '/produce_party_parrot', methods=['POST'])
    def produce_party_parrot():
        print("Received command")
        if request.form['token'] != slack_team_config.verification_token:
            return abort(400)
        request_json = request.form.to_dict()

        party_parrot_provider = PartyParrotProvider(
            request_json['text'],
            request_json['team_domain'],
            request_json['user_name'],
            request_json['response_url'],
            default_slack_emoji_mapping,
            slack_team_config,
            parrot_blame
        )

        party_parrot_provider.provide_parrot()

        payload = {
            'text': "Your parrot is queued for processing and will be along shortly!"
        }

        return jsonify(payload)

    return app
