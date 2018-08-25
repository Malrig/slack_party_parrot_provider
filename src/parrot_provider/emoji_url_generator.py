import requests
import typing

BASE_EMOJI_URL = "https://unicodey.com/emoji-data/img-google-64/{image_link}"
EMOJI_API_URL = "https://slack.com/api/emoji.list?token={oauth_token}"


class EmojiUrlGenerator:
    def __init__(self,
                 default_emoji_list: typing.List,
                 oauth_token: str) -> None:
        self.default_emoji_list = default_emoji_list
        self.oauth_token = oauth_token

    def _get_custom_emoji_dict(self):
        response = requests.get(EMOJI_API_URL.format(oauth_token=self.oauth_token))

        return response.json()["emoji"]

    def get_emoji_url(self, emoji_name: str):
        emoji_name = emoji_name.replace(":", "")

        for emoji_obj in self.default_emoji_list:
            if emoji_name in emoji_obj["short_names"]:
                return BASE_EMOJI_URL.format(image_link=emoji_obj["image"])

        # Only refresh the custom emoji dictionary if it is required.
        custom_emoji_dict = self._get_custom_emoji_dict()

        if emoji_name in custom_emoji_dict:
            return custom_emoji_dict[emoji_name]

        raise ValueError("No emoji found for :{emoji_name}:".format(emoji_name=emoji_name))
