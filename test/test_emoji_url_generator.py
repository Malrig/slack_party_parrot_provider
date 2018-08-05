import unittest
from unittest.mock import MagicMock, patch
from src.emoji_url_generator import EmojiUrlGenerator

default_emoji_dict = [
    {
        "name": "FACE WITH TEARS OF JOY",
        "unified": "1F602",
        "non_qualified": None,
        "docomo": "E72A",
        "au": "EB64",
        "softbank": "E412",
        "google": "FE334",
        "image": "1f602.png",
        "sheet_x": 30,
        "sheet_y": 26,
        "short_name": "joy",
        "short_names": ["joy"],
        "text": None,
        "texts": None,
        "category": "Smileys & People",
        "sort_order": 3,
        "added_in": "6.0",
        "has_img_apple": True,
        "has_img_google": True,
        "has_img_twitter": True,
        "has_img_emojione": True,
        "has_img_facebook": True,
        "has_img_messenger": True
    },
    {
        "name": "SMILING FACE WITH OPEN MOUTH AND COLD SWEAT",
        "unified": "1F605",
        "non_qualified": None,
        "docomo": "E722",
        "au": "E471-E5B1",
        "softbank": None,
        "google": "FE331",
        "image": "1f605.png",
        "sheet_x": 30,
        "sheet_y": 29,
        "short_name": "sweat_smile",
        "short_names": ["sweat_smile"],
        "text": None,
        "texts": None,
        "category": "Smileys & People",
        "sort_order": 7,
        "added_in": "6.0",
        "has_img_apple": True,
        "has_img_google": True,
        "has_img_twitter": True,
        "has_img_emojione": True,
        "has_img_facebook": True,
        "has_img_messenger": True
    }
]

custom_emoji_dict = {
    "ok": True,
    "emoji": {
        "bowtie": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/bowtie\/f3ec6f2bb0.png",
        "squirrel": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/squirrel\/465f40c0e0.png",
        "glitch_crab": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/glitch_crab\/db049f1f9c.png",
        "piggy": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/piggy\/b7762ee8cd.png",
        "cubimal_chick": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/cubimal_chick\/85961c43d7.png",
        "dusty_stick": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/dusty_stick\/6177a62312.png",
        "slack": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/slack\/5ee0c9bea3.png",
        "pride": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/pride\/56b1bd3388.png",
        "thumbsup_all": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/thumbsup_all\/50096a1020.gif",
        "slack_call": "https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/slack_call\/b81fffd6dd.png",
        "shipit": "alias:squirrel",
        "white_square": "alias:white_large_square",
        "black_square": "alias:black_large_square",
        "simple_smile": "https:\/\/a.slack-edge.com\/21511\/img\/emoji_2017_12_06\/apple\/simple_smile.png"
    }
}


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://slack.com/api/emoji.list?token=OAUTH_STRING':
        return MockResponse(custom_emoji_dict, 200)

    return MockResponse(None, 404)


@patch('src.emoji_url_generator.requests.get', side_effect=mocked_requests_get)
class TestEmojiUrlGenerator(unittest.TestCase):
    def setUp(self):
        self.emoji_url_generator = EmojiUrlGenerator(default_emoji_dict, "OAUTH_STRING")

    def test_basic_emoji(self, mock_get):
        emoji_url = self.emoji_url_generator.get_emoji_url(":joy:")

        self.assertEqual("https://unicodey.com/emoji-data/img-google-64/1f602.png",
                         emoji_url)
        mock_get.assert_not_called()

    def test_emoji_with_underscores(self, mock_get):
        emoji_url = self.emoji_url_generator.get_emoji_url(":sweat_smile:")

        self.assertEqual("https://unicodey.com/emoji-data/img-google-64/1f605.png",
                         emoji_url)
        mock_get.assert_not_called()

    # TODO write unit tests for skin tone emojis
    # def test_skin_tone_emoji_case(self):
    #     print("test_skin_tone_emoji_case")

    def test_custom_emoji_case(self, mock_get):
        emoji_url = self.emoji_url_generator.get_emoji_url(":squirrel:")

        self.assertEqual("https:\/\/emoji.slack-edge.com\/TBF3XA5LP\/squirrel\/465f40c0e0.png",
                         emoji_url)
        mock_get.assert_called_with('https://slack.com/api/emoji.list?token=OAUTH_STRING')

    def test_no_emoji_found_case(self, mock_get):
        with self.assertRaises(ValueError) as val_err:
            self.emoji_url_generator.get_emoji_url(":emoji_which_doesnt_exist:")

        the_exception = val_err.exception

        mock_get.assert_called_with('https://slack.com/api/emoji.list?token=OAUTH_STRING')
        self.assertEqual("No emoji found for :{emoji_name}:".format(emoji_name="emoji_which_doesnt_exist"),
                         str(the_exception))

