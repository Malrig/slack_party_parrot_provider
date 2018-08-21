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

    parrot_blame_object = ParrotBlame(data_dir_path)

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
            parrot_blame_object
        )

        party_parrot_provider.provide_parrot()

        if "_parrot" in request_json['text']:
            message = "You're the reason we can't have nice things, stupid recursive parrots! \n" \
                      "Your abomination will be along shortly... yay /s"
        else:
            message = "Your parrot is queued for processing and will be along shortly!"

        payload = {
            'text': message
        }

        return jsonify(payload)

    @app.route(hosting_config.app_route + '/parrot_blame', methods=['POST'])
    def parrot_blame():
        print("Received command")
        if request.form['token'] != slack_team_config.verification_token:
            return abort(400)
        request_json = request.form.to_dict()

        try:
            blame_info = parrot_blame_object.blame_parrot(request_json['text'], request_json['team_domain'])

            if "parrot_parrot" in blame_info.parrot_name:
                message = "The abomination :{parrot_name}: was created by {user} at {datetime}."
            else:
                message = "The parrot :{parrot_name}: was created by {user} at {datetime}."

            message = message.format(parrot_name=blame_info.parrot_name,
                                     user=blame_info.username,
                                     datetime=blame_info.created_date.strftime("%H:%M:%S %d %b %Y"))
            response_type = "ephemeral"
        except ValueError as err:
            message = str(err)
            response_type = "ephemeral"

        return jsonify({
            "response_type": response_type,
            "text": message
        })



    return app
