import json
import os
import re
import time

from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

import utils
from context import get_homepage_context, team_join_block, send_greeting_message_block

from loguru import logger

# Get secrets
load_dotenv()

# Init slack app
app = App(
    token=os.getenv('SLACK_BOT_TOKEN'),
    signing_secret=os.getenv('SLACK_SIGNING_SECRET')
)
handler = SlackRequestHandler(app)

# Init Flask app
flask_app = Flask(__name__)
flask_app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot.db'  # Не забудь 4 флеша для *nix
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    slack_id = db.Column(db.String(255), nullable=False)
    slack_username = db.Column(db.String(255), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    photo = db.Column(db.String(500), nullable=True)
    is_teamlead = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_congratulate = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Username - {self.slack_username} ID - {self.slack_id} BDay - {self.birthday}'


@app.message(re.compile('(hi|hello|hey|привет|:wave:|даров|дратути)'))
def say_hello_regex(say, context):
    """spam stub"""
    try:
        greeting = context['matches'][0]
        slack_id = context['user_id']
        say(f'{greeting}, <@{slack_id}> how are you?')

    except Exception as e:
        logger.error(f'Error say_hello_regex: {e}')


@app.event('team_join')
def ask_for_introduction(event, say):
    """Stub, should send a message when entering the channel"""

    welcome_channel_id = utils.get_channel_id(event)
    slack_id = event['user']['id']
    person = utils.get_or_create(db.session, User, slack_id=slack_id)

    logger.debug(event)
    logger.debug(f'{person} enter in channel {welcome_channel_id}')

    blocks = team_join_block

    try:
        say(
            blocks=blocks,
            text=f'Добро пожаловать, <@{slack_id}>! 🎉 Я поздработ!',
            channel=event["user"]
        )
    except Exception as e:
        logger.error(f'Error team join - {e}')


@app.event('app_home_opened')
def update_home_tab(client, event):
    """View Home page"""

    try:
        slack_id = event['user']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        client.views_publish(
            user_id=person.slack_id,
            view=get_homepage_context(person)
        )

    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')


@app.action('send_greeting_message')
def send_greeting_message(ack, say):
    """Admin sends message by button"""

    ack()
    blocks = send_greeting_message_block
    say(
        blocks=blocks,
        channel='C018QT2BV5X'  # CHANNEL_ID
    )


@logger.catch
@app.action('send_congratulations')
def send_greeting_message(ack, say):
    """The admin sends congratulations to the general chat, if there are birthday people by clicking the button"""
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

            # congratulate the birthday people with a 2 minute interval
            time.sleep(120)


@app.action('datepicker-birthday')
def get_birthday(ack, body):
    try:
        ack()
        slack_id = body['user']['id']
        person = utils.get_or_create(db.session, User, slack_id=slack_id)
        person.slack_username = body['user']['username']

        try:
            birthday = body['view']['state']['values']['birthday']['datepicker-birthday']['selected_date']
        except:
            birthday = body['actions'][0]['selected_date']

        person.birthday = utils.convert_birthday(birthday)
        db.session.commit()

    except Exception as e:
        logger.error(f'Error get birthday: {e}')


@app.action('congratulate_on_the_general_channel')
def get_congratulate(ack, body):
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
def get_data(message, say):
    """Test handler to get channel and user info"""
    try:
        logger.debug(message)

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


# TODO: shedule\\111
@app.message("wake me up")
def say_hello(client, message):
    # https://api.slack.com/methods/chat.scheduleMessage
    logger.debug('wakeup')
    # Unix Epoch time for September 30, 2020 11:59:59 PM
    when_september_ends = 1618870600
    channel_id = message["channel"]
    client.chat_scheduleMessage(
        channel=channel_id,
        post_at=when_september_ends,
        text="Summer has come and passed"
    )


@logger.catch
@app.message('my avatar')
def get_avatar(client, message):
    users = User.query.all()
    for user in users:
        result = client.users_info(
            user=user.slack_id
        )
        person = utils.get_or_create(db.session, User, slack_id=user.slack_id)
        url = result.get('user').get('profile').get('image_original')
        person.photo = url
        db.session.commit()

        logger.info(person.photo)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


# It was supposed to make a one-page with information about the bot
# @flask_app.route("/")
# def index():
#     page_title = 'HomePage'
#     return render_template('index.html',
#                            mytitle=page_title,
#                            mycontent="Hello World, i'm happy bot")


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', debug=True, port=3000)
