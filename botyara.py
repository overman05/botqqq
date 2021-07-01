import telebot
from telebot import types
import lockServer
import config
import db
import logging
from geopy.distance import geodesic

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.TOKEN)
server_adress = config.SERVER_ADDRESS
login = "admin"
password = "123456"
db = db.DB()


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    logger.debug("start")
    db.create_user(user_id)


@bot.message_handler(commands=["test"])
def get_lock(msg):
    locker = lockServer.LockerAPI(server_adress)
    locker.login(login, password)
    rv = locker.device_location()
    bot.reply_to(msg, rv)


####################################################################


@bot.message_handler(commands=["occupy"])
def check_location(message):
    keyboard = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
    button_geo = types.KeyboardButton(
        text="Отправить местоположение", request_location=True
    )
    keyboard.add(button_geo)
    bot.send_message(
        message.chat.id,
        "Чтобы найти удобный для вас автомат, нам необхоимо ваше местоположение. Нажмите на кнопку если согласны на передачу своих геоданных",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(message, find_device)


def find_device(message):
    locker = lockServer.LockerAPI(server_adress)
    locker.login(login, password)
    rv = locker.device_location()

    device = rv[0]
    u_long = message.location.longitude
    u_lat = message.location.latitude
    d_long = float(rv[0]["longitude"])
    d_lat = float(rv[0]["latitude"])
    m = geodesic((u_long, u_lat), (d_long, d_lat))
    for i, el in enumerate(rv[1:]):
        d_long = float(el["longitude"])
        d_lat = float(el["latitude"])
        t = geodesic((u_long, u_lat), (d_long, d_lat))
        if t < m:
            m = t
            device = el

    bot.send_location(
        message.chat.id,
        device["latitude"],
        device["longitude"],
        reply_markup=types.ReplyKeyboardRemove(),
    )
    rv = locker.occupy_cell(device["id"])
    bot.reply_to(
        message, f"Занята ячейка с номером {rv['number']} и паролем {rv['user_key']}"
    )
    db.add_cell_to_user(str(message.from_user.id), rv["id"])


##################################################################


@bot.message_handler(commands=["free"])
def free_cell(message):
    cells = db.get_user_cell(message.from_user.id)
    markup = types.ReplyKeyboardMarkup()

    for cell in cells:
        markup.add(types.KeyboardButton(text=cell[1]))
    bot.send_message(
        message.chat.id,
        "Введите номер своей ячейки",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, free_cell_final)


def free_cell_final(message):
    locker = lockServer.LockerAPI(server_adress)
    locker.login(login, password)
    locker.free_cell(message.text)
    bot.send_message(
        message.chat.id,
        "Ячейка освобождена",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    db.delete_cell_from_user(user_id=message.from_user.id, cell_id=message.text)


bot.polling(none_stop=True)
