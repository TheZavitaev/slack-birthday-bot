import utils


def get_context(person):
    """The function forms the context for the home page"""
    # Shows the user's date of birth as a placeholder
    try:
        initial_date = person.birthday
    except:
        initial_date = '1990-01-01'

    # Get 3 "nearest" birthday people
    persons = utils.get_birthday_persons()
    birth_month = {}
    # Gets the short name of the month of the birthday as a dictionary.
    for p in persons:
        month = utils.get_birthday_month(p)
        birth_month[p] = month
    if person.is_admin:
        context = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "birthday",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Выберите дату своего рождения"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": f'{initial_date}',
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date"
                        },
                        "action_id": "datepicker-birthday"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "block_id": "congratulate",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Хотите ли вы получать поздравления в общем канале?"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "выберите вариант"
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "да"
                                },
                                "value": "True"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "нет"
                                },
                                "value": "False"
                            }
                        ],
                        "action_id": "congratulate_on_the_general_channel"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Скоро дни рождения у:"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://mygamehunter.ru/images/thumbnail/147702/550",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[0].slack_id}> отмечает день рождение {persons[0].birthday.day} {birth_month[persons[0]]}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[1].slack_id}> отмечает день рождение {persons[1].birthday.day} {birth_month[persons[1]]}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://store.playstation.com/store/api/chihiro/00_09_000/container/TW/en/999/UP2538-CUSA05620_00-ASIA000000000148/1578133265000/image?w=240&h=240&bg_color=000000&opacity=100&_version=00_09_000",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[2].slack_id}> отмечает день рождение {persons[2].birthday.day} {birth_month[persons[2]]}"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Отправь приветственное сообщение"
                            },
                            "value": "click_me_123",
                            "action_id": "send_greeting_message"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Отправь поздравление именинникам"
                            },
                            "value": "congrat_button",
                            "action_id": "send_congratulations"
                        }
                    ]
                }
            ]
        }

    else:
        context = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "birthday",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Выберите дату своего рождения"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": f'{initial_date}',
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date"
                        },
                        "action_id": "datepicker-birthday"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "block_id": "congratulate",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Хотите ли вы получать поздравления в общем канале?"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "выберите вариант"
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "да"
                                },
                                "value": "True"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "нет"
                                },
                                "value": "False"
                            }
                        ],
                        "action_id": "congratulate_on_the_general_channel"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Скоро дни рождения у:"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://mygamehunter.ru/images/thumbnail/147702/550",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[0].slack_id}> отмечает день рождение {persons[0].birthday.day} {birth_month[persons[0]]}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[1].slack_id}> отмечает день рождение {persons[1].birthday.day} {birth_month[persons[1]]}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://store.playstation.com/store/api/chihiro/00_09_000/container/TW/en/999/UP2538-CUSA05620_00-ASIA000000000148/1578133265000/image?w=240&h=240&bg_color=000000&opacity=100&_version=00_09_000",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<@{persons[2].slack_id}> отмечает день рождение {persons[2].birthday.day} {birth_month[persons[2]]}"
                        }
                    ]
                }
            ]
        }
    return context
