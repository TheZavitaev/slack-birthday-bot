import os
import random

from api.generator_data import *


def image_generator():
    """!!should be corrected the path"""
    path = r"C:\Yandex\slack-birthday-bot\images"
    random_filename = random.choice(
        [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    return random_filename


def text_generator(sex, name):
    dict_sex = None
    if sex == "male":
        dict_sex = MALE
    else:
        dict_sex = FEMALE
    our = dict_sex.get("our")
    which = random.choice(dict_sex.get("which"))
    bad_situation = random.choice(dict_sex.get("bad_situation"))
    from_which = random.choice(GENERAL.get("from"))
    good_situation = random.choice(GENERAL.get("good_situation"))
    which_day = random.choice(GENERAL.get("which_day"))
    time_period = random.choice(GENERAL.get("time_period"))
    funny_one = random.choice(GENERAL.get("funny_one"))

    phrase = f"Сегодня {name} празднует свой День Рождения! " \
             f"{our} {which} {name}! От {from_which} и всех без исключения," \
             f" поздравляем Вас с Днем Рождения! Желаем Вам в сложных ситуациях" \
             f" всегда быть {bad_situation}, а в хороших - {good_situation}. " \
             f"Пусть этот день будет {which_day} для Вас, как и {time_period}. " \
             f"Да {funny_one}!"
    return phrase


if __name__ == "__main__":
    text_generator(sex, name)
    image_generator()
