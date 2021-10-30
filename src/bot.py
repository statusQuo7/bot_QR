import os
from flask import Flask, request

import telebot

from config import TOKEN
from service import create_qr

server = Flask(__name__)
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@server.route("/", methods=["POST"])
def receive_update():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return {'ok': True}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    path = create_qr(message.text)
    photo = open(path, 'rb')
    bot.send_photo(message.chat.id, photo)
    os.remove(path)


@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [
            telebot.types.Update.de_json(
                request.stream.read().decode("utf-8")
            )
        ]
    )
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# import requests
# import time
# token = "2068544366:AAEvzmimlsIxI3gt4TyHMPKrgYT8767dipA"
# api_url = f"https://api.telegram.org/bot{token}/" 
# update_id = 547238385

# def send_requests(method):
#     return requests.get(api_url + method).json()
# for i in range(100):
#     time.sleep(5)
#     response = send_requests(f"getUpdates?offset={update_id}")
#     for result in response["result"]:
#         update_id = int(result["update_id"]) +1
#         chat_id = result["message"]["chat"]["id"]
#         message = result["message"]["text"]
#         send_requests(f"sendMessage?chat_id={chat_id}&text={message}")