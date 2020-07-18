from slack import WebClient
from django.conf import settings
from slack.errors import SlackApiError


class SlackClient(object):
    def __init__(self):
        self.client = WebClient(token=getattr(settings, 'SLACK_BOT_USER_TOKEN', None))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SlackClient, cls).__new__(cls)
        return cls.instance

    def api_call(self, method, **kwargs):
        response = None
        try:
            if method == 'chat_postMessage':
                response = self.client.chat_postMessage(**kwargs)
            elif method == 'chat_delete':
                response = self.client.chat_delete(**kwargs)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        return response
