import requests
import sqlite3 as lite
import json
from newsapi import NewsApiClient
from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)

def add_user(id_vk, name):
    sql_request = "INSERT INTO Users (id_vk, name) VALUES ('%s','%s')" % (id_vk,name)
    con = lite.connect('news_api.sqlite')
    curID = con.cursor()
    curID.executescript(sql_request)
    resp = curID.fetchone()
    con.close()
    print(resp)
    return str(resp)

def get_user(vk_id):
    sql_request = "SELECT * FROM Users WHERE id_vk = "+str(vk_id)
    con = lite.connect('news_api.sqlite')
    curID = con.cursor()
    curID.execute(sql_request)
    resp = curID.fetchone()
    con.close()
    return str(resp)

@app.route('/users/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users(*args, **kwargs):
    post_user = 'user'
    for user in data_in:
        if user['id'] == int(kwars['id']):
            post_user = user['name']
            post_age = user['age']
            post_type = user['type']
            post_parent = user['parent']
            post_id = user['id']

@app.route('/users/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def all_users(*args, **kwargs):
    if request.method == 'GET':
        return get_user(request.args.get('vk_id'))
    elif request.method == 'POST':
        print('Добавление в базу ',request.args.get('vk_id'),request.args.get('name'))
        return add_user(request.args.get('vk_id'),request.args.get('name'))
    elif request.method == 'PATCH':
        return update_user(**kwars)
    elif request.method == 'DELETE':
        return del_user(**kwars)
    else:
        pass

def get_all_category():
#    def list_of_filters(params, **filters):
    api_key = 'c6b4dff59361415dada7968f05685325'
    newsapi = NewsApiClient(api_key)
    all_sources = newsapi.get_sources()
    sources = all_sources['sources']
    selections = set()
    for news_number in range(0, len(all_sources['sources'])):
        selections.add(sources[news_number]['category'])
    print(str(list(selections)))

#    for news_number in range(0, len(selections)):
#        print(str(news_number+1)+'. '+list(selections)[news_number])
    print('0. Все')
    return list(selections)

def add_all_category():
#    msg_text = "Все доступные категории новостей: \n"
    selections = get_all_category()
    for news_number in range(0, len(selections)):
        try:
            sql_request = "INSERT INTO Category (Text) VALUES ('%s')" % (selections[news_number])
            con = lite.connect('news_api.sqlite')
            curID = con.cursor()
            curID.executescript(sql_request)
            con.close()
        except:
            print('Ошибка добавления')
            return "Error"
    return 'Ok'

def add_category(vk_id, category_id):
#    Добавление подписок на категории
    sql_request = "INSERT INTO Users_Category (CategoryID, UserID) VALUES ('%s','%s')" % (category_id, vk_id)
    con = lite.connect('news_api.sqlite')
    curID = con.cursor()
    curID.executescript(sql_request)
    con.close()
    return 'Ok'

def get_category(vk_id):
    sql_request = '''
                    SELECT Category.Text FROM Category
                    JOIN Users_Category ON Category.ID = Users_Category.CategoryID 
                    WHERE Users_Category.UserID = '''+str(vk_id)
    con = lite.connect('news_api.sqlite')
    curID = con.cursor()
    curID.execute(sql_request)
    resp = curID.fetchall()
    con.close()
    print(jsonify(resp))
    return jsonify(resp)

@app.route('/subscriptions/categories/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def categorys(*args, **kwargs):
    if request.method == 'GET':
        return get_category(request.args.get('vk_id'))
    elif request.method == 'POST':
        if request.args.get('vk_id') == 0:
            return add_all_category()
        else:
            return add_category(request.args.get('vk_id'),request.args.get('category_id'))
    elif request.method == 'PATCH':
        return update_user(**kwars)
    elif request.method == 'DELETE':
        return del_user(**kwars)
    else:
        return 'None'



if __name__ == '__main__':
   app.run (host = '127.0.0.1', port = 8080)
