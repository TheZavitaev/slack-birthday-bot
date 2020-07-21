from api.models import Interaction


def get_interaction_kind_code(kind_choice):
    return [code for code, choice in Interaction.INTERACTION_CHOICES if kind_choice == choice][0]


def get_blocks_for_join_form():
    return [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Привет! Меня зовут *Happy bot*! Я умею поздравлять с днем рождения.\n\n *Пожалуйста, заполните форму ниже*"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Дата рождения:"
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
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Пол:"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Выберете значение",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "М",
                                    "emoji": True
                                },
                                "value": "male"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Ж",
                                    "emoji": True
                                },
                                "value": "female"
                            }
                        ]
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Сохранить",
                                "emoji": True
                            },
                            "value": "save"
                        }
                    ]
                }
            ]