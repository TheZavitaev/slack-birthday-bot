from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from django.conf import settings

from api.operations import on_slack_event, on_slack_interaction

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_ID = getattr(settings, 'SLACK_BOT_USER_ID', None)


class SlackEventsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        on_slack_event(slack_message, SLACK_BOT_USER_ID)
        return Response(status=status.HTTP_200_OK)


class SlackInteractionsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        payload = request.data.get('payload')
        if payload:
            on_slack_interaction(payload[0].get('message'))
        return Response(status=status.HTTP_200_OK)
