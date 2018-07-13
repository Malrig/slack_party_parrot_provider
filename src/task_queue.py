from threading import Thread
import queue
import time
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
            emoji_upload_task = self.get()

            uploader = EmojiUploader(emoji_upload_task)

            uploader.upload_emoji()

            self.task_done()
