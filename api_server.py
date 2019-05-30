import requests
import sqlite3 as lite
from flask import Flask, request, Response, render_template
# jsonfy

app = Flask(__name__)

def add_user(id_vk, name):
    sql_request = "INSERT INTO Users (id_vk, name) VALUES ('%s','%s')" % (id_vk,name)
    con = lite.connect('news_api.sqlite')
    curID = con.cursor()
    curID.executescript(sql_request)
    print(id_vk, name)
    print(curID.fetchall())
    con.close()
    return Response('{"status": "ok"}', status=200, mimetype='application/json')

@app.route('/users/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users(*args, **kwars):
    pickle_in = open('users_file.data', "rb")
    data_in = pickle.load(pickle_in)
    pickle_in.close()
    post_user = 'user'
    for user in data_in:
        if user['id'] == int(kwars['id']):
            post_user = user['name']
            post_age = user['age']
            post_type = user['type']
            post_parent = user['parent']
            post_id = user['id']

    if request.method == 'GET':
        return '''
            <html>
              <head>
                <title>User Info</title>
              </head>
              <body>
                <h1> Name - , ''' + post_user + '''</h1>
                <h1> age - , ''' + str(post_age) + '''</h1>
                <h1> type - , ''' + post_type + '''</h1>
                <h1> parent - , ''' + str(post_parent) + '''</h1>
                <h1> id - , ''' + str(post_id) + '''</h1>
              </body>
            </html>
            '''
    elif request.method == 'POST':
        return add_user(**kwars)
    elif request.method == 'PATCH':
        return update_user(**kwars)
    elif request.method == 'DELETE':
        return del_user(**kwars)
    else:
        pass

if __name__ == '__main__':
   add_user(123424,'Иван Петров')
   app.run (host = '127.0.0.1', port = 8080)
