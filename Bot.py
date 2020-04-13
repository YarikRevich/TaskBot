import telebot
from telebot import types
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import datetime
import threading

bot = telebot.TeleBot("1074387650:AAERuC9d1NEfVli6pd8NL5KYz6uj4C96uPg")

#Connecting to Mongo


client = MongoClient("localhost",27018)

db = client["taskbot"]
collection = db["autorization"]
Notes = []


@bot.message_handler(commands = ["start"])

#The calling of the main menu and start message

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stuff1 = types.KeyboardButton("🔓Авторизуватися")
    stuff2 = types.KeyboardButton("📝Зареєструватися")
    markup.add(stuff1,stuff2)

    bot.send_message(message.chat.id,"🔥Вітаю у TaskBot" + "\n" + "Для продовження роботи натисни кнопку Авторизуватися",reply_markup=markup)


@bot.message_handler(content_types = ["text"])

#The controlling of all buttons in the menu

def autorization(message):

    #The reaction on the pressing of the button "Sign up"

    if message.text == ("📝Зареєструватися"):
        try:
            find = collection.find({"_id":"{0.id}".format(message.from_user)})
            w = [i for i in find]
        
            if {"_id":"{0.id}".format(message.from_user)} in w:
                bot.send_message(message.chat.id,"⛔️Ви вже зареєстровані")
       
            else:
                collection.insert_one({"_id":"{0.id}".format(message.from_user)})
                bot.send_message(message.chat.id,"✅Вітаю,ви зареєструвалися")
        except pymongo.errors.DuplicateKeyError:
            bot.send_message(message.chat.id,"⛔️Ви вже зареєстровані або робите багато запросів...")	

    #The reaction on the pressing of the button "Sign in"

    if message.text == ("🔓Авторизуватися"):
        
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        
        a = [i for i in find]
        if len(a) == 0:
            bot.send_message(message.chat.id,"❌Ви не зареєстровані")
        else:           
            bot.send_message(message.chat.id,"⚠️Зачекайте....")
            time.sleep(1.5)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            part1 = types.KeyboardButton("🗒Зробити запис")
            part2 = types.KeyboardButton("🔎Продивитися усі записи")
            part3 = types.KeyboardButton("🔔Нагадування")
            part4 = types.KeyboardButton("❌Видалити аккаунт")
            markup.add(part1,part2,part3,part4)
            bot.send_message(message.chat.id,"✅Вітаю,ви увійшли в систему",reply_markup=markup)

    #The reaction on the pressing on the button "Delete the accaunt"

    if message.text == ("❌Видалити аккаунт"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stuff1 = types.KeyboardButton("🔓Авторизуватися")
        stuff2 = types.KeyboardButton("📝Зареєструватися")
        markup.add(stuff1,stuff2)
        bot.send_message(message.chat.id,"✅" + "{0.first_name}".format(message.from_user) + " " + "ви видалили аккаунт",reply_markup=markup)
        collection.find_one_and_delete({"_id":"{0.id}".format(message.from_user)})


    #The reaction on the pressing of the button "Reminders"
    
    if message.text == ("🔔Нагадування"):
        msg = bot.send_message(message.chat.id,"✏️Напишіть,що Вам нагадати")
        
        #Comming to the next function "reminders"

        bot.register_next_step_handler(msg, reminders)

    #The reaction on the pressing of the button "Look at all notes"

    if message.text == ("🔎Продивитися усі записи"):
        try:
            note = collection.find({"_id":"{0.id}".format(message.from_user)})          
            for i in note:
                k = i["notes"]           
                for s in k:
                    w = s.get("{0.id}".format(message.from_user))                      
                    main = list()
                    main.append(w)
                    o = [i for i in main if i is not None]
                    for i in o:
                        bot.send_message(message.chat.id,i)
        except KeyError:
            bot.send_message(message.chat.id,"⛔️Ви не маєте записів")

        
                
    #The reaction on the pressing of the button "Make the note"   

    if message.text == ("🗒Зробити запис"):
        msg = bot.send_message(message.chat.id,"🖍Можете робити запис" + "\n" + "❗️❗️❗️Небхідно виконувати запис у такому форматі" + "\n" + "--------------------------" + "\n" + "1)..........." + "\n" + "2)..........." + "\n" + "3)..........." + "\n" + "--------------------------")
        
        #Comming to the next function "notes"

        bot.register_next_step_handler(msg, notes)


def notes(message):

    #The message adding to Mongo

    Notes.append({"{0.id}".format(message.from_user):message.text + "\n" + "Час запису" + " " +  str(datetime.date.today())})         
    collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
    msg = bot.send_message(message.chat.id,"✅Ви зробили запис")
    
    #Comming to the main function branche

    bot.register_next_step_handler(msg, autorization)
    
    



def reminders(message):

    #The reminder adding to the database

    try:
        info = collection.find({"_id":"{0.id}".format(message.from_user)})
        for i in info:
            k = i["reminders"]              
            if len(k) >= 1:
                bot.send_message(message.chat.id,"⛔️Ви вже маєте активне нагадування")
            else:   
                collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes,"reminders":message.text})
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                stuff1 = types.KeyboardButton("🕐15 хвилин")
                stuff2 = types.KeyboardButton("🕖30 хвилин")
                stuff3 = types.KeyboardButton("🕕1 година")
                stuff4 = types.KeyboardButton("🕔2 години")
                stuff5 = types.KeyboardButton("🕓4 години")
                stuff6 = types.KeyboardButton("🕒6 годин")
                stuff7 = types.KeyboardButton("🕑12 годин")
                stuff8 = types.KeyboardButton("🕗24 години")
                markup.add(stuff1,stuff2,stuff3,stuff4,stuff5,stuff6,stuff7,stuff8)
                mess = bot.send_message(message.chat.id,"⏰Коли Вам це нагадати",reply_markup=markup)   
                bot.register_next_step_handler(mess, name_reminder)
    except KeyError:    
        collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes,"reminders":message.text})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stuff1 = types.KeyboardButton("🕐15 хвилин")
        stuff2 = types.KeyboardButton("🕖30 хвилин")
        stuff3 = types.KeyboardButton("🕕1 година")
        stuff4 = types.KeyboardButton("🕔2 години")
        stuff5 = types.KeyboardButton("🕓4 години")
        stuff6 = types.KeyboardButton("🕒6 годин")
        stuff7 = types.KeyboardButton("🕑12 годин")
        stuff8 = types.KeyboardButton("🕗24 години")
        markup.add(stuff1,stuff2,stuff3,stuff4,stuff5,stuff6,stuff7,stuff8)
        mess = bot.send_message(message.chat.id,"⏰Коли Вам це нагадати",reply_markup=markup)   
        
        #Comming to the next fuction "name_reminder"
        
        bot.register_next_step_handler(mess, name_reminder)

    

def name_reminder(message):

    #the reaction on the pressing of the button "15 minutes"

    if message.text == ("🕐15 хвилин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 15 minutes
        
        timerr = threading.Timer(30*30, main_remind, [message])
        timerr.start()
        
        
    #the reaction on the pressing of the button "30 minutes"        
            
    if message.text == ("🕖30 хвилин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 30 minutes
        
        timerr = threading.Timer(1800, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "1 hour"

    if message.text == ("🕕1 година"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 1 hour
        
        timerr = threading.Timer(3600, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "2 hours"

    if message.text == ("🕔2 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 2 hours
        
        timerr = threading.Timer(7200, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "4 hours"

    if message.text == ("🕓4 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 4 hours
        
        timerr = threading.Timer(14400, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "6 hours"

    if message.text == ("🕒6 годин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer 6 hours

        timerr = threading.Timer(21600, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "12 hours"

    if message.text == ("🕑12 годин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 12 hours

        timerr = threading.Timer(43200, main_remind, [message])
        timerr.start()

    #the reaction on the pressing of the button "24 hours"

    if message.text == ("🕗24 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
        
        #The starting of the timer on 24 hours
        
        timerr = threading.Timer(294**2, main_remind, [message])
        timerr.start()

#Called function for sending the written reminder   

def main_remind(message):
    find = collection.find({"_id":"{0.id}".format(message.from_user)})
    
    for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"])

            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            
bot.polling(none_stop=True)

