import datetime as dt
import random

from sqlalchemy import extract

from bot import User


def get_or_create(session, model, **kwargs) -> object:
    """Receives an instance of the model upon request, if there is none,
    creates it """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def bool_convert(string: str) -> bool:
    """Needed to save to the database"""
    if string == 'True':
        return True
    else:
        return False


def get_channel_id(data: dict) -> str:
    """Return channel id from payload"""
    channel = data['channel']
    return channel


def convert_birthday(birthday: str):
    birthday = dt.date(*tuple(map(int, birthday.split('-'))))
    return birthday


def get_birthday_persons() -> list:
    """Gets a list of birthday people sorted by day and month"""
    date_now = dt.datetime(dt.datetime.today().year, dt.datetime.today().month,
                           dt.datetime.today().day)

    persons = []

    bday_sort = User.query.group_by(
        extract('month', User.birthday),
        extract('day', User.birthday)).filter(
        extract('month', User.birthday) >= dt.datetime.today().month).all()

    for p in bday_sort:
        replace_date = p.birthday.replace(year=date_now.year)
        if replace_date >= date_now.date():
            persons.append(p)
    #  The slice allows you to get the next X birthday.
    return persons[:3]


def get_birthday_month(person) -> str:
    """Gets the month of birth to be reflected in home"""
    bday_month = person.birthday.strftime("%b")
    return bday_month


def find_birthday_person():
    """Returns the birthday queriset"""
    bday_qs = User.query.filter(
        extract('month', User.birthday) == dt.datetime.today().month,
        extract('day', User.birthday) == dt.datetime.today().day).all()
    return bday_qs


def get_gif() -> str:
    """Returns a random GIF"""
    gifs = [
        'https://media.giphy.com/media/lZqlpPlT9llVm/giphy.gif',
        'https://media.giphy.com/media/26FPzWoJlFvXyiZ6E/giphy.gif',
        'https://media.giphy.com/media/9hqsyNVlf0DOU/giphy.gif',
        'https://media.giphy.com/media/45gODt1krqCOI/giphy.gif',
        'https://media.giphy.com/media/ToMjGpM3hk5UL5UMQ4o/giphy.gif',
        'https://media.giphy.com/media/W0rfEyF1UeEda/giphy.gif',
        'https://media.giphy.com/media/WUO8fZQmigr4aiqmgl/giphy.gif',
        'https://media.giphy.com/media/3ryOqmAw0s1Ve/giphy.gif',
        'https://media.giphy.com/media/7JKCXRIPRJSkiQ3TFA/giphy.gif',
        'https://media.giphy.com/media/26BRtW4zppWWjrsPu/giphy.gif',
        'https://media.giphy.com/media/26Cfluza7h46k/giphy.gif',
        'https://media.giphy.com/media/l4Kid4P3KeSvaXJok/giphy.gif',
        'https://media.giphy.com/media/l4KhKxndSqYESS5y0/giphy.gif',
        'https://media.giphy.com/media/26FPIV12CYbDSVIR2/giphy.gif',
        'https://media.giphy.com/media/26FPpSuhgHvYo9Kyk/giphy.gif',
        'https://media.giphy.com/media/equMguFgSfCOA/giphy.gif',
        'https://media.giphy.com/media/26FPtpYuSu0pHJbYA/giphy.gif',
        'https://media.giphy.com/media/Y4hRvf3iMThJBYanrA/giphy.gif',
        'https://media.giphy.com/media/WOleJLo90kPzwP08Yj/giphy.gif',
        'https://media.giphy.com/media/3o7btM5SfPJ8YlfjfW/giphy.gif',
        'https://media.giphy.com/media/fiSOwmsa55BXW/giphy.gif',
    ]
    return random.choice(gifs)


def text_generator(name: str) -> str:
    wish_you = 'творческих узбеков, розовых пони и говорящих единорогов'
    day = 'удивительный'
    phrase = (f'Поздравляем с днем рождения {name}! '
              f'В этот {day} день желаем тебе {wish_you}! '
              f'Мы рады работать с тобой, '
              f'а как сильно - расскажут ребята в комментариях!'
              f':tada::tada::tada:')
    return phrase
