import datetime as dt
from itertools import groupby

from sqlalchemy import extract

from bot import User, db


def get_or_create(session, model, **kwargs):
    """Получает экземпляр модели по запросу, если такового нет - создает его"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def bool_convert(string: str) -> bool:
    """Конвертирует строку в Bool"""
    if string == 'True':
        return True
    else:
        return False


def get_channel_id(data: dict) -> str:
    """Возвращает id канала из payload"""
    channel = data['channel']
    return channel


def convert_birthday(birthday: str):
    birthday = dt.date(*tuple(map(int, birthday.split('-'))))
    return birthday


def get_birthday_persons() -> list:
    date_now = dt.datetime(dt.datetime.today().year, dt.datetime.today().month,
                           dt.datetime.today().day)

    persons = []

    bday_sort = User.query.group_by(
        extract('month', User.birthday),
        extract('day', User.birthday)).filter(
        extract('month', User.birthday) >= dt.datetime.today().month).all()

    for p in bday_sort:
        replace_date = p.birthday.replace(year=date_now.year)
        if replace_date > date_now.date():
            persons.append(p)

    return persons[:3]


def get_birthday_month(person):
    bday_month = person.birthday.strftime("%b")
    return bday_month
