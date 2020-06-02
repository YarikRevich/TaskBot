import telebot
from telebot import types
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
import datetime
import threading
import os
import re

bot = telebot.TeleBot("1074387650:AAERuC9d1NEfVli6pd8NL5KYz6uj4C96uPg")

#Connecting to Mongo


client = MongoClient("localhost",27017)
db = client["taskbot"]
collection = db["autorization"]
Notes = []
site = db["tasksite"]



@bot.message_handler(commands = ["start"])

#The calling of the main menu and start message

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stuff1 = types.KeyboardButton("🔓Авторизуватися")
    stuff2 = types.KeyboardButton("📝Зареєструватися")
    markup.add(stuff1,stuff2)

########################################################################
    #Global Variables
    
    global Check_time
    global checker_v2
    global checker_v3
    global checker_v4
    global checker
    global Check
    global user_email


    user_email = {"{0.id}".format(message.from_user):0}
    Check = {"{0.id}".format(message.from_user):0}
    Check_time = {"{0.id}".format(message.from_user):0}
 


    checker = threading.Timer(60, exception_remind, [message])
    checker_v2 = threading.Timer(60, exception_remind, [message])
    checker_v3 = threading.Timer(60, exception_remind, [message])
    checker_v4 = threading.Timer(60, exception_remind, [message])


########################################################################

    
    bot.send_message(message.chat.id,"🔥Вітаю у TaskBot" + "\n" + "Для продовження роботи натисни кнопку Авторизуватися",reply_markup=markup)


@bot.message_handler(content_types = ["text"])

#The controlling of all buttons in the menu

def autorization(message,*args, **kwargs):
    

    #The reaction on the pressing of the button "Sign up"

    if message.text == ("📝Зареєструватися"):
        print(args)
        Check["{0.id}".format(message.from_user)] = 0
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

    elif message.text == ("🔓Авторизуватися"):
        Check["{0.id}".format(message.from_user)] = 0
        
        find = collection.find({"_id":"{0.id}".format(message.from_user)})
        a = [i for i in find]
        if len(a) == 0:
            bot.send_message(message.chat.id,"❌Ви не зареєстровані")
        else:           
            bot.send_message(message.chat.id,"⚠️Зачекайте....")
            time.sleep(1.5)
            for check in collection.find({"_id":"{0.id}".format(message.from_user)}):
                try:
                    if check["connected"] == True:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        part1 = types.KeyboardButton("🗒Зробити запис")
                        part2 = types.KeyboardButton("🔎Продивитися усі записи")
                        part3 = types.KeyboardButton("🔔Нагадування")
                        part4 = types.KeyboardButton("❌Видалити аккаунт")
                        part5 = types.KeyboardButton("Аккаунт TaskBot")
                        markup.add(part1,part2,part3,part4,part5)
                        bot.send_message(message.chat.id,"✅Вітаю,ви увійшли в систему",reply_markup=markup)
                except KeyError:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    part1 = types.KeyboardButton("🗒Зробити запис")
                    part2 = types.KeyboardButton("🔎Продивитися усі записи")
                    part3 = types.KeyboardButton("🔔Нагадування")
                    part4 = types.KeyboardButton("❌Видалити аккаунт")
                    part5 = types.KeyboardButton("Прив'язати аккаунт")
                    markup.add(part1,part2,part3,part4,part5)
                    bot.send_message(message.chat.id,"✅Вітаю,ви увійшли в систему",reply_markup=markup)

    elif message.text == "Прив'язати аккаунт":
        msg = bot.send_message(message.chat.id,"Введіть email")
        bot.register_next_step_handler(msg,connect_email)



    #The reaction on the pressing on the button "Delete the accaunt"

    elif message.text == ("❌Видалити аккаунт"):
        Check["{0.id}".format(message.from_user)] = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stuff1 = types.KeyboardButton("🔓Авторизуватися")
        stuff2 = types.KeyboardButton("📝Зареєструватися")
        markup.add(stuff1,stuff2)
        bot.send_message(message.chat.id,"✅" + "{0.first_name}".format(message.from_user) + " " + "ви видалили аккаунт",reply_markup=markup)
        collection.find_one_and_delete({"_id":"{0.id}".format(message.from_user)})


    #The reaction on the pressing of the button "Reminders"
    
    elif message.text == ("🔔Нагадування"):
        msg = bot.send_message(message.chat.id,"✏️Напишіть,що Вам нагадати")
        Check["{0.id}".format(message.from_user)] = 0
        global check_time_reminder
        check_time_reminder = threading.Timer(60, check_func_reminder, [message])
        check_time_reminder.start()

        #Comming to the next function "reminders"

        bot.register_next_step_handler(msg, reminders)
        
        
    elif message.text == ("Аккаунт TaskBot"):
        for email_and_password in collection.find({"_id":"{0.id}".format(message.from_user)}):
            try:
                if email_and_password["connected"] == True:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    stuff = types.InlineKeyboardButton("Cумарна заборгованість",callback_data="Sum")
                    stuff1 = types.InlineKeyboardButton("Усі записані заборгованості",callback_data="Loan")
                    stuff2 = types.InlineKeyboardButton("Відв'язати аккаунт",callback_data="unconnect")
                    markup.add(stuff,stuff1,stuff2)
                    bot.send_message(message.chat.id,"Ось усі варіанти опцій",reply_markup=markup)
            except KeyError:
                bot.send_message(message.chat.id,"Сталася помилка😿")
        

    #The reaction on the pressing of the button "Look at all notes"

    elif message.text == ("🔎Продивитися усі записи"):
        Check["{0.id}".format(message.from_user)] = 0
        try:
            note = collection.find({"_id":"{0.id}".format(message.from_user)})
            len_list = [note]
            if len(len_list) == 0:
                bot.send_message(message.chat.id,"⛔️Ви не маєте записів")
            else:
                len_list.clear()
                for i in note:
                    k = i["notes"] 
                    if len(k) == 0:
                        bot.send_message(message.chat.id,"⛔️Ви не маєте записів")    
                    else:      
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

    elif message.text == ("🗒Зробити запис"):
        msg = bot.send_message(message.chat.id,"🖍Можете робити запис" + "\n" + "❗️❗️❗️Небхідно виконувати запис у такому форматі" + "\n" + "--------------------------" + "\n" + "1)..........." + "\n" + "2)..........." + "\n" + "3)..........." + "\n" + "--------------------------")
        global check_time
        check_time = threading.Timer(60, check_func_notes, [message])
        ra = re.findall(r'started',str(check_time))
        print(ra)
        check_time.start()
        print(check_time)
        r = re.findall(r'started',str(check_time))
        print(r)
        
        

        
        #Comming to the next function "notes"

        bot.register_next_step_handler(msg, notes)
    else:
        bot.send_message(message.chat.id,"Виберіть пункт із меню😉")

def notes(message):
    
    check_time.cancel()
   

    Notes.append({"{0.id}".format(message.from_user):message.text + "\n" + "Час запису" + " " +  str(datetime.date.today())})         
    collection.replace_one({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
    msg = bot.send_message(message.chat.id,"✅Ви зробили запис")
    bot.register_next_step_handler(msg, autorization)  



def connect_email(message):
    user_email = message.text
    if site.find_one({"_id":user_email}) != None:
        msg = bot.send_message(message.chat.id,"Введіть пароль")
        bot.register_next_step_handler(msg, connect_password, user_email) 
    else:
        bot.send_message(message.chat.id,"Аккаунту з таким email не існує")

def connect_password(message,email):
    if site.find_one({"_id":email,"password":message.text}) != None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        part5 = types.KeyboardButton("Аккаунт TaskBot")
        markup.add(part1,part2,part3,part4,part5)
        bot.send_message(message.chat.id,"Вітаю,ви прив'язали бота до аккаунту сайту TaskBot",reply_markup=markup)
        collection.update({"_id":"{0.id}".format(message.from_user)},{"$set":{"connected":True,"email":email,"password":message.text}})
        site.update({"_id":email},{"$set":{"connected":True,"connected_name":"{0.first_name}".format(message.from_user),"connected_last_name":"{0.last_name}".format(message.from_user)}})
    else:
        bot.send_message(message.chat.id,"Пароль неправильний")
    

def reminders(message):

    #The reminder adding to the database
     
    try: 
        info = collection.find({"_id":"{0.id}".format(message.from_user)})
        for i in info:
            k = i["reminders"]          
            if len(k) >= 1:
                markup = types.InlineKeyboardMarkup()
                stuff = types.InlineKeyboardButton(text="Видалити нагадування",callback_data="delete")
                markup.add(stuff)
                bot.send_message(message.chat.id,"⛔️Ви вже маєте активне нагадування",reply_markup=markup)
                check_time_reminder.cancel()
            else:
                check_time_reminder.cancel()
                collection.update({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes,"reminders":message.text})
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                special = types.KeyboardButton("💭Вибрати свій час")
                stuff1 = types.KeyboardButton("🕐15 хвилин")
                stuff2 = types.KeyboardButton("🕖30 хвилин")
                stuff3 = types.KeyboardButton("🕕1 година")
                stuff4 = types.KeyboardButton("🕔2 години")
                stuff5 = types.KeyboardButton("🕓4 години")
                stuff6 = types.KeyboardButton("🕒6 годин")
                stuff7 = types.KeyboardButton("🕑12 годин")
                stuff8 = types.KeyboardButton("🕗24 години")
                markup.add(special,stuff1,stuff2,stuff3,stuff4,stuff5,stuff6,stuff7,stuff8)
                mess = bot.send_message(message.chat.id,"⏰Коли Вам це нагадати",reply_markup=markup) 
                bot.register_next_step_handler(mess, name_reminder)
    except KeyError:
        check_time_reminder.cancel() 
        collection.replace_one({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes,"reminders":message.text})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        special = types.KeyboardButton("💭Вибрати свій час")
        stuff1 = types.KeyboardButton("🕐15 хвилин")
        stuff2 = types.KeyboardButton("🕖30 хвилин")
        stuff3 = types.KeyboardButton("🕕1 година")
        stuff4 = types.KeyboardButton("🕔2 години")
        stuff5 = types.KeyboardButton("🕓4 години")
        stuff6 = types.KeyboardButton("🕒6 годин")
        stuff7 = types.KeyboardButton("🕑12 годин")
        stuff8 = types.KeyboardButton("🕗24 години")
        markup.add(special,stuff1,stuff2,stuff3,stuff4,stuff5,stuff6,stuff7,stuff8)
        mess = bot.send_message(message.chat.id,"⏰Коли Вам це нагадати",reply_markup=markup)           
        bot.register_next_step_handler(mess, name_reminder)

    

def name_reminder(message):

    #the reaction on the pressing of the button "15 minutes"

    if message.text == ("💭Вибрати свій час"):
        msg = bot.send_message(message.chat.id,"📝Напишіть час коли Вам нагадати ваш запис у такому форматі❗️" + "\n" + "\n" + "<b>Рік.Місяць.День Година:Хвилини:Секунди</b>",parse_mode="html")
        global check_time_reminder_own
        check_time_reminder_own = threading.Timer(60, check_func_reminder_own, [message])
        check_time_reminder_own.start()
        bot.register_next_step_handler(msg, time_reminders_own)




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


###########################################################################################################################################
#Functions for the checking of the activity


def check_func_reminder(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    part1 = types.KeyboardButton("🗒Зробити запис")
    part2 = types.KeyboardButton("🔎Продивитися усі записи")
    part3 = types.KeyboardButton("🔔Нагадування")
    part4 = types.KeyboardButton("❌Видалити аккаунт")
    markup.add(part1,part2,part3,part4)
    msg = bot.send_message(message.chat.id,"😭Ви не встигли зробити нагадування,якщо хочете повторити спробу,натисніть кнопку" + "\n" + "         " + "<b>Нагадування</b>",parse_mode="html",reply_markup=markup)
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.register_next_step_handler(msg, autorization)   






def exception_remind(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    part1 = types.KeyboardButton("🗒Зробити запис")
    part2 = types.KeyboardButton("🔎Продивитися усі записи")
    part3 = types.KeyboardButton("🔔Нагадування")
    part4 = types.KeyboardButton("❌Видалити аккаунт")
    markup.add(part1,part2,part3,part4)
    msg = bot.send_message(message.chat.id,"😭Ви не встигли зробити нагадування,якщо хочете повторити спробу,натисніть кнопку" + "\n" + "         " + "<b>Нагадування</b>",parse_mode="html",reply_markup=markup)   
    collection.replace_one({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.register_next_step_handler(msg, autorization)   
    






def check_func_reminder_own(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    part1 = types.KeyboardButton("🗒Зробити запис")
    part2 = types.KeyboardButton("🔎Продивитися усі записи")
    part3 = types.KeyboardButton("🔔Нагадування")
    part4 = types.KeyboardButton("❌Видалити аккаунт")
    markup.add(part1,part2,part3,part4)
    msg = bot.send_message(message.chat.id,"😭Ви не встигли зробити нагадування,якщо хочете повторити спробу,натисніть кнопку" + "\n" + "         " + "<b>Нагадування</b>",parse_mode="html",reply_markup=markup)
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.register_next_step_handler(msg, autorization)   
    




def check_func_notes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    part1 = types.KeyboardButton("🗒Зробити запис")
    part2 = types.KeyboardButton("🔎Продивитися усі записи")
    part3 = types.KeyboardButton("🔔Нагадування")
    part4 = types.KeyboardButton("❌Видалити аккаунт")
    markup.add(part1,part2,part3,part4)
    msg = bot.send_message(message.chat.id,"😭Ви не встигли зробити запис,якщо хочете повторити спробу,натисніть кнопку 'Зробити запис' ",reply_markup=markup)
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    bot.register_next_step_handler(msg,autorization)




#######################################################################################################################################

#Function for the chacking of the rightness input of your own reminder time


def time_reminders_own(message):
    
    
    try:
        finder = r'[0-9]{4}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
        result = re.findall(finder, message.text)
        global comparedtime_copy
        global comparedtime
        for i in result:
            
            comparedtime = i.replace(".", "").replace(":","").replace(" ", "")
            comparedtime_copy = i.replace(".", ":")
        
        
        date = datetime.datetime.now()
        comparedtime_global = date.strftime("%Y,%m,%d %H,%M,%S")
        changed_time = comparedtime_global.replace(",","").replace(" ","")
        solution = int(comparedtime) - int(changed_time)
        

        #The cancelling of all timers for the checking of the activity

        checker.cancel()
        checker_v2.cancel()
        checker_v3.cancel()
        checker_v4.cancel()
        check_time_reminder_own.cancel()

        #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#


        if solution >= 0:
            if len(result) > 0:
                
                #The cancelling of all timers for the checking of the activity

                checker.cancel()
                checker_v2.cancel()
                checker_v3.cancel()
                checker_v4.cancel()
                check_time_reminder_own.cancel()

                #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#


                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                part1 = types.KeyboardButton("🗒Зробити запис")
                part2 = types.KeyboardButton("🔎Продивитися усі записи")
                part3 = types.KeyboardButton("🔔Нагадування")
                part4 = types.KeyboardButton("❌Видалити аккаунт")
                markup.add(part1,part2,part3,part4)
                bot.send_message(message.chat.id,"✅Нагадування зроблене!",reply_markup=markup)
                

                Check_time["{0.id}".format(message.from_user)] = comparedtime_copy
                result.clear()
                timercheck = threading.Thread(target=checking_time(message))
                timercheck.start()
                timercheck.join()
                    
            else:

                #The cancelling of all timers for the checking of the activity

                checker.cancel()
                checker_v2.cancel()
                checker_v3.cancel()
                checker_v4.cancel()
                check_time_reminder_own.cancel()

                #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#

                
                msg = bot.send_message(message.chat.id,"😭Ви не правильно ввели час або дату")
                checker.start()
                bot.register_next_step_handler(msg, time_reminders_own)

        else:

            #The cancelling of all timers for the checking of the activity

            checker.cancel()
            checker_v2.cancel()
            checker_v3.cancel()
            checker_v4.cancel()
            check_time_reminder_own.cancel()

            #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#


            msg = bot.send_message(message.chat.id,"😜Я не можу відправити Вам нагадування у минуле\nВведіть коректну дату та час")
            checker_v2.start()
            bot.register_next_step_handler(msg, time_reminders_own)
        

    except ValueError:

        #The cancelling of all timers for the checking of the activity

        checker.cancel()
        checker_v2.cancel()
        checker_v3.cancel()
        checker_v4.cancel()
        check_time_reminder_own.cancel()

        #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#

        
        msg = bot.send_message(message.chat.id,"😭Ви не правильно ввели час або дату")
        checker_v3.start()
        bot.register_next_step_handler(msg, time_reminders_own)

    except NameError:

        #The cancelling of all timers for the checking of the activity

        checker.cancel()
        checker_v2.cancel()
        checker_v3.cancel()
        checker_v4.cancel()
        check_time_reminder_own.cancel()

        #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#

        msg = bot.send_message(message.chat.id,"😭Ви не правильно ввели час або дату")
        checker_v4.start()
        bot.register_next_step_handler(msg, time_reminders_own)

    except RuntimeError:
        
        #The cancelling of all timers for the checking of the activity

        checker.cancel()
        checker_v2.cancel()
        checker_v3.cancel()
        checker_v4.cancel()
        check_time_reminder_own.cancel()

        #~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#

        
        msg = bot.send_message(message.chat.id,"😭Ви не правильно ввели час або дату")
        checker_v3.start()
        bot.register_next_step_handler(msg, time_reminders_own)
            
            
                        
#Function for the sending message in your own time
         

def checking_time(message):
    date = datetime.datetime.now()
    global_time = date.strftime("%Y:%m:%d %H:%M:%S")
    
    try:
        if Check_time["{0.id}".format(message.from_user)] == global_time:
            mess = collection.find({"_id":"{0.id}".format(message.from_user)})
            for i in mess:
                bot.send_message(message.chat.id,"❗️❗️❗️" + "Нагадування" + "\n" + "\n" + "\n" +  i["reminders"])
                collection.replace_one({"_id":"{0.id}".format(message.from_user)}, {"_id":"{0.id}".format(message.from_user),"notes":Notes})
        else:
            remtimer = threading.Timer(1, checking_time, [message])
            remtimer.start()
    except KeyError:
        print("An error happened")



################################################################################################################################################

#Function for the deleting of your own reminder if you wanna change it 



@bot.callback_query_handler(lambda delete: delete.data=="delete")
def dele(delete):
    if delete.data == "delete":
        info = collection.find({"_id":"{0.id}".format(delete.from_user)})
        for i in info:
            try:
                if len(i["reminders"]) > 0:
                    collection.replace_one({"_id":"{0.id}".format(delete.from_user)}, {"_id":"{0.id}".format(delete.from_user),"notes":Notes})
                    bot.send_message(delete.message.chat.id,"✅Нагадування видалено")
                else:
                    bot.send_message(delete.message.chat.id,"❗️Немає нагадувань")
            except KeyError:
                bot.send_message(delete.message.chat.id,"❗️Немає нагадувань")


                
@bot.callback_query_handler(lambda summ: summ.data=="Sum")
def taskbot_acc(summ):
    if summ.data == "Sum":
        for email in collection.find({"_id":"{0.id}".format(summ.from_user)}):
            user_email = email["email"]
            #user_password = email["password"]
            for data in site.find({"_id":user_email}):
                try:
                    bot.send_message(summ.message.chat.id,"Сумма вашої заборгованості" + " " + "-" + " " + str(data["loan"]))      
                except KeyError:
                    bot.send_message(summ.message.chat.id,"❗️Немає інформації про Ваш сумарний борг")
                    

@bot.callback_query_handler(lambda loan: loan.data == "Loan")
def taskbot_loan(loan):
    if loan.data == "Loan":
        bot.send_message(loan.message.chat.id,"Перша колонка - 'За що'" + "\n" + "Друга колонка - 'Опис'" + "\n" + "Третя колонка - 'Cума заборгованості'")
        for email_user in collection.find({"_id":"{0.id}".format(loan.from_user)}):
            user = email_user["email"]
            for info in site.find({"_id":user}):
                try:
                    for i in info["full_loan"]:
                        splited = (*i,)
                        bot.send_message(loan.message.chat.id,str(splited[0]) + " " + "|" + " " + str(splited[1]) + " " + "|" + " " + str(splited[2]))
                except KeyError:
                    bot.send_message(loan.message.chat.id,"❗️Немає інформації про ваші заборгованості")
                    
@bot.callback_query_handler(lambda unconnect: unconnect.data == "unconnect")
def taskbot_unconnect(unconnect):
    if unconnect.data == "unconnect":
        collection.update({"_id":"{0.id}".format(unconnect.from_user)},{"$unset":{"connected":"","email":"","password":""}})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        part1 = types.KeyboardButton("🗒Зробити запис")
        part2 = types.KeyboardButton("🔎Продивитися усі записи")
        part3 = types.KeyboardButton("🔔Нагадування")
        part4 = types.KeyboardButton("❌Видалити аккаунт")
        part5 = types.KeyboardButton("Прив'язати аккаунт")
        markup.add(part1,part2,part3,part4,part5)
        bot.send_message(unconnect.message.chat.id,"Вітаю,ви відв'язали аккаунт",reply_markup=markup)



###################################################################################################################################################
            
bot.polling(none_stop=True,timeout=5,interval=1)