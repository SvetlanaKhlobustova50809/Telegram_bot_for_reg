import telebot

import mysql.connector

from telebot import types


bot = telebot.TeleBot('5550305703:AAE8br7Ke_683BU92MYo0S8SvDPVZ_P633E')

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Boruto505cat+",
  port="3306",
  database="datebase"
)


cursor = db.cursor()
# Удаление строк
sql = "DELETE FROM users WHERE id in (25,26)"

cursor.execute(sql)

db.commit()

# Создание таблицы вручную
# cursor.execute("CREATE DATABASE datebase")

# cursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255))")

# cursor.execute("ALTER TABLE users ADD COLUMN (Age INT)")

# sql = "INSERT INTO users (first_name, last_name,age,user_id) VALUES (%s, %s,%s, %s)"
# val = ("Sveta", "Veber",19,1)
# cursor.execute(sql, val)
#
# db.commit()

#
# cursor.execute("SHOW DATABASES")
#
# for x in cursor:
#   print(x)

name=''
surname = '';
age = 0;
user_data={}
@bot.message_handler(content_types=['text'])

def start(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию

    global name;
    user_id = message.from_user.id
    # user_data[user_id] = User(message.text)
    name=message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname
    user_id = message.from_user.id
    # user = user_data[user_id]
    # user.surname = message.text
    surname=message.text
    # user_data[user_id] = User(message.text)
    bot.send_message(message.from_user.id,'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age;
    global user_id
    user_id = message.from_user.id
    while age == 0: #проверяем что возраст изменился
        try:
            age = int(message.text) #проверяем, что возраст введен корректно
            keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
            key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
            keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
            key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
            keyboard.add(key_no);
            question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?';
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        except Exception:
            bot.send_message(message.from_user.id, 'ошибка: неправильно ввели возраст или уже зарегистрированы!');


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        #код сохранения данных, или их обработки
        sql = "INSERT INTO users (first_name, last_name,age,user_id) VALUES (%s, %s,%s, %s)"
        val = (name, surname, age, user_id)
        cursor.execute(sql, val)

        db.commit()
        bot.send_message(call.message.chat.id, 'Запомню : )'
                                               'Если желаете продолжить, напишите /reg')

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Не запишу, но ещё есть шанс всё изменить : )')

bot.polling(none_stop=True, interval=0)