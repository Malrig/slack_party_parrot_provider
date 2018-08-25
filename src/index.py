from flask import Flask, jsonify, request, abort
import os
import json

from config import ROOT_DIR, APP_ROUTE, VERIFICATION_TOKEN
from src.party_parrot_provider import PartyParrotProvider
from src.parrot_blame.parrot_blame import ParrotBlame

app = Flask(__name__)

with open(os.path.join(ROOT_DIR, "data", "emoji_image_locations.json")) as default_file:
    default_slack_emoji_mapping = json.load(default_file)

parrot_blame_object = ParrotBlame(os.path.join(ROOT_DIR, "data"))


def verify_slack_request(to_verify: request) -> bool:
    return to_verify.form['token'] == VERIFICATION_TOKEN


@app.route(APP_ROUTE + '/', methods=['GET'])
@app.route(APP_ROUTE + '/hello_world', methods=['GET'])
def hello_world():
    payload = {
        "text": "Hello World!"
    }

    return jsonify(payload)


@app.route(APP_ROUTE + '/produce_party_parrot', methods=['POST'])
def produce_party_parrot():
    if not verify_slack_request(request):
        return abort(400)

    request_json = request.form.to_dict()

    party_parrot_provider = PartyParrotProvider(
        request_json['text'],
        request_json['team_domain'],
        request_json['user_name'],
        request_json['response_url'],
        default_slack_emoji_mapping,
        parrot_blame_object
    )

    party_parrot_provider.provide_parrot()

    if "_parrot" in request_json['text']:
        message = "You're the reason we can't have nice things, stupid recursive parrots! \n" \
                  "Your abomination will be along shortly... yay..."
    else:
        message = "Your parrot is queued for processing and will be along shortly!"

    payload = {
        'text': message
    }

    return jsonify(payload)


@app.route(APP_ROUTE + '/parrot_blame', methods=['POST'])
def parrot_blame():
    if not verify_slack_request(request):
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
        response_type = "in_channel"
    except ValueError as err:
        message = str(err)
        response_type = "ephemeral"

    return jsonify({
        "response_type": response_type,
        "text": message
    })
