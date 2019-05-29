import requests
import vk_api
import bs4
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
    pass

def get_all_category(user_id):
    pass

def add_category(user_id):
    pass

def delete_category(user_id):
    pass

def get_all_keywords(user_id):
    pass

def add_keywords(user_id):
    pass

def delete_keywords(user_id):
    pass

def get_news(user_id):
    pass

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:
        if event.from_user or event.from_chat: #Если написали
            if event.text == 'Привет' or event.text == 'Hi':  # Если написали заданную фразу
                vk_username = get_user_name_from_vk_id(event.user_id)
                write_msg(user_id=event.user_id,
                          message='Hi, '+vk_username,
                          )
            elif event.text == 'Список команд':
                write_msg(user_id=event.user_id,
                          message='''
                            Список команд:
                            1. Добавить пользователя
                            2. Категории новостей
                            2.1. Посмотреть категории
                            2.2. Добавить категорию
                            2.3. Удалить категорию
                            3. Ключевые слова 
                            3.1. Посмотреть ключевые слова
                            3.2. Добавить ключевые слова
                            3.3. Удалить ключевые слова
                            4. Получить новости                                 
                         ''')
            elif event.text == 'Добавить пользователя' or event.text == '1':
                add_user(event.user_id)
            elif event.text == 'Посмотреть категории' or event.text == '2.1':
                get_all_category(event.user_id)
            elif event.text == 'Добавить категорию' or event.text == '2.2':
                add_category(event.user_id)
            elif event.text == 'Удалить категорию' or event.text == '2.3':
                delete_category(event.user_id)
            elif event.text == 'Посмотреть ключевые слова' or event.text == '3.1':
                get_all_keywords(event.user_id)
            elif event.text == 'Добавить ключевые слова' or event.text == '3.2':
                add_keywords(event.user_id)
            elif event.text == 'Удалить ключевые слова' or event.text == '3.3':
                delete_keywords(event.user_id)
            elif event.text == 'Получить новости' or event.text == '4':
                get_news(event.user_id)