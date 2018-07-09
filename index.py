from flask import Flask, jsonify, request, make_response, abort
import os
import dotenv
import json

from src.emoji_uploader import EmojiUploader
from src.emoji_url_generator import EmojiUrlGenerator
from src.parrot_url_generator import ParrotUrlGenerator

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

app_root = os.environ["WEB_ROUTE"]

# Authentication parameters
verification_token = os.environ['VERIFICATION_TOKEN']
oauth_access_token = os.environ["OATUH_ACCESS_TOKEN"]

emoji_url_generator = None

# Very bad way to open a file but who cares it works
with open(os.path.join(os.path.dirname(__file__), 
                       "config",
                       "emoji_image_locations.json")) as default_file:
    emoji_url_generator = EmojiUrlGenerator(json.load(default_file), oauth_access_token)


@app.route(app_root + '/produce_party_parrot', methods=['POST'])
def produce_party_parrot():
    if request.form['token'] != verification_token:
        return abort(400)

    request_json = request.form.to_dict()
    # print(request.form.to_dict())

    # Validate the request
    if not request_json['text']:
        return abort(400)

    original_emoji_name = request_json['text']

    original_emoji_url = emoji_url_generator.get_emoji_url(original_emoji_name)

    parrot_url_generator = ParrotUrlGenerator(original_emoji_url)

    uploader = EmojiUploader(
        request_json['team_domain'],
        os.environ["TEAM_COOKIE"],
        parrot_url_generator.get_emoji_url(),
        original_emoji_name.replace(":","") + "_parrot"
    )

    uploader.upload_emoji()

    payload = {'text': 'DigitalOcean Slack slash command is successful!'}

    return jsonify(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
