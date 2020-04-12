import telebot
from telebot import types
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import datetime

bot = telebot.TeleBot("1074387650:AAERuC9d1NEfVli6pd8NL5KYz6uj4C96uPg")


client = MongoClient("localhost",27018)

db = client["taskbot"]
collection = db["autorization"]
Notes = []
Reminders = []
Date_reminders = []


@bot.message_handler(commands = ["start"])


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stuff1 = types.KeyboardButton("Авторизуватися")
    stuff2 = types.KeyboardButton("Зареєструватися")
    markup.add(stuff1,stuff2)

    bot.send_message(message.chat.id,"Вітаю у TaskBot" + "\n" + "Для продовження роботи натисни кнопку Авторизуватися",reply_markup=markup)


@bot.message_handler(content_types = ["text"])

def autorization(message):
    if message.text == ("Зареєструватися"):
        try:
            find = collection.find({"_id":"{0.id}".format(message.from_user)})
            w = [i for i in find]
        
            if {"_id":"{0.id}".format(message.from_user)} in w:
                bot.send_message(message.chat.id,"Ви вже зареєстровані")
       
            else:
                collection.insert_one({"_id":"{0.id}".format(message.from_user)})
                bot.send_message(message.chat.id,"Вітаю,ви зареєструвалися")
        except pymongo.errors.DuplicateKeyError:
            bot.send_message(message.chat.id,"Ви вже зареєстровані або робите багато запросів...")	



    if message.text == ("Авторизуватися"):
        
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        
        a = [i for i in find]
        if {"_id"} in a == "{0.id}".format(message.from_user):
            bot.send_message(message.chat.id,"Ви не зареєстровані")
        else:           
            bot.send_message(message.chat.id,"Зачекайте....")
            time.sleep(1.5)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            part1 = types.KeyboardButton("Зробити запис")
            part2 = types.KeyboardButton("Продивитися усі записи")
            part3 = types.KeyboardButton("Нагадування")
            part4 = types.KeyboardButton("Вийти з аккаунту")
            markup.add(part1,part2,part3,part4)
            bot.send_message(message.chat.id,"Вітаю,ви увійшли в систему",reply_markup=markup)



    if message.text == ("Вийти з аккаунту"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stuff1 = types.KeyboardButton("Авторизуватися")
        stuff2 = types.KeyboardButton("Зареєструватися")
        markup.add(stuff1,stuff2)
        bot.send_message(message.chat.id,"{0.first_name}".format(message.from_user) + " " + "ви вийшли з аккаунту",reply_markup=markup)



    
    if message.text == ("Нагадування"):
        msg = bot.send_message(message.chat.id,"Напишіть,що Вам нагадати")
        bot.register_next_step_handler(msg, reminders)
        
    if message.text == ("Продивитися усі записи"):
        try:
            note = collection.find({"_id":"{0.id}".format(message.from_user)})
            for i in note:
                bot.send_message(message.chat.id,i["notes"])
        except KeyError:
            bot.send_message(message.chat.id,"Ви не маєте нагадувань")

        
                
            

    if message.text == ("Зробити запис"):
        msg = bot.send_message(message.chat.id,"Можете робити запис" + "\n" + "Небхідно виконувати запис у такому форматі" + "\n" + "--------------------------" + "\n" + "1)..........." + "\n" + "2)..........." + "\n" + "3)..........." + "\n" + "--------------------------")
        bot.register_next_step_handler(msg, notes)


def notes(message): 
    print(Notes)  
    Notes.append(message.text + "\n" + "Час запису" + " " +  str(datetime.date.today()))
    collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
    msg = bot.send_message(message.chat.id,"Ви зробили запис")
    bot.register_next_step_handler(msg, autorization)
    
    



def reminders(message):     
        
        l = len(Reminders)
        if l >= 1:
            bot.send_message(message.chat.id,"Ви вже маєте активне нагадування")
        else:   
            Reminders.append(message.text)    
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes,"reminders":Reminders})
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            stuff1 = types.KeyboardButton("15 хвилин")
            stuff2 = types.KeyboardButton("30 хвилин")
            stuff3 = types.KeyboardButton("1 година")
            stuff4 = types.KeyboardButton("2 години")
            stuff5 = types.KeyboardButton("4 години")
            stuff6 = types.KeyboardButton("6 годин")
            stuff7 = types.KeyboardButton("12 годин")
            stuff8 = types.KeyboardButton("24 години")
            markup.add(stuff1,stuff2,stuff3,stuff4,stuff5,stuff6,stuff7,stuff8)
            mess = bot.send_message(message.chat.id,"Коли Вам це нагадати",reply_markup=markup)   
            bot.register_next_step_handler(mess, name_reminder)
   
    

def name_reminder(message):
    if message.text == ("15 хвилин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(900)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("30 хвилин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(1800)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("1 година"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(3600)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("2 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(7200)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("4 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(14400)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("6 годин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(21600)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("12 годин"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(43200)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    if message.text == ("24 години"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("Зробити запис")
        part2 = types.KeyboardButton("Продивитися усі записи")
        part3 = types.KeyboardButton("Нагадування")
        part4 = types.KeyboardButton("Вийти з аккаунту")
        markup.add(part1,part2,part3,part4)
        bot.send_message(message.chat.id,"Нагадування зроблене!",reply_markup=markup)
        time.sleep(86400)
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        for whole_list in find:
            bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  whole_list["reminders"][0])
            collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
            del Reminders[0]
    #try:
        
        #Date_reminders.append(eval(message.text))
        #date = datetime.datetime.today()
        #dat = date.strftime("%H.%M")
        
        #if Date_reminders == dat:
        #    bot.send_message(message.chat.id,"Good")
    #except (NameError, SyntaxError):
    #    msg = bot.send_message(message.chat.id,"Введіть коректний час")
    #    bot.register_next_step_handler(msg, name_reminder)
bot.polling(none_stop=True)

