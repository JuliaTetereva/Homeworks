import telebot
import requests
import string
import nltk 
from nltk.probability import FreqDist
from telebot import types

#nltk.download('averaged_perceptron_tagger_ru')
#nltk.download('punkt')

bot = telebot.TeleBot('токен');
@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    splitted_text = message.text.split()
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь? То, что я умею, можешь узнать в /help.")
    elif message.text == "Я тебя люблю":
        bot.send_message(message.from_user.id, "Я тебя тоже")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, '''Если вы хотите проверить доступность сайта - напишите /site ссылка_на сайт;
Если вы хотите проанализировать текст - напишите /text текст_для_анализа;
Если вы хотите открыть калькулятор - напишите /calc''')

#Задание 1. Проверка доступности сайта
    elif  splitted_text[0] == "/site":
        if len(splitted_text) != 2:
            bot.send_message(message.from_user.id,'Нет такого сайта!')
            return 0 
        try:
            response = requests.get(splitted_text[1])
            bot.send_message(message.from_user.id,'Сайт доступен!')
        except:
            bot.send_message(message.from_user.id,'Сайт не доступен:(')


# Задание 2. Статистика текста
    elif  splitted_text[0] == "/text":
        your_text = message.text.split()
        del your_text[0]

# Убираем пунктуацию кроме конца предложений
        new_str = string.punctuation.replace('!', '') 
        new_str = new_str.replace('.', '')
        new_str = new_str.replace('?', '')
        new_str = new_str + '—'+'«'+'»'
        end_sent = ('.','!','?','/n')
        your_text = " ".join(your_text)

        new_text = "".join([ch for ch in your_text if ch not in new_str])
        count=0
        for i in new_text:
            if i in end_sent:
                count+=1
            else:
                continue
        bot.send_message(message.from_user.id,'Количество предложений: '+str(count))

# Удаляем оставшиеся знаки препинания, считаем количество слов
        new_text = "".join([ch for ch in new_text if ch not in string.punctuation])
        new_text = new_text.lower()
        dict_t = {}
        for key in new_text.split():
            dict_t[key] = dict_t.setdefault(key, 0) +1
        bot.send_message(message.from_user.id,'Количество уникальных слов: '+str(dict_t))
        summa=0
        for key,value in dict_t.items():
            summa+=1
        bot.send_message(message.from_user.id,'Всего уникальных слов: '+str(summa))
# Удаляем предлоги, частицы, союзы
        words = nltk.word_tokenize(new_text)
        functors_pos = {'CONJ', 'PR', 'PART'}
        without_functors_string = [word for word, pos in nltk.pos_tag(words, lang='rus') if pos not in functors_pos]
# Самые популярные слова
        fdist = FreqDist(without_functors_string)
        bot.send_message(message.from_user.id,'Самые популярные слова: '+ str(fdist.most_common(3)))

# Калькулятор
# Создаем кнопки и просим ввести числа, передаем в функцию входа
    elif  splitted_text[0] == "/calc":
        markup = types.ReplyKeyboardRemove(selective=True)
        msg = bot.send_message(message.chat.id, "Введите два числа через пробел, для выхода введите отмена ", reply_markup=markup)
        global calc
        calc = types.ReplyKeyboardMarkup(row_width=1)
        item_btn1 = types.KeyboardButton('+')
        item_btn2 = types.KeyboardButton('-')
        item_btn3 = types.KeyboardButton('*')
        item_btn4 = types.KeyboardButton('/')
        calc.add(item_btn1, item_btn2, item_btn3, item_btn4)
        bot.register_next_step_handler(msg, calculator_enter)

# Else case
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        print('Пользователь не понимает, что нужно написать Привет')
        print(message)


# Функция входа в калькулятор. Проверка на выход из калькулятора, выбор действия, передача в функию расчета
def calculator_enter(message):
    global user_num
    user_num = message.text.lower()
    if user_num == 'отмена':
        bot.send_message(message.from_user.id, 'Калькулятор закрыт')
        return
    else:
        msg = bot.send_message(message.chat.id, " Выберите действие:", reply_markup=calc)
        bot.register_next_step_handler(msg, calculator_operate)

# Функция расчета, реализована проверка на правильно введенные данные 
def calculator_operate(message):  
    user_numbers = message.text
    count_list = user_num.split()
    if user_numbers == '+':
        try:   
            result = float(count_list[0]) + float(count_list[1])
            bot.send_message(message.from_user.id, 'Результат: ' + str(result))
        except:
            bot.send_message(message.from_user.id, 'Пишите правильно!')
    elif user_numbers == '-':
        try:   
            result = float(count_list[0]) - float(count_list[1])
            bot.send_message(message.from_user.id, 'Результат: ' + str(result))
        except:
            bot.send_message(message.from_user.id, 'Пишите правильно!')
    elif user_numbers == '*':
        try:   
            result = float(count_list[0]) * float(count_list[1])
            bot.send_message(message.from_user.id, 'Результат: ' + str(result))
        except:
            bot.send_message(message.from_user.id, 'Пишите правильно!')
    elif user_numbers == '/':
        if int(count_list[1]) != 0:  
            try:   
                result = float(count_list[0]) / float(count_list[1])
                bot.send_message(message.from_user.id, 'Результат: ' + str(result))
            except:
                bot.send_message(message.from_user.id, 'Пишите правильно!')
        else:
            bot.send_message(message.from_user.id, 'Делить на ноль я не умею')
    calc = types.ReplyKeyboardRemove(selective=True)
    msg = bot.send_message(message.chat.id, 'Введите два числа через пробел: ', reply_markup=calc)
    bot.register_next_step_handler(msg, calculator_enter)   

bot.polling(none_stop=True, interval=0)


