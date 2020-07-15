from slack import WebClient
from django.conf import settings
from slack.errors import SlackApiError


class SlackClient(object):
    def __init__(self):
        self.user_client = WebClient(token=getattr(settings, 'SLACK_BOT_USER_TOKEN', None))
        self.bot_client = WebClient(token=getattr(settings, 'SLACK_BOT_BOT_TOKEN', None))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SlackClient, cls).__new__(cls)
        return cls.instance

    def api_call(self, method, **kwargs):
        response = None
        client = self.user_client if kwargs.get('is_user_api') else self.bot_client
        try:
            if method == 'chat_postMessage':
                response = client.chat_postMessage(**kwargs)
            elif method == 'conversations_members':
                response = client.conversations_members(**kwargs)
            elif method == 'conversations_list':
                response = client.conversations_list(**kwargs)
            elif method == 'users_list':
                response = client.users_list(**kwargs)
            elif method == 'users_info':
                response = client.users_info(**kwargs)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        return response
