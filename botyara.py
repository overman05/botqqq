import telebot
import lockServer

bot = telebot.TeleBot("1755603336:AAGEHorxjv_WOzRrJYGPvGuvPSxeZ26jBBI")
server_adress = "http://lockers.vendweb.ru"
login = "admin"
password = "123456"


@bot.message_handler(commands=["FreeCell"])
def free(message):
    locker = lockServer.LockerAPI(server_adress)
    locker.login(login, password)
    cells = locker.get


@bot.message_handler(commands=["OccupyCell"])
def occupy(message):
    locker = lockServer.LockerAPI(server_adress)
    locker.login(login, password)
    cells = locker.get_cells()
    location = locker.device_location()
    occupant = locker.occupy_cell()
    bot.send_chat_action(message.from_user.id, "find_location")
    bot.reply_to(message, str(occupant) + str(cells) + str(location))


bot.polling(none_stop=True)
