from api.models import Staff, Channel, Interaction
from slack.errors import SlackApiError
from slackbot.client import SlackClient


def on_slack_event(slack_message, bot_user_id):
    event = slack_message.get('event')
    event_type = event.get('type')
    user_id = event.get('user')
    channel_id = event.get('channel')

    if event_type == 'member_joined_channel':
        if user_id == bot_user_id:
            Channel.objects.create(slack_id=channel_id)
        elif Channel.objects.filter(slack_id=channel_id).exists():
            interact_with_joiner(channel_id, user_id)

    elif event_type == 'member_left_channel':
        if user_id == bot_user_id:
            Channel.objects.filter(slack_id=channel_id).delete()


def interact_with_joiner(channel_id, user_id):
    if not Staff.objects.filter(slack_id=user_id).exists():
        # TODO: добавить в форму поля для имени и пола
        message = [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Pick a date of your birthday."
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": "1990-04-28",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        }
                    }
                }]
        client = SlackClient().client
        try:
            res = client.chat_postMessage(channel=channel_id, blocks=message)
            Interaction.objects.create(slack_ts=res.get('ts'), kind='create_user')
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")


def on_slack_interaction(message):
    try:
        interaction = Interaction.objects.get(message.get('ts'))
        if interaction.kind == 'create_user':
            create_user(message)

        interaction.delete()
    except Exception as e:
        pass


def create_user(create_form):
    # TODO: добавить парсинг данных из формы и создание пользователя
    pass