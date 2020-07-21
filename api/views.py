import json

from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from django.conf import settings

from api.handlers import on_slack_event_handler, on_slack_interaction_handler, on_slack_command_handler

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_ID = getattr(settings, 'SLACK_BOT_USER_ID', None)


class SlackEventsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        on_slack_event_handler(slack_message.get('event'), bot_user_id=SLACK_BOT_USER_ID)
        return Response(status=status.HTTP_200_OK)


class SlackInteractionsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        payload = request.data.get('payload')
        on_slack_interaction_handler(json.loads(payload))
        return Response(status=status.HTTP_200_OK)


class SlackCommandsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        command = request.data
        on_slack_command_handler(command['command'], channel__name=command['text'], bot_user_id=SLACK_BOT_USER_ID)
        return Response(status=status.HTTP_200_OK)
