update_home_tab_context = {
    "type": "home",
    "callback_id": "home_view",
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
                "initial_date": "1990-01-01",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
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
                    "text": "выберите вариант",
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "да",
                        },
                        "value": 'True'
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "нет",
                        },
                        "value": 'False'
                    }
                ],
                "action_id": "congratulate_on_the_general_channel"
            }
        },
    ]
}

update_home_tab_context_admin = {
    "type": "home",
    "callback_id": "home_view",
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
                "initial_date": "1990-01-01",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
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
                    "text": "выберите вариант",
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "да",
                        },
                        "value": 'True'
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "нет",
                        },
                        "value": 'False'
                    }
                ],
                "action_id": "congratulate_on_the_general_channel"
            }
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "I Need a Marg",
            },
            "image_url": "https://assets3.thrillist.com/v1/image/1682388/size/tl-horizontal_main.jpg",
            "alt_text": "marg"
        }
    ]
}
