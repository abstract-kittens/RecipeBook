# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с логами.
import logging

# Импортируем модуль для работы с API Алисы
from alice_sdk import AliceRequest, AliceResponse

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

from flask_ngrok import run_with_ngrok

from handle_dialog import handle_dialog

from pymongo import MongoClient

app = Flask(__name__)
run_with_ngrok(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
session_storage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
#    client = MongoClient('localhost', 27017)
    client = MongoClient('mongodb://admin:adminadmin1@ds241298.mlab.com:41298/heroku_t04mh511?retryWrites=false')
#    db = client.db
    db = client['heroku_t04mh511']
    
    alice_request = AliceRequest(request.json)
    logging.info('Request: {}'.format(alice_request))

    alice_response = AliceResponse(alice_request)

    user_id = alice_request.user_id      
    
    alice_response, session_storage[user_id] = handle_dialog(
        alice_request, alice_response, session_storage.get(user_id), db
    )
    logging.info('Response: {}'.format(alice_response))

    return alice_response.dumps()


if __name__ == '__main__':
    app.run()