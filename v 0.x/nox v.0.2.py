'''
План:

1) Создать оболочку способную выполнять простейшие голосовые команды
--- Создать перехват ошибок, если после "Слова-Активатора команда не распознана, сообщает ою этом

2) Создать на основе скрипта программу способную запускаться с запуском компьютера

3) Создать функционал добавления команд пользователем




Дополнительно:
--- Создать код Универсального Переводчика, конектящегося к гугл переводчику, заливающегшо туда сказаное пользователем( переменная),
--- и забирающего отуда результат произнося его
------ Создать перехват ошибкок, к примеру если ошибка в виде невозмождности подключится к сети или сайту сообщать об этом

'''


# v. 0.1 " Поехали!"




################################################################################################################################################################################
#                                                           Упрощенная версия распознавания команд (не отвечает)
################################################################################################################################################################################
'''

# снача создаем выполнение команд, через распознавание голоса, потом добавляем голос самому помошнику

import speech_recognition as sr
import os
import datetime

# Создание среды распознавания
record = sr.Recognizer()
# Задание микрофона
microphone = sr.Microphone(device_index = 1)


def runProgramm(text):
    if str(text) == 'время':
        print(datetime.datetime.now().hour, ' : ' , datetime.datetime.now().minute)
    # Воспроизвести Радио
    elif str(text) == 'радио':
        os.system('E:/Python/Projects/NOX/09f85c8c0e74.mp3')
    #elif str(text) == 'google':
        #os.system('C:/users/Projects/NOX/09f85c8c0e74.mp3')
    else:
        print('Команда не распознана, пожалуйста повторите')

try:
    while True:
        with microphone as source:
            record.adjust_for_ambient_noise(source)
            audio = record.listen(source)
            result =record.recognize_google(audio, language='ru-RU').lower()
            result = result.lower()
            print(f'{result}')
            runProgramm(result)
except Exception as e:
    print(e)
    print('Сервер Гугл не отвечает')


'''




#################################################  Кривая GOOGLE API гробит весь скрипт, от чего он работает через раз   #############################################################

'''

# Обязательные модули для установки
# pywin32, pypiwin32, SpeechRecognition, fuzzywuzzy, ОСОБЕННО pyttsx3( руский текс не распознает) PyAudio( не работает на Python 3.7)
import speech_recognition as sr     # Library SpeechRecognition - Распознаватель голоса и Микрофона(в том числе GOOGLE) \ Альтернатив много к примеру pocketsphinx , но гребт адски
from fuzzywuzzy import fuzz
#import fuzzywuzzy as fuzz          # Library fuzzywuzzy        - Для НЕЧЕТКОГО СРАВНЕНИЯ Словарей
import pyttsx3                      # Library pyttsx3           - ПРЕОБРАЗОВАТЕЛЬ ТЕКСТА В РЕЧЬ! - Голос помошника
import time
import os
import datetime




#------------------------------------------------------------------------------------- ПРОВЕРКИ РАБОТЫ БИБЛИОТЕК -------------------------------------------------------------
# После загрузки модулей надо проверить правильно ли они встали ( особенно pyttsx3  pywin32 и pypiwin32) Так как может НЕ ОПРЕДЕЛЯТЬ РУССКИЙ ЯЗЫК. и тогда наждо задать в ручную
# Проверка РАСПОЗНАВАНИЯ ТЕКСТА ИПЕРЕВЕДЕНИЯ ЕГО В ГОЛОС

engine = pyttsx3.init()
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
engine.setProperty('voice', ru_voice_id)
engine.say(' One Один Two. Програма помошник НОКС готова к работе!')
engine.runAndWait()
'''

# Проверка ИНДЕКСА МИКРОФОНА в системе ( у меня Микрофон (Realtek High Definition Audio) бывает 2 индекса ( у меня вышло 1 и 7))
'''
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index,name))
'''

# Проверка РАСПОЗНАВАНИЯ ГОЛОСА
'''
r= sr.Recognizer()                                          # Создание СРЕДЫ распознования речи
with sr.Microphone(device_index=1) as source:               # Включение микровона для записи сообщения на распознование
    r.adjust_for_ambient_noise(source, duration=0.5)        # В течении указаного времени(0.5 сек) слушает фоновый шум что бы потом не путать его с речью человека
                                                            # ! ВАЖНО ! : Установи задержку между включением и распонования, без её команда может уйти в ВЕЧНЫЙ ЦИКЛ!
    print("Скажи что-нибудь")                               # Оповещение что можно говорить
    audio = r.listen(source)                                # Запись сообщения для распознавания

# Перехват ошибки ессли речь не удалось распознать
try:
    query = r.recognize_google(audio, language="ru-RU")     # API GOOGLE тоесть нужно иметь связь с инетом+ занимает время
    print(' Я сказал:' + query)
except Exception as e:
    print(e)
    print('Нихера не разобрать')

#query = r.recognize_google(audio, language="us-US", show_all=True)
#print(' Я сказал:' + query)
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


'''

# Опции НЕЧЕТКОГО РАСПОЗНАВАНИЯ КОМАНД + fuzzywuzzy - Словарь команд (задается словать с возможными вараинтами запросов)
# alias(псевдоним)      - Запуск СЛУХА. обращение активирующее программу прослушивания команд
# tbr (to_be_removed)   - Слова паразиты которые надо удалить из команд пользователя, что бы не захломлять команды для кода
# cmds                  - Словарь самих Команд, и слова которые их активизируют.


opts = {
    "alias" :('nox', 'нокс', 'бокс','max','макс','мопс','люкс','linux','Люнукс','курс'),
    "tbr"   :('скажи','произнеси','озвучь','сколько','расскажи'),

    "cmds"  :{
        "ctime" :('время','текущее время','которы час','сейчас времени'),
        "radio" :('включи радио','запусти радио','включи музыку','воспроизвести музыку'),
        "stipid":('расскажи анегдот','ты знаешь анегдот','рассмеши','анекдот расскажи'),
        }

    }


# РАСПОЗНАВАНИЕ ГОЛОСОВОЙ КОМАНДЫ  через GOOGLE распознаватель голоса
def callback(recognizer, audio):

    try:


        voice = recognizer.recognize_google(audio, language="ru-Ru").lower()
        print('[log] Распознано ' + voice)

        # Если фраза начинается с имени нашегно помошника то
        # 1) АКТИВИРУЕМ ПОМОШНИКА
        # 2) Вырезаем из фразы все возможные имена помошника и все фразы из ячейки tbr, что бы оставить лишь ЧИСТУЮ команду
        # АЛЬТЕРНАТИВА (2) просто задать что если в фраще есть КЛЮЧЕВОЕ СЛОВО команды то активировать команду( так проще если команды короткие, но хуже если длиные)
        if voice.startswith(opts["alias"]):

            # Обращение к помошнику полной фразой
            cmd = voice
            # Очистка команды для Обращение к NOX(cmd) ЧИСТОЙ КОМАНДОЙ без лишнего шума( имен , слов паразитов и т.д.)
            for x in opts['alias']:
                cmd.replace(x,'').strip()
            for x in opts['tbr']:
                cmd.replace(x,'').strip()

            # Распознавание оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
            cmd = recognizer_cmd(cmd)
            # ИСПОЛНЕНИЕ оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
            execute_cmd(cmd['cmd'])


    #except recognizer.UnknownValueError:
    except Exception as e:
        print(e)
        print('[log] Команда не распознана')

# Распознавание НЕЧЕТКОЕ команды при помощи fuzzywuzzy
def recognizer_cmd(cmd):
    # НЕЧЕТКОЕ сравнение полученой команды из ячейки настроек cmds
    RC = {'cmd':'','percent':0}

    # Получаем Ключи и Значения ячейкир настроек cmds, (нас интересуют только значения, ключ будет нуден когда мы узнаем ЗНАЧЕНИЕ)
    for c,v in opts['cmds'].items():

        # Проверяем НЕЧЕТКОЕ совпадения команды и Значения
        for x in v:
            vrt = fuzz.ratio(cmd,x)

            # И оставляем самую похожую на то что произнес пользователь команду
            if vrt > RC['percent']:
                # Выбираем КЛЮЧ-команду которму соответсвует комманда-значение
                RC['cmd'] = c

                RC['percent'] = vrt     # [log] Распознано мопс время {'cmd': 'ctime', 'percent': 67}
                #print(RC)
    return RC

# Исполнение команды
def execute_cmd(cmd):


    # Сказать текущее время (узнать время кодом, передать на озвучку помошнику полученую строку)
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Сейчас ' + str(now.hour)+' : ' + str(now.minute))


    # Воспроизвести Радио
    elif cmd == 'radio':
        os.system('E:/Python/Projects/NOX/09f85c8c0e74.mp3')


    # Расказать анегдот
    elif cmd == 'stupid':
        speak('Ни один анегдот пока не загружен')


    else:
        print('Команда не распознана, пожалуйста повторите')
        speak('Команда не распознана, пожалуйста повторите')




# Говорить (функция произнесения помошником полученых из кода текстовых (str) данных)
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()








# Начало
# Запуск Распознавания голоса
r = sr.Recognizer()
# Выбор устройства для передачи голоса (микрофон)
m = sr.Microphone(device_index = 1)


#Обработка команды
# Используем  выбраный микрофон для распознавания голоса
with m as source:
    # adjust_for_ambient_noise  в течении указаного времени(0.5 сек) слушает фоновый шум что бы потом не путать его с речью человека
    r.adjust_for_ambient_noise(source)
    #r.adjust_for_ambient_noise(source, duration=0.5)



#-------------------------------------------------------------------------------------------------------
# Голос Помошника
speak_engine = pyttsx3.init()

# Дефалтный помошник, ВАЖНО перевести на РУССКИЙ язык текста иначе будет распознавать только английский!( в реестре можно глянуть остальыне языки)
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
speak_engine.setProperty('voice', ru_voice_id)


# ТОЛЬКО если установлены ОТЛИЧНЫЕ ОТ ДЕФОЛТНЫХ голоса речи для помошника
#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voices', voices[4].id)
#------------------------------------------------------------------------------------------------------


speak('Добрый День Нокс активен')



stop_listening = r.listen_in_background(m, callback)



while True:
        input('Сказано:')
        print('1')
        time.sleep(0.1) #Бесконечный цикл до исполнения start()
'''







###########################################  УЛУЧШЕНАЯ ВЕРСИЯ помошника, распознает лучше и не прекращает рабоыт после  выполнения команды  #########################################



# Обязательные модули для установки
# pywin32, pypiwin32, SpeechRecognition, fuzzywuzzy, ОСОБЕННО pyttsx3( руский текс не распознает) PyAudio( не работает на Python 3.7)
import speech_recognition as sr     # Library SpeechRecognition - Распознаватель голоса и Микрофона(в том числе GOOGLE) \ Альтернатив много к примеру pocketsphinx , но гребт адски
from fuzzywuzzy import fuzz
#import fuzzywuzzy as fuzz          # Library fuzzywuzzy        - Для НЕЧЕТКОГО СРАВНЕНИЯ Словарей
import pyttsx3                      # Library pyttsx3           - ПРЕОБРАЗОВАТЕЛЬ ТЕКСТА В РЕЧЬ! - Голос помошника
import time
import os
import sys
import subprocess
import datetime



'''
#------------------------------------------------------------------------------------- ПРОВЕРКИ РАБОТЫ БИБЛИОТЕК -------------------------------------------------------------
# После загрузки модулей надо проверить правильно ли они встали ( особенно pyttsx3  pywin32 и pypiwin32) Так как может НЕ ОПРЕДЕЛЯТЬ РУССКИЙ ЯЗЫК. и тогда наждо задать в ручную
# Проверка РАСПОЗНАВАНИЯ ТЕКСТА ИПЕРЕВЕДЕНИЯ ЕГО В ГОЛОС

engine = pyttsx3.init()
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
engine.setProperty('voice', ru_voice_id)
engine.say(' One Один Two. Програма помошник НОКС готова к работе!')
engine.runAndWait()
'''

# Проверка ИНДЕКСА МИКРОФОНА в системе ( у меня Микрофон (Realtek High Definition Audio) бывает 2 индекса ( у меня вышло 1 и 7))
'''
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index,name))
'''

# Проверка РАСПОЗНАВАНИЯ ГОЛОСА
'''
r= sr.Recognizer()                                          # Создание СРЕДЫ распознования речи
with sr.Microphone(device_index=1) as source:               # Включение микровона для записи сообщения на распознование
    r.adjust_for_ambient_noise(source, duration=0.5)        # В течении указаного времени(0.5 сек) слушает фоновый шум что бы потом не путать его с речью человека
                                                            # ! ВАЖНО ! : Установи задержку между включением и распонования, без её команда может уйти в ВЕЧНЫЙ ЦИКЛ!
    print("Скажи что-нибудь")                               # Оповещение что можно говорить
    audio = r.listen(source)                                # Запись сообщения для распознавания

# Перехват ошибки ессли речь не удалось распознать
try:
    query = r.recognize_google(audio, language="ru-RU")     # API GOOGLE тоесть нужно иметь связь с инетом+ занимает время
    print(' Я сказал:' + query)
except Exception as e:
    print(e)
    print('Нихера не разобрать')

#query = r.recognize_google(audio, language="us-US", show_all=True)
#print(' Я сказал:' + query)
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# Опции НЕЧЕТКОГО РАСПОЗНАВАНИЯ КОМАНД + fuzzywuzzy - Словарь команд (задается словать с возможными вараинтами запросов)
# alias(псевдоним)      - Запуск СЛУХА. обращение активирующее программу прослушивания команд
# tbr (to_be_removed)   - Слова паразиты которые надо удалить из команд пользователя, что бы не захломлять команды для кода
# cmds                  - Словарь самих Команд, и слова которые их активизируют.


opts = {
    "alias" :('nox', 'нокс', 'бокс','max','макс','мопс','люкс','linux','Люнукс','курс','нукс'),
    "tbr"   :('скажи','произнеси','озвучь','сколько','расскажи'),

    "cmds"  :{
        "ctime" :('время','текущее время','которы час','сейчас времени'),
        "radio" :('включи радио','запусти радио','включи музыку','воспроизвести музыку'),
        "stipid":('расскажи анегдот','ты знаешь анегдот','рассмеши','анекдот расскажи'),
        }

    }






# Распознавание НЕЧЕТКОЕ команды при помощи fuzzywuzzy
def recognizer_cmd(cmd):
    # НЕЧЕТКОЕ сравнение полученой команды из ячейки настроек cmds
    RC = {'cmd':'','percent':0}

    # Получаем Ключи и Значения ячейкир настроек cmds, (нас интересуют только значения, ключ будет нуден когда мы узнаем ЗНАЧЕНИЕ)
    for c,v in opts['cmds'].items():

        # Проверяем НЕЧЕТКОЕ совпадения команды и Значения
        for x in v:
            vrt = fuzz.ratio(cmd,x)

            # И оставляем самую похожую на то что произнес пользователь команду
            if vrt > RC['percent']:
                # Выбираем КЛЮЧ-команду которму соответсвует комманда-значение
                RC['cmd'] = c

                RC['percent'] = vrt     # [log] Распознано мопс время {'cmd': 'ctime', 'percent': 67}
                #print(RC)
    return RC

# Исполнение команды
def execute_cmd(cmd):


    # Сказать текущее время (узнать время кодом, передать на озвучку помошнику полученую строку)
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Сейчас ' + str(now.hour)+' : ' + str(now.minute))


    # Воспроизвести Радио
    elif cmd == 'radio':
        os.system('E:/Python/Projects/NOX/09f85c8c0e74.mp3')


    # Расказать анегдот
    elif cmd == 'stupid':
        speak('Ни один анегдот пока не загружен')


    else:
        print('Команда не распознана, пожалуйста повторите')
        speak('Команда не распознана, пожалуйста повторите')




# Говорить (функция произнесения помошником полученых из кода текстовых (str) данных)
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()




# Начало
# Запуск Распознавания голоса
r = sr.Recognizer()
# Выбор устройства для передачи голоса (микрофон)
m = sr.Microphone(device_index = 1)


#Обработка команды
# Используем  выбраный микрофон для распознавания голоса
with m as source:
    # adjust_for_ambient_noise  в течении указаного времени(0.5 сек) слушает фоновый шум что бы потом не путать его с речью человека
    r.adjust_for_ambient_noise(source)
    #r.adjust_for_ambient_noise(source, duration=0.5)



#-------------------------------------------------------------------------------------------------------
# Голос Помошника
speak_engine = pyttsx3.init()

# Дефалтный помошник, ВАЖНО перевести на РУССКИЙ язык текста иначе будет распознавать только английский!( в реестре можно глянуть остальыне языки)
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
speak_engine.setProperty('voice', ru_voice_id)


# ТОЛЬКО если установлены ОТЛИЧНЫЕ ОТ ДЕФОЛТНЫХ голоса речи для помошника
#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voices', voices[4].id)
#------------------------------------------------------------------------------------------------------


speak('Добрый День, Нокс активен')

# РАСПОЗНАВАНИЕ ГОЛОСОВОЙ КОМАНДЫ  через GOOGLE распознаватель голоса
try:
    while True:
        with m as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            result = r.recognize_google(audio, language='ru-RU').lower()
            result = result.lower()
            print(f'{result}')

            if result.startswith(opts["alias"]):

                # Обращение к помошнику полной фразой
                cmd = result
                # Очистка команды для Обращение к NOX(cmd) ЧИСТОЙ КОМАНДОЙ без лишнего шума( имен , слов паразитов и т.д.)
                for x in opts['alias']:
                    cmd.replace(x, '').strip()
                for x in opts['tbr']:
                    cmd.replace(x, '').strip()

                # Распознавание оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
                cmd = recognizer_cmd(cmd)
                # ИСПОЛНЕНИЕ оставшейся ЧИСТОЙ КОМАНДЫ (cmd)
                execute_cmd(cmd['cmd'])

except Exception as e:
    print(e)
    print('Сбой Сервера Гугл, перезапуск программы')
    #speak('Сбой Сервера Гугл, перезапуск программы')

    # Если конекта с сервером нет или потерян происходит рестарт програмы и реконект с API соответственно гугла
    # Подпроцесс (subprocess.call) Запуска(sys.executable) данного файла ('path/filename.py')
    subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')
