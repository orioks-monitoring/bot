# ОРИОКС Мониторинг Бот

## Что это?
[ОРИОКС Мониторинг](https://t.me/orioks_monitoring_bot) - это Бот для отслеживания изменений в образовательной электронной среде НИУ МИЭТ [orioks.miet.ru](https://orioks.miet.ru/) на платформе [Telegram](https://core.telegram.org/bots/api).

## Зачем это?
Бот создан для автоматизации контроля над учебным процессом. Он помогает студентам удобным способом получать информацию о своей успеваемости и новостях в режиме реального времени. 

## Как это работает?
Студент авторизируется в ОРИОКС через [Бота](https://t.me/orioks_monitoring_bot). Каждые 15 минут запускается скрипт, который сравнивает данные, хранящяется на сервере, с информацией от запроса HTTP-клиента[^1] [AIOHTTP](https://docs.aiohttp.org/en/stable/). При появлении изменений студенту автоматически отправляется сообщение о них.

## Какие функции есть у этого бота?
На данный момент в Боте реализованы следующие функции оповещений по категориям:
- раздел "Обучение": изменения баллов в накопительно-балльной системе (НБС)

  <img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/grades.png" width="400">
  
- раздел "Новости": публикация общих новостей (новости по дисциплинам *(coming soon)*);

  <img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/news.png" width="400">
  
- раздел "Ресурсы": изменения и загрузка файлов по дисциплине *(coming soon)*;
- раздел "Домашние задания": изменения статусов отправленных работ;

  <img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/homework2.png" width="400">
  <br>
  <img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/homework1.png" width="400">
  
- раздел "Заявки": изменения статусов заявок на обходной лист, материальную помощь, социальную стипендию, копии документов, справки.

  <img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/requests.png" width="400">


## Почему это безопасно?

Наша политика хранения и обработки данных:

* параметры для входа (логин и пароль) обрабатываются автоматически и единократно, они не хранятся на сервере ни в каком виде;
* ответы, сохраняемые скриптом от посылаемых им запросов, не содержат информацию, позволяющую однозначно идентифицировать и обезличить пользователя;
* хранящиеся на сервере данные используются только для отправки сообщений пользователям и не передаются третьим лицам;
* в логи работы записывается только техническая информация о работе Бота, ни одно сообщение не логгируется.

Наш Бот - проект с открытым исходным кодом. Он создан действующими студентами МИЭТ для помощи нашему университетскому сообществу.

<img src="https://github.com/orioks-monitoring/bot/blob/gh-pages/img/faq/open-source-logo.png" width="100">

Проект такого типа подразумевает возможность пользователей использовать код самостоятельно. Вы можете просмотреть реализуемые скрипты и самостоятельно решить, пользоваться ли данным готовым Ботом, или выбрать [вариант для продвинутых пользователей](#какие-возможности-есть-еще-для-продвинутых-пользователей) с реализацией на своем собственном сервере. 

## Какие возможности есть еще? *(для продвинутых пользователей)*
Есть возможность запустить настоящего Бота на собственном сервере, используя [инструкцию](#настройка-на-собственном-сервере). 

Более того:

Существуют два независимых скрипта[^2], с помощью которых, имея опыт работы с [GitHub](https://github.com/) и API, можно реализовать работу скрипта на основе [GitHub Actions](https://docs.github.com/en/actions) с выбором платформы для оповещений ([API VK](https://dev.vk.com/) или [API Telegram](https://core.telegram.org/bots/api)) и хранением данных с помощью [API Yandex Disk](https://yandex.ru/dev/disk/rest/):
- [ORIOKS MONITORING SELENIUM](https://github.com/llirrikk/orioks-monitoring-selenium) — работает, используя [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/);
- [ORIOKS MONITORING API](https://github.com/llirrikk/orioks-monitoring-api) работает на основе [ORIOKS STUDENT API](https://orioks.gitlab.io/student-api/).[^3][^4]

### Настройка на собственном сервере

1. Клонирование репозитория и смена директории
```bash
git clone https://github.com/orioks-monitoring/bot.git && cd bot
```

2. Создание вируального окружения и его активация
```bash
python3 -m venv venv && source venv/bin/activate
```

3. Установка необходимых зависимостей в виртуальное окружение
```bash
pip install -r requirements.txt
```

4. Получение [API токена для Telegram бота](https://core.telegram.org/bots/api)
    1. Пишем `/newbot` сюда: [@BotFather](https://t.me/botfather).
    2. Запоминаем `TELEGRAM_BOT_API_TOKEN` токен Telegram бота.
    3. Узнаём свой *Telegram ID*, например, так:
        1. Пишем `/start` сюда: [@userinfobot](https://t.me/userinfobot).
        2. Запоминаем свой *Telegram ID* (для использования в `TELEGRAM_ADMIN_IDS_LIST`).

5. Копирование файла с примерами установки переменных окружения в файл `setenv.sh`. Замена примеров на реальные значения
```bash
cp setenv-example.sh setenv.sh && vim setenv.sh
```

6. Активация переменных окружения (будут сброшены после выхода из сессии вируального окружения)
```bash
source setenv.sh
```

7. Запуск Бота
```bash
python main.py
```



## У меня есть предложение / Я нашел баг. С кем можно связаться?
Вы можете написать в нашу поддержку — [@orioks_monitoring_support](https://t.me/orioks_monitoring_support), а так же создать [Issues](https://github.com/orioks-monitoring/bot/issues) в репозитории.



[^1]: HTTP-клиент - это библиотека методов выполнения [HTTP-запросов](https://habr.com/ru/post/215117/)

[^2]: В обоих скриптах, [ORIOKS MONITORING SELENIUM](https://github.com/llirrikk/orioks-monitoring-selenium) и [ORIOKS MONITORING API](https://github.com/llirrikk/orioks-monitoring-api), *реализована только функция оповещений по разделу "Обучение"*.

[^3]: [ORIOKS STUDENT API](https://orioks.gitlab.io/student-api/), по сравнению с [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/), имеет ряд весомых ограничений (не позволяет получить всю необходимую информацию и имеет значительную задежку в считывании выставленных баллов в НБС).

[^4]: Решение из настоящего репозитория на основе [AIOHTTP](https://docs.aiohttp.org/en/stable/) является наиболее эффективным и полным среди приведенных скриптов.
