from api.models import Staff, Channel, Interaction
from api.utils import get_interaction_kind_code, get_blocks_for_join_form
from slackbot.client import SlackClient


def on_slack_event(slack_message, bot_user_id):
    event = slack_message.get('event')
    event_type = event.get('type')
    user_id = event.get('user')
    channel_id = event.get('channel')

    if event_type == 'member_joined_channel':
        if user_id == bot_user_id:
            channel = Channel.objects.create(slack_id=channel_id)
            # Добавляем в канал интерактивную форму,
            # на которую будем отправлять ссылку для каждого нового пользователя, прибывшего в канал
            # TODO: подумать о кейсе, когда форму удалил кто-то из пользователей
            blocks = get_blocks_for_join_form()
            message = SlackClient().api_call('chat_postMessage', channel=channel_id, blocks=blocks)
            Interaction.objects.create(
                message_ts=message.get('ts'),
                kind=get_interaction_kind_code('user_join_form'),
                channel=channel,
            )
            # TODO: добавить создание в БД пользователей, которые уже есть в канале на момент, когда туда добавляют бота
        else:
            interact_with_joiner(channel_id, user_id)

    elif event_type == 'member_left_channel':
        if user_id == bot_user_id:
            channel = Channel.objects.get(slack_id=channel_id)
            interactions = Interaction.objects.filter(channel=channel)
            for interaction in interactions:
                SlackClient().api_call('chat_delete', channel=channel_id, ts=interaction.message_ts)
            channel.delete()
        else:
            Staff.objects.filter(slack_id=user_id).delete()


def interact_with_joiner(channel_id, user_id):
    try:
        channel = Channel.objects.get(slack_id=channel_id)
        # TODO: добавить получение имени из АПИ Slack
        name = 'Petya'
        user = Staff.objects.create(channel=channel, slack_id=user_id, name=name)
        # TODO: добавить отправку ссылки на форму ввода данных пользователя (может даже в личку, чтобы не спамить канал)

    except Exception as e:
        pass


def on_slack_interaction(payload):
    message = payload.get('message', None)
    try:
        kind = Interaction.objects.get(message_ts=message.get('ts')).kind
        if kind == 'UJF':
            print(payload)
            # TODO: добавить обработку данных формы и обновления данных пользователя в БД (дата рождения и пол)
    except Exception as e:
        pass