# slack-birthday-bot
Slack-bot for the Yandex.Practicum team.

## В общем.
Первым делом идем сюда: https://github.com/TheZavitaev/slack-birthday-bot/projects/1
Тут я вел проект, что сделано, что не сделано, ТЗ, сценарии, мои мысли, ссылки.

Далее идем сюда: https://api.slack.com/start/building/bolt-python
Знакомимся с общей концепцией, работой с АПИ, какие есть токены, скоупы и т.д.

___
Написан на Python 3.8.

Чтобы его запустить:
* ```git clone https://github.com/TheZavitaev/slack-birthday-bot.git```
* ``` pip install -r requirements.txt```

Далее все как и [тут](https://api.slack.com/start/building/bolt-python):
* Создаем тестовый воркспейс слака 
* Создаем тестовое слак приложение
* Забираем секреты 
* Создаем ".env" по образу и подобию .env.template и кладем в него секреты
* На порте 3000 запускаем ngrok, забираем ссылку
* Вставляем эту ссылку в Event Subscriptions и Interactivity & Shortcuts
* Развлекаемся

У меня бот подписан был на следующие события:
* app_home_opened
* message.channels
* channels:history
* message.groups
* groups:history
* message.im
* im:history
* message.mpim

___
В настоящий момент бот умеет:
* Создавать юзера в БД;
* Получать информацию о его дне рождении;
* Получать согласие на отправку поздравления в общий канал;
* Брать рандомную гифку, генерировать простое поздравление;
* Админ по кнопке может отправить сообщение в общий канал;
* Админ по кнопке может отправить поздравление в общий канал;
___
То, что нужно сделать находится [тут](https://github.com/TheZavitaev/slack-birthday-bot/projects/1)

Документация по библиотеке [тут](https://slack.dev/bolt-python/concepts)
