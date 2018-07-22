from threading import Thread
import queue
import requests
from src.emoji_uploader import EmojiUploader, EmojiUploadTask


class TaskQueue(queue.Queue):
    def __init__(self, num_workers=1):
        queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((task, args, kwargs))

    def start_workers(self):
        for i in range(self.num_workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            emoji_upload_task = EmojiUploadTask(*self.get())

            uploader = EmojiUploader(emoji_upload_task)

            uploader.upload_emoji()

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

            response_data = {
                'response_type': 'in_channel',
                'text': message.format(emoji_name=emoji_upload_task.emoji_name)
            }

            print(emoji_upload_task.notify_url)

            requests.post(emoji_upload_task.notify_url,
                          json=response_data,
                          headers={'Content-Type': 'application/json'})

            self.task_done()
