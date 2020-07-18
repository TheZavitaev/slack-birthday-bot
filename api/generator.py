import os
import random

""" dict - maybe move it to another file """

GENERAL = {
    "from": ["всей души", "всего сердца", "сердца и почек", "полных легких",
             "чистого сердца", "ясных мозгов", ],
    "good_situation": ["на коне", "на слоне", "на жирафе", "на верблюде",
                       "на носороге", "на единороге", "на драконе",
                       "на фениксе", ],
    "which_day": ["незабываемым", "чудесным", "отпадным", "интригующим",
                  "чарующим", "зажигательным", "безупречным", "волшебным",
                  "грандионым", "искромётным", "увлекательным", "магическим",
                  "незаурядным", "необычным", "непринуждённым", "озорным",
                  "первоклассным", "удивительным", "фантастическим", ],
    "time_period": ["весь следующий век", "всё следующее столетие",
                    "всё следующее тысячелетие", "весь следующий миллион лет",
                    "весь следующий квадриллион лет", ],
    "funny_one": ["прибудет с Вами мишура", "прибудут с Вами шарики",
                  "прибудут с Вами тортики", "прибудут с Вами конфетки",
                  "прибудут с Вами танцы", "прибудут с Вами пляски",
                  "прибудут с Вами песни", "прибудет с Вами сила",
                  "прибудут с Вами хороводы", "прибудут с Вами колокольчики",
                  "прибудет с Вами конфетти"]
}

MALE = {
    "our": "Наш",
    "which": ["гениальный", "неподражаемый", "незаменимый",
              "целеустремленный", "общительный", "надежный", "ответственный",
              "веселый", "демократичный", "доблестный", "достопочтенный",
              "дружелюбный", "заботливый", "зажигательный", "жизнерадостный",
              "замечательный", "интеллигентный", "искренний", "исключительный",
              "калифицированный", "конкурентноспособный", "констуктивный",
              "компанейский", "корректный", "креативный", "культурный",
              "логичный", "многогранный", "наблюдательный", ],
    "bad_situation": ["настороже", "в исключительно хорошем настроении",
                      "ни при чём", "не виноватым", "оптимистом",
                      "как рыба в воде", ],
}
FEMALE = {
    "our": "Наша",
    "which": ["жизнерадостная", "шикарная", "бесподобная",
              "бесценная", "блестящая", "грациозная", "дипломатичная",
              "зажигательная", "завораживающая", "инициативная", "лучезарная",
              "мелодичная", "неповторимая", "обворожительнаяя", "окрыляющая",
              "очаровательная", "потрясная", "разносторонняя", "роскошная",
              "солнечная", "талантливая", "уникальная", "улыбчивая",
              "феноменальная", "цветущая", "яркая", ],
    "bad_situation": ["настороже", "в исключительно хорошем настроении",
                      "ни при чём", "не виноватой", "оптимисткой",
                      "как рыба в воде", ],
}

def image_generator():
    """!!should correct the path
        gonna do it lately """
    path = r"C:\Yandex\slack-birthday-bot\images"
    random_filename = random.choice(
        [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    # print(random_filename)
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
    phrase = f"Сегодня {name} празднует свой День Рождения! "\
             f"{our} {which} {name}! От {from_which} и всех без исключения," \
             f" поздравляем Вас с Днем Рождения! Желаем Вам в сложных ситуациях" \
             f" всегда быть {bad_situation}, а в хороших - {good_situation}. " \
             f"Пусть этот день будет {which_day} для Вас, как и {time_period}. " \
             f"Да {funny_one}!"
    # print(phrase)
    return phrase

if __name__ == "__main__":
    text_generator("female", "Светлана")
    # print("-------------------")
    text_generator("male", "Сергей")
    image_generator()

