from api.models import Staff, Channel, Interaction
from api.utils import get_interaction_kind_code, get_blocks_for_join_form
from slackbot.client import SlackClient


def try_set_channel(channel_name, bot_user_id):
    channels = SlackClient().api_call('conversations_list', is_user_api=True)['channels']
    channel = [ch for ch in channels if ch['name'] == channel_name]
    if len(channel) == 1:
        channel_id = channel[0]['id']
        if not Channel.objects.filter(slack_id=channel_id).exists():
            Channel.objects.all().delete()
            channel = Channel.objects.create(slack_id=channel_id)
            member_ids = SlackClient().api_call('conversations_members', channel=channel_id, is_user_api=True)['members']
            users = SlackClient().api_call('users_list', is_user_api=True)['members']

            for user in users:
                if user['id'] in member_ids and user['id'] != bot_user_id:
                    create_user(channel, user['id'], user['profile']['real_name'])


def try_create_user(channel_id, user_id):
    channel = Channel.objects.filter(slack_id=channel_id)
    if channel.exists():
        name = SlackClient().api_call('users_info', user=user_id, is_user_api=True)['user']['profile']['real_name']
        create_user(channel[0], user_id, name)


def create_user(channel, user_id, name):
    user = Staff.objects.create(channel=channel, slack_id=user_id, name=name)
    blocks = get_blocks_for_join_form()
    # TODO: сообщение может заспамить личный канал пользователя, если администратор будет переключать каналы с ботом
    #  командой '/set_channel'. Сама по себе привязка пользователя к каналу поздравлений нужна для корректной рассылки
    #  интерактивной формы ввода даты рождения и пола.
    message = SlackClient().api_call('chat_postMessage', channel=user_id, blocks=blocks)
    Interaction.objects.create(
        message_ts=message.get('ts'),
        kind=get_interaction_kind_code('user_join_form'),
        user=user,
    )


def remove_user(user_id):
    Staff.objects.filter(slack_id=user_id).delete()


def get_kind_of_interaction(**kwargs):
    return Interaction.objects.get(**kwargs).kind
