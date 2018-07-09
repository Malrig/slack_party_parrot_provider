import requests

BASE_EMOJI_URL = "https://emojipedia-us.s3.amazonaws.com/thumbs/120/google/119/{emoji_name}_{emoji_code}.png"
EMOJI_API_URL = "https://slack.com/api/emoji.list?token={oauth_token}"


class EmojiUrlGenerator:
    def __init__(self,
                 default_emoji_list: object,
                 oauth_token: str):
        self.default_emoji_list = default_emoji_list
        self.oauth_token = oauth_token
        self.custom_emoji_dict = None
        
    def _refresh_custom_emoji_dict(self):
        response = requests.get(EMOJI_API_URL.format(oauth_token=self.oauth_token))

        return response.json()["emoji"]

    def get_emoji_url(self, emoji_name: str):
        emoji_name = emoji_name.replace(":", "")

        for emoji_obj in self.default_emoji_list:
            if emoji_name in emoji_obj["short_names"]:
                return BASE_EMOJI_URL.format(emoji_name=self.default_emoji_list["name"].lower()
                                                                                       .replace(" ", "-"),
                                             emoji_code=self.default_emoji_list["unified"].lower())

        # Only refresh the custom emoji dictionary if it is required.
        self._refresh_custom_emoji_dict()

        if emoji_name in self.custom_emoji_dict:
            return self.custom_emoji_dict[emoji_name]

        raise ValueError("No emoji found for {emoji_name}".format(emoji_name=emoji_name)) 