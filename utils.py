import datetime


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


def convert_birthday(birthday):
    birthday = datetime.date(*tuple(map(int, birthday.split('-'))))
    return birthday
