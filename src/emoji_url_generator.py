import json
import requests

URL = "https://emojipedia-us.s3.amazonaws.com/thumbs/120/google/119/{emoji_name}_{emoji_code}.png"

class EmojiUrlGenerator():
    def __init__(self,
                 default_emoji_list: object,
                 emoji_url: str):
        self.custom_emoji_dict = self._get_custom_emoji_dict(emoji_url)
        self.default_emoji_list = default_emoji_list
        
    def _get_custom_emoji_dict(self, url: str):
        response = requests.get(url)

        return response.json()["emoji"]

    def _create_default_emoji_url(self, default_emoji_object: object):
        return URL.format(emoji_name=default_emoji_object["name"].lower()
                                                                 .replace(" ", "-"),
                          emoji_code=default_emoji_object["unified"].lower())

    def get_emoji_url(self, emoji_name: str):
        emoji_name = emoji_name.replace(":", "")

        if emoji_name in self.custom_emoji_dict:
            return self.custom_emoji_dict[emoji_name]

        for emoji_obj in self.default_emoji_list:
            if emoji_name in emoji_obj["short_names"]:
                return self._create_default_emoji_url(emoji_obj)

        raise ValueError() 