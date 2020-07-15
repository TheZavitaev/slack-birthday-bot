import json
from threading import Thread

from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from django.conf import settings

from slackbot.engine import Engine

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)


class SlackEventsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        event = slack_message.get('event')
        event_type = event.get('type')
        user_id = event.get('user')
        # лучше создавать пользователя по событию приглашения от админа,
        # при котором в общем случае происходит несколько событий member_joined_channel,
        # но такое решение доступно только для платных аккаунтов. Поэтому делаем костыль
        if event_type == 'member_joined_channel':
            Engine().operation('create_user', user_id=user_id)

        return Response(status=status.HTTP_200_OK)


class SlackInteractionsSubscriptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        payload = json.loads(request.data.get('payload'))
        Engine().operation('hold_interaction_message', payload=payload)
        return Response(status=status.HTTP_200_OK)


class StartViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        thread = Thread(target=start_processing, args=[request.data['user_id']])
        thread.start()
        return Response(status=status.HTTP_200_OK)


class StopViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        Engine().stop(request.data['user_id'])
        return Response(status=status.HTTP_200_OK)


def start_processing(user_id):
    Engine().start(user_id)
