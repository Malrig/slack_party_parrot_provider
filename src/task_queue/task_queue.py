from threading import Thread
import queue
import requests
import logging
from src.parrot_provider.emoji_uploader import EmojiUploader, EmojiUploadTask, UploadError
from src.parrot_blame.parrot_blame import ParrotBlame

logger = logging.getLogger()


class TaskQueue(queue.Queue):
    def __init__(self, parrot_blame: ParrotBlame, num_workers: int = 1) -> None:
        queue.Queue.__init__(self)
        self.parrot_blame = parrot_blame
        self.num_workers = num_workers
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        logger.debug("Adding task to task queue.")
        self.put((task, args, kwargs))

    def start_workers(self):
        for i in range(self.num_workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            emoji_upload_task = EmojiUploadTask(*self.get())
            logger.debug("Getting task.")

            uploader = EmojiUploader(emoji_upload_task)

            try:
                logger.debug("Attempting to upload the emoji.")
                uploader.upload_emoji()
            except UploadError as err:
                message = "Hit an error whilst uploading the emoji :{emoji_name}:: {message}"
                message = message.format(emoji_name=err.emoji_name, message=err.message)
                logger.warning(message)
                response_type = "ephemeral"
            except Exception:
                message = "Hit an unhandled exception whilst uploading the emoji."
                logger.exception("Hit an unhandled exception when uploading the emoji.")
                response_type = "ephemeral"
            else:
                logger.debug("Emoji has been uploaded successfully.")
                message = "\n:{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          "\nCongratulations, your party parrot may or may not have been uploaded. " \
                          "\nIf it has then you should be able to begin using it immediately."\
                          "\n:{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"\
                          ":{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}::{emoji_name}:"
                message = message.format(emoji_name=emoji_upload_task.emoji_name)
                response_type = "in_channel"
                self.parrot_blame.add_parrot_blame_information(emoji_upload_task.emoji_name,
                                                               emoji_upload_task.username,
                                                               emoji_upload_task.team_name)

            response_data = {
                'response_type': response_type,
                'text': message
            }

            requests.post(emoji_upload_task.notify_url,
                          json=response_data,
                          headers={'Content-Type': 'application/json'})

            self.task_done()
