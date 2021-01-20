import json
import os
import re

from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

import utils
from context import get_context

load_dotenv()

app = App(
    token=os.getenv('SLACK_BOT_TOKEN'),
    signing_secret=os.getenv('SLACK_SIGNING_SECRET')
)
handler = SlackRequestHandler(app)

flask_app = Flask(__name__)
flask_app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot.db'  # Не забудь 4 флеша для *nix
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)

NOTIFICATION_TIME = 9
CHANNEL_ID = 'C0185GLD9ML'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    slack_id = db.Column(db.String(255), nullable=False)
    slack_username = db.Column(db.String(255), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    wishlist = db.Column(db.String(255), nullable=True)
    # teams = db.relationship('Team', backref='teams')
    #  incoming_notifications_time = db
    is_teamlead = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_congratulate = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Username - {self.slack_username} ID - {self.slack_id} BDay - {self.birthday}'


class Team(db.Model):
    __tablename__ = 'teams'

    team_id = db.Column(db.Integer, primary_key=True)
    teamlead_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    teammates_ids = db.Column(db.Integer(), db.ForeignKey('users.id'))
    channel_id = db.Column(db.String(255), nullable=False)


@app.message(re.compile('(hi|hello|hey|привет|:wave:|даров|дратути)'))
def say_hello_regex(say, context, logger):
    try:
        greeting = context['matches'][0]
        slack_id = context['user_id']
        say(f'{greeting}, <@{slack_id}> how are you?')

    except Exception as e:
        logger.error(f'Error say_hello_regex: {e}')


@app.event('team_join')
def ask_for_introduction(event, say):
    welcome_channel_id = utils.get_channel_id(event)
    slack_id = event["user"]["id"]
    person = utils.get_or_create(db.session, User, slack_id=slack_id)
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Выбери дату своего рождения"},
            "accessory": {
                "type": "datepicker",
                "action_id": "datepicker-birthday",
                "initial_date": "1990-01-01",
                "placeholder": {"type": "plain_text", "text": "Выбери дату"}
            }
        }
    ]
    say(
        blocks=blocks,
        text=f'Добро пожаловать, <@{slack_id}>! 🎉 Я поздработ!',
        channel=welcome_channel_id
    )


@app.event('app_home_opened')
def update_home_tab(client, event, logger):
    """Вью Home page"""
    try:
        slack_id = event['user']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        client.views_publish(
            user_id=person.slack_id,
            view=get_context(person)
        )

    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')


@app.action('send_greeting_message')
def send_greeting_message(ack, say):
    ack()
    blocks = [
        {
            "type": "section",
            "block_id": "birthday",
            "text": {"type": "mrkdwn", "text": "Всем привет! Я поздработ! "
                                               "Введи дату своего рождения и"
                                               " никто про тебя не забудет "
                                               ":)"},
            "accessory": {
                "type": "datepicker",
                "action_id": "datepicker-birthday",
                "initial_date": "1990-01-01",
                "placeholder": {"type": "plain_text", "text": "Выбери дату"}
            }
        }
    ]
    say(
        blocks=blocks,
        channel='C018QT2BV5X'  # CHANNEL_ID
    )


@app.action('send_congratulations')
def send_greeting_message(ack, say):
    """Отправляет поздравления в общий чат, при наличии именинников"""
    ack()
    birthday_persons = utils.find_birthday_person()

    i = 0
    while i != len(birthday_persons):
        for person in birthday_persons:
            gif = utils.get_gif()
            greeting = utils.text_generator(name=person.slack_id)
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Сегодня день рождения у"
                                f" <@{person.slack_username}>!",
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{greeting}"
                    }
                },
                {
                    "type": "image",
                    "image_url": f"{gif}",
                    "alt_text": "inspiration"
                }
            ]
            say(
                blocks=blocks,
                text='someone_text',
                channel='C018QT2BV5X'  # CHANNEL_ID
            )
            i += 1


@app.action('datepicker-birthday')
def get_birthday(ack, body, logger):
    """Достает дату рождения"""
    try:
        ack()
        slack_id = body['user']['id']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        person.slack_username = body['user']['username']

        try:
            birthday = \
                body['view']['state']['values']['birthday'][
                    'datepicker-birthday'][
                    'selected_date']
        except:
            birthday = body['actions'][0]['selected_date']

        person.birthday = utils.convert_birthday(birthday)
        db.session.commit()

    except Exception as e:
        logger.error(f'Error get birthday: {e}')


@app.action('congratulate_on_the_general_channel')
def get_congratulate(ack, body, logger):
    """Достает согласие на поздравление"""
    try:
        ack()
        slack_id = body['user']['id']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        is_congratulate = body['view']['state']['values']['congratulate'][
            'congratulate_on_the_general_channel']['selected_option']['value']
        person.is_congratulate = utils.bool_convert(is_congratulate)
        db.session.commit()

    except Exception as e:
        logger.error(f'Error send congratulate message: {e}')


@app.message('get_data')
def get_data(message, say, logger):
    """Тестовая ручка, чтобы получать инфу о канале и пользователе"""
    try:
        slack_id = message['user']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        birthday = person.birthday
        channel = utils.get_channel_id(message)

        if person.is_admin:
            is_admin = 'админ'
        else:
            is_admin = 'не админ'

        if person.is_congratulate:
            is_congratulate = 'хочешь'
        else:
            is_congratulate = 'не хочешь'

        if person.is_teamlead:
            is_teamlead = 'тимлид'
        else:
            is_teamlead = 'не тимлид'

        say(text=f"Приветики, <@{person.slack_id}>! Мы в канале: {channel}. "
                 f"Твой id - {slack_id} у тебя ДР - {birthday}. "
                 f"Ты {is_admin}. "
                 f"Получать поздравления ты {is_congratulate}. "
                 f"Ты {is_teamlead}")

    except Exception as e:
        logger.error(f"Error send data: {e}")


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/")
def index():
    pagetitle = 'HomePage'
    return render_template('index.html',
                           mytitle=pagetitle,
                           mycontent="Hello World, i'm happy bot")


if __name__ == "__main__":
    flask_app.run(debug=True, port=3000)
