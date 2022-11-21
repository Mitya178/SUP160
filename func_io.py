# Импорт необходимых библиотек
import os
import sys
import shutil
import datetime


# Вызов объекта с текущей датой и временем
cur_datatime = datetime.datetime.now()

# Формирование имени лог-файла
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LOG_FILES',
                        'LOG_' + cur_datatime.strftime("%Y_%m_%d_%H_%M_%S") +
                        '.txt')


# Объявление функции аварийного завершение программы
def sys_exit():
    print_cmd("Аварийное завершение программы!")
    sys.exit()


# Объявление функции зачистки папок от файлов
def clear_folder(path_folder):
    for files in os.listdir(path_folder):
        path = os.path.join(path_folder, files)
        try:
            shutil.rmtree(path)
            print_cmd("Зачистка папки '" + path_folder + "' завершена!")
        except OSError:
            os.remove(path)
    return True


# Объявление функции обработки исключений сканирования папок
def walk_error():
    print("Указанный абсолютный путь до папки с шаблонами некорректен!\n")
    print("Аварийное завершение программы!")
    sys.exit()


# Объявление функции сканирования папки и заполнения словаря
def scan_folder(path_folder, dictionary):
    for dirs, folder, files in os.walk(path_folder,
                                       onerror=walk_error):
        for file in files:
            dictionary[os.path.basename(
                os.path.splitext(
                    os.path.join(dirs, file))[0])] = os.path.join(dirs, file)


# Объявление функции проверки наличия файла и доступа к нему в папке
def access_file(path, mode='r'):
    try:
        f = open(path, mode, encoding='cp1251')
        f.close()
    except IOError:
        return False
    return True


# Объявление функции поиска файлов с конкретным расширением
def find_file(dirname, extension):
    return [os.path.join(dirname, filename)
            for filename in os.listdir(dirname)
            if filename.endswith(extension)]


# Объявление функции вывода текста в консоль и записи данной инфы в лог-файл
def print_cmd(text='', flag_print=True, flag_write=True):
    if flag_print:
        print(text)
    if flag_write:
        with open(log_file, 'a', encoding='cp1251') as f:
            print(text, file=f)


# Объявление функции коррекции окончаний слов под склонения числительных
def word_fix(number, strwhen1, strwhen15, strelse):
    if number == 1 or number % 100 == 1:
        text = strwhen1
    elif 1 < number < 5 or 1 < number % 100 < 5:
        text = strwhen15
    else:
        text = strelse
    return text


# Объявление функции поиска ключа по значению в словаре
def get_key(dictionary, value):
    for k, v in dictionary.items():
        if v == value:
            return k


# Объявление функции поиска ключа по значению в словаре (возвращает список)
def get_key_list(dictionary: dict, value) -> list:
    y = []
    for k, v in dictionary.items():
        if v == value:
            y.append(k)
    return y
