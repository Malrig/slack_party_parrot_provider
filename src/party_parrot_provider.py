from src.utils.slack_team_config import SlackTeamConfig
from src.parrot_provider.emoji_url_generator import EmojiUrlGenerator
from src.parrot_provider.parrot_url_generator import ParrotUrlGenerator
from src.parrot_provider.emoji_uploader import EmojiUploadTask
from src.task_queue.task_queue import TaskQueue
from src.parrot_blame.parrot_blame import ParrotBlame


class PartyParrotProvider:
    def __init__(self,
                 slack_text: str,
                 team_name: str,
                 username: str,
                 notify_url: str,
                 default_slack_emoji_mapping: dict,
                 slack_team_config: SlackTeamConfig,
                 parrot_blame: ParrotBlame):
        self.slack_text = slack_text
        self.team_name = team_name
        self.username = username
        self.notify_url = notify_url
        self.original_emoji_name = None
        self.new_emoji_name = None
        self.default_slack_emoji_mapping = default_slack_emoji_mapping
        self.slack_team_config = slack_team_config
        self.task_queue = TaskQueue(parrot_blame, num_workers=1)

    def _parse_and_validate_input(self):
        print('Validating input')
        # TODO Need to do some validation of the text sent from Slack

        # Now assign the parameters
        self.original_emoji_name = self.slack_text.replace(":", "")
        self.new_emoji_name = self.original_emoji_name + "_parrot"

    def provide_parrot(self):
        # First validate the text sent from Slack
        self._parse_and_validate_input()

        # Get the URL to the original emoji
        emoji_url_generator = EmojiUrlGenerator(self.default_slack_emoji_mapping,
                                                self.slack_team_config.oauth_access_token)
        original_emoji_url = emoji_url_generator.get_emoji_url(self.original_emoji_name)

        # Create the URL for the parrot
        parrot_url_generator = ParrotUrlGenerator(original_emoji_url)
        parrot_url = parrot_url_generator.get_emoji_url()

        self.task_queue.put(EmojiUploadTask(
            team_name=self.team_name,
            team_cookie=self.slack_team_config.team_cookie,
            username=self.username,
            emoji_url=parrot_url,
            emoji_name=self.new_emoji_name,
            notify_url=self.notify_url
        ))
