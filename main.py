# Импорт необходимых библиотек
import os
import re
import sys
import csv
import time
import pandas
import pathlib
import itertools


# Импорт самописных функций
from func_io import scan_folder, clear_folder, access_file, find_file, sys_exit
from func_io import print_cmd, word_fix, get_key
from func_csv import count_csv
from func_sub import counter_rows_col, get_parametrs_from_io_list, parametr_counter

# Старт таймера выполнения программы
start = time.time()

# Заставка для терминального окна
print_cmd("==================================")
print_cmd("===SUPCON_LOGIC_GENERATOR_v1.60===")
print_cmd("==================================\n")

print_cmd("=/=/= Начата инициализация программы =/=/=\n")

# Создания словаря с абсолютными путями до рабочих папок
root_path = dict()

# Заполнение словаря с абсолютными путями до рабочих папок
root_path['root'] = \
    os.path.dirname(os.path.abspath(__file__))
root_path['temp'] = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TEMP_FILES')
root_path['template'] = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TEMPLATE_LOGIC')
root_path['logic'] = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'COMPLETE_LOGIC')

# Создание папок в корневой папке, где лежит файл программы, если их нет
pathlib.Path(root_path['temp']).mkdir(parents=True, exist_ok=True)
pathlib.Path(root_path['template']).mkdir(parents=True, exist_ok=True)
pathlib.Path(root_path['logic']).mkdir(parents=True, exist_ok=True)

# Удаление временных файлов и файлов программ до выполнения программы
clear_folder(root_path['temp'])
clear_folder(root_path['logic'])

# Создание словаря с абсолютными путями до файлов шаблонов в папке "TEMP_FILES"
templates_PATH = dict()

# Сканирование корневой папки с шаблонами и заполнение словаря
scan_folder(root_path['template'], templates_PATH)

# Проверка словаря с шаблонами
if len(templates_PATH) == 0:
    print_cmd("В папке '" + root_path['template'] + "' отсутствуют шаблоны!\n")
    sys_exit()
else:
    print_cmd("Сканирование папки '" + root_path['template'] +
              "' c шаблонами успешно выполнено, обнаружено " +
              "' c шаблонами успешно выполнено, обнаружено " +
              str(len(templates_PATH)) + " шаблон" +
              word_fix(len(templates_PATH), "", "а", "ов") + "!\n")

# Вывод словаря с абсолютными путями до файлов с шаблонами
print_cmd("Вывод словаря с абсолютными путями до файлов шаблонов:\n")
print_cmd(templates_PATH)
print_cmd('')

# Определение расширения файла Excel 'LOOP_BOOK'
LB_TYPE_XLS = find_file(root_path['root'], "LOOP_BOOK.xls")
LB_TYPE_XLSX = find_file(root_path['root'], "LOOP_BOOK.xlsx")

# Объявление переменной с хранением типа файла Excel
TYPE_EXCEL = ''

# Проверка типа Excel файла
if LB_TYPE_XLSX:
    TYPE_EXCEL = pathlib.Path(LB_TYPE_XLSX[0]).suffix
elif LB_TYPE_XLS:
    TYPE_EXCEL = pathlib.Path(LB_TYPE_XLS[0]).suffix

# Проверка наличия файла таблицы Excel LOOP_BOOK и доступа к ней
if access_file(os.path.join(root_path['root'], 'LOOP_BOOK' + TYPE_EXCEL)):
    print_cmd("Таблица 'LOOP_BOOK' доступна!\n")
else:
    print_cmd("Таблица 'LOOP_BOOK' недоступна!\n")
    sys_exit()

# Определение расширения файла Excel 'IO_LIST_BGCC'
LB_TYPE_XLS_IO = find_file(root_path['root'], "IO_LIST_BGCC.xls")
LB_TYPE_XLSX_IO = find_file(root_path['root'], "IO_LIST_BGCC.xlsx")

# Объявление переменной с хранением типа файла Excel
TYPE_EXCEL_IO = ''

# Проверка типа Excel файла
if LB_TYPE_XLSX_IO:
    TYPE_EXCEL_IO = pathlib.Path(LB_TYPE_XLSX_IO[0]).suffix
elif LB_TYPE_XLS_IO:
    TYPE_EXCEL_IO = pathlib.Path(LB_TYPE_XLS_IO[0]).suffix

# Проверка наличия файла таблицы Excel IO_LIST_BGCC и доступа к ней
if access_file(os.path.join(root_path['root'], 'IO_LIST_BGCC' + TYPE_EXCEL_IO)):
    print_cmd("Таблица 'IO_LIST_BGCC' доступна!\n")
else:
    print_cmd("Таблица 'IO_LIST_BGCC' недоступна!\n")
    sys_exit()

print_cmd("=/=/= Инициализация программы завершена =/=/=\n")

print_cmd("=/=/= Начата обработка Excel файла =/=/=\n")

# Открытие Excel LOOP_BOOK и определение листов в ней
LOOP_BOOK = pandas.ExcelFile(os.path.join(root_path['root'], 'LOOP_BOOK' +
                                          TYPE_EXCEL),
                             engine='openpyxl')
LOOP_BOOK_SHEETS = LOOP_BOOK.sheet_names
print_cmd("Таблица 'LOOP_BOOK' содержит следующие листы:")
print_cmd(LOOP_BOOK_SHEETS)
print_cmd('')

# Подсчет количества строчек/колонок в таблицах Excel [LOOP_BOOK]
loop_DICT, LB_1_ROW, LB_1_COLUMN = counter_rows_col(root_path['root'], LOOP_BOOK,
                                                    'LOOP', 'LOOP_NAME', True)
prg_DICT, LB_2_ROW = counter_rows_col(root_path['root'], LOOP_BOOK,
                                      'PROG', 'PROG_DESC')
swtype_DICT, LB_3_ROW = counter_rows_col(root_path['root'], LOOP_BOOK,
                                         'SW_TYPE', 'SW_TYPE')
swtype_rules_DICT, LB_4_ROW = counter_rows_col(root_path['root'], LOOP_BOOK,
                                               'SW_TYPE_BLOCK_RULES', 'SW_TYPE')
calc_DICT, LB_5_ROW = counter_rows_col(root_path['root'], LOOP_BOOK,
                                       'CALC', 'FUNCTION')
param_DICT = dict()

# Вывод количества имеющихся данных в таблице Excel
print_cmd("В листе 'LOOP' содержится " + str(LB_1_ROW) + " контур" +
          word_fix(LB_1_ROW, "", "а", "ов") + " и " + str(LB_1_COLUMN) +
          " параметр" + word_fix(LB_1_COLUMN, "!", "а!", "ов!"))
print_cmd("В листе 'PROG' содержится " + str(LB_2_ROW) + " программ" +
          word_fix(LB_2_ROW, "а!", "ы!", "!"))
print_cmd("В листе 'SW_TYPE' содержится " + str(LB_3_ROW) + " тип" +
          word_fix(LB_3_ROW, "", "а", "ов") + " контуров!")
print_cmd("В листе 'SW_TYPE_BLOCK_RULES' содержится " + str(LB_4_ROW) + " тип" +
          word_fix(LB_4_ROW, "", "а", "ов") + " контуров!")
print_cmd("В листе 'CALC' содержится " + str(LB_5_ROW) + " тип" +
          word_fix(LB_5_ROW, "", "а", "ов") + " контуров!\n")

# Открытие Excel IO_LIST_BGCC и определение листов в ней
IO_LIST_BGCC = pandas.ExcelFile(os.path.join(root_path['root'], 'IO_LIST_BGCC' +
                                             TYPE_EXCEL_IO),
                                engine='openpyxl')
IO_LIST_BGCC_SHEETS = IO_LIST_BGCC.sheet_names
print_cmd("Таблица 'IO_LIST_BGCC' содержит следующие листы:")
print_cmd(IO_LIST_BGCC_SHEETS)
print_cmd('')

# Подсчет количества строчек/колонок в таблицах Excel [IO_LIST_BGCC]
IO_DICT = counter_rows_col(root_path['root'], IO_LIST_BGCC,
                           'IO_LIST', 'TAG', False, False)

print_cmd("=/=/= Обработка Excel файла завершена =/=/=\n")

print_cmd("=/=/= Начата генерация файлов программ =/=/=\n")

print_cmd("=/=/= Начата генерация временных файлов шапок программ =/=/=\n")

# Выполнение замены параметров в csv шапки программ в соответствии с Excel
for PRG_ID in range(LB_2_ROW):
    if prg_DICT['PROG_DESC'][PRG_ID] != 'EMPTY':
        with open(templates_PATH['BASE_0000_0000'],
                  'r', newline='', encoding='cp1251') as f_input, \
                open(os.path.join(root_path['temp'],
                                  prg_DICT['PROG_NAME'][PRG_ID] + '_BASE.csv'),
                     'w', newline='', encoding='cp1251') as f_output:
            # Чтение файла в переменную
            file_input = f_input.read()

            # Выполнение замен ключевых слов на параметры из Excel - словаря
            csv_str = re.sub('PROG_NAME', prg_DICT['PROG_NAME'][PRG_ID],
                             file_input)
            csv_str = re.sub('PROG_DESC', prg_DICT['PROG_DESC'][PRG_ID],
                             csv_str)
            csv_str = re.sub('PROG_CYCLE', str(prg_DICT['PROG_CYCLE'][PRG_ID]),
                             csv_str)
            csv_str = re.sub('PROG_PHASE', str(prg_DICT['PROG_PHASE'][PRG_ID]),
                             csv_str)

            # Запись файла из переменной
            file_output = f_output.write(csv_str)

        print_cmd("Сгенерирован временный файл шапки программы " +
                  prg_DICT['PROG_NAME'][PRG_ID] + "!")

print_cmd('')

print_cmd("=/=/= Генерация временных файлов шапок программ завершена =/=/=\n")

print_cmd("=/=/= Начата генерация временных файлов готовых контуров =/=/=\n")

# Выполнение открытия файлов для переноса строк из шаблона в промежуточный файл
for LOOP_ID in range(LB_1_ROW):
    template = loop_DICT['SW_TYPE'][LOOP_ID]
    loop_name = loop_DICT['LOOP_NAME'][LOOP_ID]
    print_cmd(f"Начата генерация временного файла готового контура {loop_name}"
              f" по шаблону {template}!")

    with open(templates_PATH[template],
              'r', newline='', encoding='cp1251') as f_input, \
            open(os.path.join(root_path['temp'],
                              'LOOP_' + loop_name +
                              '_PRERAW.CSV'),
                 'w', newline='', encoding='cp1251') as f_output:

        # Чтение файлов в переменные
        csv_input = csv.reader(f_input)
        csv_output = csv.writer(f_output)

        # Подчистка первых строк шапки для корректной работы pandas
        csv_output.writerows(itertools.islice(csv_input, 3,
                            count_csv(templates_PATH[template])))

    # Перевод файла csv в словарь при помощи pandas
    df = pandas.read_csv(os.path.join(root_path['temp'], 'LOOP_' +
                                      loop_name +
                                      '_PRERAW.CSV'),
                         encoding='cp1251', encoding_errors='ignore',
                         dtype=object).to_dict()

    # Перестановка имени контура между столбцами, если не Null
    if df['Original Logic Name'][0] != df['Original Logic Name'][0]:
        pass
    else:
        df['Logic Name'][0] = loop_name + '_LOOP'

    # Перестановка комментариев контура между столбцами, если не Null
    for i in range(len(df['Original Remark'])):
        if df['Original Remark'][i] != df['Original Remark'][i]:
            pass
        else:
            df['Remark'][i] = df['Original Remark'][i]

    print_cmd('', flag_print=False)
    print_cmd(df, flag_print=False)
    print_cmd('', flag_print=False)
    # =================================================================
    param_DICT = get_parametrs_from_io_list(LOOP_ID, loop_DICT, swtype_rules_DICT,
                                            IO_DICT, calc_DICT, param_DICT)
    # =================================================================
    # Перевод отредактированного словаря в файл csv при помощи pandas
    dg = pandas.DataFrame.from_dict(df, orient='columns')

    # Выполнение замены параметров в виде как отдельные ячейки
    for i in range(1, LB_1_COLUMN - 3):
        par = 'P' + str(i)
        if loop_DICT[par][LOOP_ID] != loop_DICT[par][LOOP_ID]:
            pass
        else:
            dg = dg.replace(r'^' + par + '$', loop_DICT[par][LOOP_ID], regex=True)

    # Выполнение замены параметров в виде как текст в составе ячейки
    for i in reversed(range(1, LB_1_COLUMN - 3)):
        par = 'P' + str(i)
        if loop_DICT[par][LOOP_ID] != loop_DICT[par][LOOP_ID]:
            pass
        else:
            dg = dg.replace(par, loop_DICT[par][LOOP_ID], regex=True)
            print_cmd(par + ': ', flag_print=False)
            print_cmd('DESCR - ' +
                      swtype_DICT[par][get_key(swtype_DICT['SW_TYPE'],
                                               template)],
                      flag_print=False)
            print_cmd('VALUE - ' + str(loop_DICT[par][LOOP_ID]), flag_print=False)
            print_cmd('', flag_print=False)

    # Выполнение замены параметров функциональных блоков из SW_TYPE_BLOCK_RULES
    for i in dg['FB Tag Name'].keys():
        fb_name = dg['FB Tag Name'][i]
        if fb_name != fb_name:
            pass
        elif fb_name in param_DICT.keys():
            for k, v in param_DICT[fb_name].items():
                dg.loc[(dg['Param Name'] == k) & (dg.index >= i) &
                       (dg.index < i+parametr_counter(dg, fb_name)),
                       'Param Value'] = v
                print_cmd(f"Параметр {k}\t= {v}", flag_print=False)
        else:
            print_cmd(f"Параметры функционального блока {fb_name} отсутствуют "
                      f"или допущена ошибка в SW_TYPE_BLOCK_RULES шаблона")
            pass

    # Сохранение pandas DataFrame обратно в csv файл
    dg.to_csv(os.path.join(root_path['temp'], 'LOOP_' +
                           loop_DICT['LOOP_NAME'][LOOP_ID] + '_RAW.CSV'),
              encoding='cp1251', index=False)

    # Подчистка заголовков в файле csv
    with open(os.path.join(root_path['temp'], 'LOOP_' + loop_name + '_RAW.CSV'),
              'r', newline='', encoding='cp1251') as f_input, \
            open(os.path.join(root_path['temp'], 'LOOP_' + loop_name + '_FIN.CSV'),
                 'w', newline='', encoding='cp1251') as f_output:

        # Чтение файлов в переменные
        csv_input = csv.reader(f_input)
        csv_output = csv.writer(f_output)

        # Подчистка первых строк шапки
        csv_output.writerows(
            itertools.islice(
                csv_input, 1,
                count_csv(os.path.join(root_path['temp'], 'LOOP_' +
                                       loop_name +
                                       '_RAW.CSV'))))

    print_cmd("Сгенерирован временный файл готового контура " + loop_name +
              " по шаблону " + template + "!\n")

print_cmd("=/=/= Генерация временных файлов готовых контуров завершена =/=/=\n")

print_cmd("=/=/= Начата генерация финальных файлов логики программ =/=/=\n")

# Генерация финального файла csv c шапкой программы
for PRG_ID in range(LB_2_ROW):
    if prg_DICT['PROG_DESC'][PRG_ID] != 'EMPTY':
        with open(os.path.join(root_path['temp'],
                               prg_DICT['PROG_NAME'][PRG_ID] + '_BASE.csv'),
                  'r', newline='', encoding='cp1251') as f_base, \
                open(os.path.join(root_path['logic'],
                                  prg_DICT['PROG_NAME'][PRG_ID] + ' - ' +
                                  prg_DICT['PROG_DESC'][PRG_ID] + '.csv'),
                     'w', newline='', encoding='cp1251') as f_output:

            # Чтение файлов в переменные
            csv_input_1 = csv.reader(f_base)
            csv_output = csv.writer(f_output)

            print_cmd("Начата генерация финального файла логики программы " +
                      prg_DICT['PROG_NAME'][PRG_ID] + " - " +
                      prg_DICT['PROG_DESC'][PRG_ID] + "!")

            # Перенос шапки программы из временного файла в финальный
            csv_output.writerows(itertools.islice(csv_input_1, 0, 4))

            # Добавление в программу данных готовых контуров
            for LOOP_ID in range(LB_1_ROW):
                if loop_DICT['PROG_ID'][LOOP_ID] == PRG_ID + 1:
                    with open(os.path.join(
                            root_path['temp'], 'LOOP_' +
                                               loop_DICT['LOOP_NAME'][LOOP_ID] +
                                               '_FIN.CSV'),
                            'r', newline='', encoding='cp1251') as f_loop:

                        # Чтение файла в переменную
                        csv_input_2 = csv.reader(f_loop)

                        # Инициализация счетчика для подсчета строк в csv в 0
                        rowcount_csv = 0
                        # Итерация счетчика через csv файл
                        for row in open(
                                os.path.join(
                                    root_path['temp'],
                                    'LOOP_' + loop_DICT['LOOP_NAME'][LOOP_ID] +
                                    '_FIN.CSV'), encoding='cp1251'):
                            rowcount_csv += 1

                        # Перенос временного файла готового контура в программу
                        csv_output.writerows(itertools.islice(
                            csv_input_2, rowcount_csv))

                        print_cmd("\tКонтур " + loop_DICT['LOOP_NAME'][LOOP_ID] +
                                  "\tдобавлен в программу!")

            print_cmd("Сгенерирован финальный файл логики программы " +
                      prg_DICT['PROG_NAME'][PRG_ID] + " - " +
                      prg_DICT['PROG_DESC'][PRG_ID] + "!\n")

print_cmd("=/=/= Генерация финальных файлов логики программ завершена =/=/=\n")

# Создание словаря с абсолютными путями до файлов программ в папке
logic_PATH = dict()

# Сканирование корневой папки с программами и заполнение словаря
scan_folder(root_path['logic'], logic_PATH)

# Проверка словаря с готовыми программами
if len(logic_PATH) == 0:
    print_cmd("В папке '" + root_path['logic'] + "' отсутствуют программы!\n")
    sys_exit()
else:
    print_cmd("Сканирование папки '" + root_path['logic'] +
              "' c программами успешно выполнено, обнаружено " +
              str(len(logic_PATH)) + " программ" +
              word_fix(len(logic_PATH), "а", "ы", "") + "!\n")

# Вывод словаря с абсолютными путями до файлов с программами
print_cmd("Вывод словаря с абсолютными путями до файлов программ:\n")
print_cmd(logic_PATH)
print_cmd('')

print_cmd("=/=/= Генерация файлов программ завершена =/=/=\n")

# Финиш таймера выполнения программы
end = time.time() - start
print_cmd("Время выполнения программы составило - " + str(round(end, 2)) +
          " секунд!\n")

# Удаление временных файлов
fin_clear = input(">Очистить временные файлы? (y/n)\n")
print_cmd(">Очистить временные файлы? (y/n)", flag_print=False)
print_cmd(str(fin_clear.lower()), flag_print=False)
print_cmd('')

if fin_clear.lower() == 'y':
    clear_folder(root_path['temp'])
elif fin_clear.lower() == 'n':
    print_cmd("Зачистка папки '" + root_path['temp'] + "' пропущена!\n")
    pass
else:
    print_cmd("Зачистка папки '" + root_path['temp'] + "' пропущена!\n")
    pass

print_cmd("=/=/= Работа программы успешно завершена =/=/=\n")

fin_exit = input(">Нажмите клавишу 'Enter' для выхода из программы<\n")
print_cmd(">Нажмите клавишу 'Enter' для выхода из программы<",
          flag_print=False)

if fin_exit:
    sys.exit()
