import datetime
import json
from time import sleep
from django.conf import settings


from api.models import Staff, Interaction
from api.utils import get_blocks_for_join_form, get_interaction_kind_code
from slackbot.client import SlackClient


class Engine(object):
    enabled = False
    starter_id = ''
    stopper_id = ''

    def __init__(self):
        self.channel_name = getattr(settings, 'SLACK_BOT_CHANNEL_NAME', None)
        self.bot_user_id = getattr(settings, 'SLACK_BOT_USER_ID', None)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Engine, cls).__new__(cls)
        return cls.instance

    def start(self, starter_id):
        SlackClient().api_call('chat_postMessage', channel=starter_id, text='Добавлен запрос на запуск планировщика')
        sleep(10)
        if not self.enabled:
            channels = SlackClient().api_call('conversations_list', is_user_api=True)['channels']
            channel = [ch for ch in channels if ch['name'] == self.channel_name]
            if len(channel) == 1:
                self.enabled = True
                self.starter_id = starter_id
                SlackClient().api_call('chat_postMessage', channel=starter_id, text='Планировщик задач запущен!')
                migrate_users(self.bot_user_id)
                while self.enabled:
                    sleep(5)
                    # TODO: сюда добавляем генератор поздравлений

                SlackClient().api_call('chat_postMessage', channel=self.stopper_id,
                                       text='Планировщик задач остановлен!')
            else:
                SlackClient().api_call('chat_postMessage', channel=starter_id,
                                       text='Не удалось запустить планировщик. Не найден канал для поздравдений!')

    def stop(self, stopper_id):
        if not self.enabled:
            SlackClient().api_call('chat_postMessage', channel=self.stopper_id, text='Планировщик задач не запущен!')
        else:
            self.enabled = False
            self.stopper_id = stopper_id
            SlackClient().api_call('chat_postMessage', channel=self.stopper_id,
                                   text='Производится остановка планировщика задач ...')

    def operation(self, name, **kwargs):
        if self.enabled:
            if name == 'create_user':
                user_id = kwargs.get('user_id')
                if user_id != self.bot_user_id:
                    self.create_user(user_id, kwargs.get('user_name'))

            elif name == 'hold_interaction_message':
                payload = kwargs.get('payload')
                message = payload.get('message')
                kind = get_kind_of_interaction(message_ts=message.get('ts'))
                action = payload['actions'][0]
                action_type = action['type']
                user_id = payload['user']['id']

                if kind == 'UJF':
                    if action_type == 'button':
                        update_user(user_id)
                    else:
                        update_user_join_form(user_id, action)


def create_user(user_id, user_name=''):
    try:
        Staff.objects.get(slack_id=user_id)
    except Staff.DoesNotExist:
        if not user_name:
            user_name = SlackClient().api_call(
                'users_info',
                user=user_id,
                is_user_api=True
            )['user']['profile']['real_name']
        user = Staff.objects.create(slack_id=user_id, name=user_name)
        initial_date = datetime.datetime.now().strftime("%Y-%m-%d")
        blocks = get_blocks_for_join_form(initial_date)
        message = SlackClient().api_call('chat_postMessage', channel=user_id, blocks=blocks)
        values = {
            'birth_date': initial_date
        }
        Interaction.objects.create(
            message_ts=message.get('ts'),
            kind=get_interaction_kind_code('user_join_form'),
            user=user,
            values_json=json.dumps(values)
        )


def migrate_users(bot_user_id):
    channels = SlackClient().api_call('conversations_list', is_user_api=True)['channels']
    for channel in channels:
        member_ids = SlackClient().api_call('conversations_members', channel=channel['id'], is_user_api=True)['members']
        users = SlackClient().api_call('users_list', is_user_api=True)['members']

        for user in users:
            if user['id'] in member_ids and user['id'] != bot_user_id:
                create_user(user['id'], user['profile']['real_name'])


def update_user(user_id):
    user = Staff.objects.get(slack_id=user_id)
    interaction = Interaction.objects.get(user=user, kind=get_interaction_kind_code('user_join_form'))
    values = json.loads(interaction.values_json)
    birth_date = values.get('birth_date')
    sex = values.get('sex')
    if birth_date:
        user.birth_date = birth_date
    if sex:
        user.sex = bool(sex == 'male')
    user.activated = bool(birth_date) and bool(sex)
    user.save()


def update_user_join_form(user_id, action):
    user = Staff.objects.get(slack_id=user_id)
    interaction = Interaction.objects.get(user=user, kind=get_interaction_kind_code('user_join_form'))
    values = json.loads(interaction.values_json)
    action_type = action['type']
    if action_type == 'static_select':
        values['sex'] = action['selected_option']['value']
    elif action_type == 'datepicker':
        values['birth_date'] = action['selected_date']
    interaction.values_json = json.dumps(values)
    interaction.save()


def get_kind_of_interaction(**kwargs):
    return Interaction.objects.get(**kwargs).kind
