from flask import Flask, jsonify, request, abort
import os
import dotenv
import json
import time

from src.utils.slack_team_config import SlackTeamConfig
from src.party_parrot_provider import PartyParrotProvider

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
slack_team_config = SlackTeamConfig(dotenv_path)

default_slack_emoji_mapping = None

# TODO Move these config parameters into a config file instead of unpacking them here
dotenv.load_dotenv(dotenv_path)
verification_token = os.environ['VERIFICATION_TOKEN']
app_root = os.environ['WEB_ROUTE']

# Very bad way to open a file but who cares it works
with open(os.path.join(os.path.dirname(__file__), 
                       'data',
                       'emoji_image_locations.json')) as default_file:
    default_slack_emoji_mapping = json.load(default_file)


@app.route(app_root + '/hello_world', methods=['GET'])
def hello_world():
    print("Received command")
    time.sleep(10)
    payload = {'text': "Hello World!"}

    return jsonify(payload)


@app.route(app_root + '/produce_party_parrot', methods=['POST'])
def produce_party_parrot():
    print("Received command")
    if request.form['token'] != verification_token:
        return abort(400)
    request_json = request.form.to_dict()

    party_parrot_provider = PartyParrotProvider(
        request_json['text'],
        request_json['team_domain'],
        request_json['response_url'],
        default_slack_emoji_mapping,
        slack_team_config
    )

    party_parrot_provider.provide_parrot()

    payload = {'text': "Your parrot is queued for processing and will be along shortly!"}

    return jsonify(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
