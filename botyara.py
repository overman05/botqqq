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


commands = {
    "occupy": "Занять ячейку в ближайшем свободном аппарате",
    "free": "Освободить занятую ячейку",
}


def check_user(message):
    if not db.is_user_exist(message.from_user.id):
        db.create_user(message.from_user.id)


@bot.message_handler(commands=["start", "help"])
def start(m, message):
    number = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
    button_numb = types.KeyboardButton(
        text="Отправить свой номер", request_contact=True
    )
    number.add(button_numb)
    bot.send_message(
        message.chat.id,
        "Чтобы забронировать ячейку, нам необходим ваш номер. Нажмите на кнопку, если согласны на передачу номера",
        reply_markup=number,
    )
    check_user(m)
    cid = m.chat.id
    help_text = "Доступные комманды: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


####################################################################


@bot.message_handler(commands=["occupy"])
def check_location(message):
    check_user(message)

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
    locker = lockServer.LockerAPI(server_adress, login, password)
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
    check_user(message)

    cells = db.get_user_cell(message.from_user.id)
    if len(cells) == 0:
        bot.send_message(message.chat.id, "Похоже у вас нет забронированных ячеек")
        return

    markup = types.ReplyKeyboardMarkup(
        row_width=2, one_time_keyboard=True, resize_keyboard=True
    )
    for cell in cells:
        markup.add(types.KeyboardButton(text=cell[1]))
    bot.send_message(
        message.chat.id,
        "Введите номер своей ячейки",
        reply_markup=markup,
    )

    bot.register_next_step_handler(message, free_cell_final)


def free_cell_final(message):
    locker = lockServer.LockerAPI(server_adress, login, password)
    rv = locker.free_cell(message.text)

    msg = "Ячейка освобождена"
    if rv.get("error", None) is not None:
        msg = f"Произошла ошибка {rv['error']}"

    bot.send_message(
        message.chat.id,
        msg,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    db.delete_cell_from_user(user_id=message.from_user.id, cell_id=message.text)


bot.polling(none_stop=True)
