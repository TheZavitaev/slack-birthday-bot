from slack import WebClient
from django.conf import settings


class SlackClient(object):
    def __init__(self):
        self.client = WebClient(token=getattr(settings, 'SLACK_BOT_USER_TOKEN', None))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SlackClient, cls).__new__(cls)
        return cls.instance
