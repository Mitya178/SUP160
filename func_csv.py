# Объвление функции счетчика для подсчета строк в csv в 0
def count_csv(path):
    rowcount_csv = 0
    # Итерация счетчика через csv файл
    for row in open(path, encoding='cp1251'):
        rowcount_csv += 1
    return rowcount_csv


# Объвление функции добавления
def add_zero(number):
    string = ''
    if 0 <= number < 10:
        string = '00' + str(id)
    elif 10 <= number < 100:
        string = '0' + str(id)
    elif 100 <= number < 1000:
        string = str(id)
    return string
