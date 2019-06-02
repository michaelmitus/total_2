import requests
import vk_api
import bs4
import json
from newsapi import NewsApiClient
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType

vk_token = '9f6ef21d1fa6d22f2cbdff6eaf02dd8a52f05e3e141f0293b6f934006a26ae3d8b4780807cd39efbc07c8'
vk_session = vk_api.VkApi(token=vk_token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def write_msg(user_id, message):
    vk.messages.send(user_id=user_id,
                     message=message,
                     random_id=randint(1254353245, 2345378568347568347563453245345345))

def clean_all_tag_from_str(string_line):
    """
    Очистка строки stringLine от тэгов и их содержимых
    :param string_line: Очищаемая строка
    :return: очищенная строка
    """
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result

def get_user_name_from_vk_id(user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    user_name = clean_all_tag_from_str(bs.findAll("title")[0])

    return user_name.split()[0]

def add_user(user_id):
    response = requests.post('http://localhost:8080/users/',
                             params = {'vk_id': user_id, 'name': get_user_name_from_vk_id(user_id)})
    print(response)
    pass

def get_user(user_id):
    response = requests.get('http://localhost:8080/users/',
                             params = {'vk_id': user_id})
    return response.text

def get_all_keywords(user_id):
    pass

def add_keywords(user_id):
    pass

def delete_keywords(user_id):
    pass

def get_news(user_id):
    pass

def vk_print(user_id, title, menu_items):
    msg_text = title + '\n'
    for items in range(len(menu_items)):
        msg_text = msg_text + (str(items + 1) + '. ' + menu_items[items] + '\n')
    write_msg(user_id=user_id,
              message=msg_text)

def vk_menu(user_id, title, menu_items):
    vk_print(user_id, title, menu_items)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Слушаем longpoll, если пришло сообщение то:
            if event.from_user or event.from_chat:  # Если написали
                return event.text

def registration(user_id):
    while True:
        result_choice = vk_menu(user_id,
                                'Регистрация:',
                                ('Добавить пользователя', 'Изменить пользователя', 'Удалить пользователя', 'Выход'))
        if result_choice in ('1', 'Добавить пользователя'):
            write_msg(user_id=user_id,
                      message='Вы уже зарегистрированы')
            return 1
        elif result_choice in ('2', 'Изменить пользователя'):
            write_msg(user_id=user_id,
                      message='Не хватает прав доступа')
            return 2
        elif result_choice in ('3', 'Удалить пользователя'):
            write_msg(user_id=user_id,
                      message='Не хватает прав доступа')
            return 3
        elif result_choice in ('0', '4'):
            return 0

def get_all_category():
#    def list_of_filters(params, **filters):
    api_key = 'c6b4dff59361415dada7968f05685325'
    newsapi = NewsApiClient(api_key)
    all_sources = newsapi.get_sources()
    sources = all_sources['sources']
    selections = set()
    for news_number in range(0, len(all_sources['sources'])):
        selections.add(sources[news_number]['category'])
    return list(selections)

def get_category(user_id):
    response = requests.get('http://localhost:8080/subscriptions/categories/',
                             params = {'vk_id': user_id})
    todos = json.loads(response.text)
    print(response)
    print(todos)
    print(type(todos))
    print(type(response.text))
    return todos
    pass

def add_category(user_id,category_id):
    response = requests.post('http://localhost:8080/subscriptions/categories/',
                             params = {'vk_id': user_id, 'category_id': category_id})
    return response.text
    pass

def delete_category(user_id):
    pass

def category_of_news(user_id):
    while True:
        result_choice = vk_menu(user_id,
                                'Работа с категориями:',(
                                    'Посмотреть все доступные категории',
                                    'Посмотреть подписки на категории',
                                    'Добавить подписку на категорию',
                                    'Удалить подписку на категорию',
                                    'Выход'
                                 ))
        if result_choice in ('1', 'Посмотреть все доступные категории'):
            msg_text = 'Все доступные категории' + '\n'
            selection = list(get_all_category())
            for items in range(len(selection)):
                msg_text = msg_text + selection[items] + '\n'
            write_msg(user_id=user_id,
                      message=msg_text)

        if result_choice in ('2', 'Посмотреть подписки на категории'):
            write_msg(user_id=user_id,
                      message=get_category(user_id))
            selection = list(get_category(user_id))
            msg_text = ' '
            for items in range(len(selection)):
                msg_text = msg_text + str(selection[items])+ '\n'
            write_msg(user_id=user_id,
                      message=msg_text)




        elif result_choice in ('20', 'Добавить все категории'):
            add_category(0, 0)
            return 20
        elif result_choice in ('0', 'Выход'):
            return 0

#elif event.text == 'Посмотреть подписки категории' or event.text == '2.1':
#get_category(event.user_id)
#elif event.text == 'Добавить подписку на категорию' or event.text == '2.2':
#add_category(event.user_id)
#elif event.text == 'Удалить подписку на категорию' or event.text == '2.3':
#delete_category(event.user_id)


def main_menu(user_id):
    while True:
        result_choice = vk_menu(event.user_id,
                                'Список разделов:',
                                ('Регистрация', 'Категории новостей', 'Ключевые слова', 'Новости'))
        if result_choice in ('1', 'Регистрация'):
            registration(event.user_id)
            return 1

        elif result_choice in ('2', 'Категории новостей'):
            category_of_news(user_id)
            return 2


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:
        if event.from_user or event.from_chat: #Если написали
            if get_user(event.user_id)=='None':
                if event.text == 'Добавить пользователя' or event.text == '1':
                    add_user(event.user_id)
                    vk_username = get_user_name_from_vk_id(event.user_id)
                    write_msg(user_id=event.user_id,
                              message='Отлично, ' + vk_username + ', теперь ты в наших рядах',
                              )
                else:
                    vk_username = get_user_name_from_vk_id(event.user_id)
                    write_msg(user_id=event.user_id,
                              message='Привет, '+vk_username)
                    result_choice = vk_menu(event.user_id,
                                            'Тебя пока нет в нашей базе данных, желаешь зарегистрироваться?',
                                            ('Зарегистрироваться','Нет'))
            else:
                if event.text == 'Привет' or event.text == 'Hi':  # Если написали заданную фразу
                    vk_username = get_user_name_from_vk_id(event.user_id)
                    write_msg(user_id=event.user_id,
                              message='Привет, '+vk_username,
                              )
                elif event.text == 'Список команд' or event.text == '0':
                    main_menu(event.user_id)


                elif event.text == 'Проверка':
                    write_msg(user_id=event.user_id,
                              message=get_user(event.user_id))

#                    msg_text = "Все доступные категории новостей: \n"
#                    for news_number in range(0, len(selections)):
#                        msg_text = msg_text+(str(news_number + 1) + '. ' + selections[news_number]+'\n')
#                    msg_text = msg_text + ('0. Все' )
#                    write_msg(user_id=event.user_id,
#                              message=msg_text
#                              )
                elif event.text == 'Посмотреть ключевые слова' or event.text == '3.1':
                    get_all_keywords(event.user_id)
                elif event.text == 'Добавить ключевые слова' or event.text == '3.2':
                    add_keywords(event.user_id)
                elif event.text == 'Удалить ключевые слова' or event.text == '3.3':
                    delete_keywords(event.user_id)
                elif event.text == 'Получить новости' or event.text == '4':
                    get_news(event.user_id)