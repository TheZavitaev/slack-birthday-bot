from api.operations import remove_user, \
    get_kind_of_interaction, try_create_user, try_set_channel


def on_slack_command_handler(command_name, **kwargs):
    if command_name == '/set_channel':
        try_set_channel(kwargs.get('channel__name').replace('#', ''), kwargs.get('bot_user_id'))


def on_slack_event_handler(event, **kwargs):
    event_type = event.get('type')
    user_id = event.get('user')
    channel_id = event.get('channel')

    if user_id != kwargs.get('bot_user_id'):
        if event_type == 'member_joined_channel':
            try_create_user(channel_id, user_id)

        elif event_type == 'member_left_channel':
            remove_user(user_id)


def on_slack_interaction_handler(payload):
    message = payload.get('message', None)
    kind = get_kind_of_interaction(message_ts=message.get('ts'))
    if kind == 'UJF':
        print(payload)
        # TODO: добавить обработку данных формы и обновления данных пользователя в БД (дата рождения и пол) -
        #  при выборе даты или пола в форме пользователем заполняем поле value в ресурсе Interaction;
        #  при нажатии на кнопку Сохранить записываем данные в БД

