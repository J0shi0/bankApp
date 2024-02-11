from datetime import date
import re
import os

acc_money = 0
acc_created = 0
password_val = 0
user_info = {}
login_and_password = {}
user_transactions = {}


def input_initials():
    trys = 0
    p = re.compile(r'.*[^a-zA-Zа-яА-Я]+.*')

    while trys != 3:
        initials = input("Введите ФИО (три слова через пробел):").strip()
        m = p.match(''.join(initials.split()))
        if len(initials.split()) == 3 and m is None:
            return ' '.join(initials.split())
        else:
            print(f"Пожалуйста, введите ФИО из трех слов, разделенных пробелами.\n Осталось {2 - trys} попытки.")
            trys += 1
    return


def input_birthyear():
    trys = 0
    while trys != 3:
        try:
            today = date.today()
            birth_year = int(input("Введите год рождения:"))
            if len(str(birth_year)) == 4 and birth_year < today.year:
                age = today.year - birth_year
                print(f"Возраст: {age}\n")
                return birth_year
            else:
                print(f'Пожалуйста, введите число четырехзначное или не больше нынешнего года.\n'
                      f'Осталось {2 - trys} попытки.')
                trys += 1
        except ValueError:
            print(f'Неправильный ввод')
            trys += 1
    return


def input_password():
    trys = 0
    while trys != 3:
        password = input("Создайте пароль для аккаунта:")
        if password.strip():
            return password
        print(f"Пожалуйста, введите пароль.\nОсталось {2 - trys} попытки.")
        trys += 1
        return


def create_acc():
    info = {
        "ФИО": input_initials(),
        "Год.рождения": input_birthyear(),
        'Деньги': 0,
        'Лимит': 0
    }
    acc_info = {
        "Логин": info['ФИО'],
        "Пароль": password_hash(input_password())
    }
    acc_val = 1

    if info['ФИО'] is None or info['Год.рождения'] is None or acc_info['Пароль'] is None:
        info = {}
        acc_info = {}
        acc_val = 0
        print("Аккаунт не был зарегестрирован, из-за неправильного ввода данных.\n")

    else:
        print("Аккаунт успешно зарегистрирован!\n")

    return info, acc_info, acc_val


def password_check(password):
    user_password = password_hash(input("Введите пароль:"))
    if user_password == password:
        pass_val = 1
        print("Пароль верный.")
        return pass_val
    else:
        pass_val = 0
        print("Пароль неверный! Завершаем операцию.")
        return pass_val


def add_money(money, limit):
    try:
        print(f'Лимит пополнения счета {limit}.')
        added_money = float(input("Введите сумму пополнения:"))
        if limit >= money + added_money or limit == 0:
            money += added_money
            print("Счёт успешно пополнен!")
        else:
            print("Превышен лимит.")
    except ValueError:
        print(f'Колличество пополнения небходимо ввести число. Выберите операцию и попробуйте снова.')
    return money


def money_withdraw(money):
    print(f"Ваш баланс: {money}")
    withdraw_amount = int(input("Введите сумму для снятия:"))
    if withdraw_amount <= money:
        money -= withdraw_amount
        print(f"Снятие успешно завершено, ваш баланс: {money}")
        return money
    else:
        print("Запрашиваемая сумма для снятния больше, чем ваш балланс.\nЗарешаем операцию.")


def add_transaction(transactions):
    try:
        trans_sum = float(input("Сумма транзакции:"))
        trans_comm = input("Коментарий к транзакции:")
        if len(transactions) == 0:
            transactions[trans_comm] = trans_sum
        else:
            for trans_name in list(transactions):
                if trans_name == trans_comm:
                    transactions[trans_name] += trans_sum
                else:
                    transactions[trans_comm] = trans_sum
        print("Транзакция успешно добавлена")
        return transactions
    except ValueError:
        return transactions


def trans_stats(trans):
    stat = {}
    values = trans.values()
    if len(values) == 0:
        print("Нет ожидаемых транзакций.")
        return
    for val in values:
        if val in stat:
            stat[val] += 1
        else:
            stat[val] = 1
    for sta in stat:
        print(str(sta) + " руб.: " + str(stat[sta]) + " платеж(а)")


def apply_trans(transac, money, limit):
    for tran in list(transac):
        if limit >= money + transac[tran] or limit == 0:
            money += transac[tran]
            print("Транзакция «" + tran + "» на сумму " + str(transac[tran]) + " руб. успешно применена.")
            del transac[tran]
        else:
            print("Транзакция «" + tran + "» на сумму " +
                  str(transac[tran]) + " руб. не может быть применена (превышен лимит).")
    return transac, money


def all_transactions(iterable, r):
    pool = list(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield list(pool[i] for i in indices)


def filtering_transactions(transactions):
    print('Программа выведет все ожидаемые транзакции, сумма которых не меньше введённого числа.')
    threshold = float(input("Введите сумму:"))
    for i in range(len(transactions)):
        if i != 0:
            for pairs in (list(all_transactions(transactions.items(), i + 1))):
                if sum(num[1] for num in pairs) > threshold:
                    print(pairs)
        else:
            print('В системе нет ожидаемых операция.')
        print()


def print_balance(money):
    print("Ваш баланс:", money)


def set_limit():
    limit = float(input("Введите максимальную сумму, которая должна быть на счету (лимит): "))
    if limit >= 0:
        print("Лимит успешно установлен.")
        return limit
    else:
        print('Лимит не может быть отрицательным.')


def save_acc(info, file_name, name=None):
    if file_name == "login-password":
        if not os.path.isfile("C:/Users/joji/PycharmProjects/bankingApp/login-password.txt"):
            with open(f'{file_name}.txt', "a") as fir:
                fir.close()
            with open(f'{file_name}.txt', "w") as c:
                for bit in info:
                    c.write(f"{bit}|{info[bit]}|")
                c.write(f"\n")
                c.close()
        else:
            with open(f'{file_name}.txt', "r") as sec:
                lines = "".join(sec.readlines()).split("\n")[:-1]
                sec.close()
            if len(lines) != 0:
                with open(f'{file_name}.txt', "w") as b:
                    for line in lines:
                        if line.split("|")[1] != name:
                            b.write(f'{line}\n')
                        else:
                            pass
                    for bit in info:
                        b.write(f"{bit}|{info[bit]}|")
                    b.write(f"\n")
                    b.close()

    else:
        fw = open(f'{file_name}_{user_info["ФИО"]}.txt', "w")
        for bit in info:
            fw.write(f"{bit}|{info[bit]}")
            fw.write(f"\n")
        fw.close()


def upload_acc(name, file_name):
    try:
        if file_name == "login-password":
            fr = open(f"{file_name}.txt", 'r')
            data = {}
            data_read = fr.read().split("\n")[:-1]
            for bit in data_read:
                if bit.split("|")[1] == name:
                    for i in range(len(bit.split("|"))):
                        if i % 2 == 0:
                            com = bit.split("|")[i]
                        else:
                            info = bit.split("|")[i]
                            data[com] = info
        else:
            fr = open(f"{file_name}_{name}.txt", 'r')
            data = {}
            data_read = fr.read().split("\n")[:-1]
            for bit in data_read:
                com = bit.split("|")[0]
                if bit.split("|")[1].split(".")[0].isdigit():
                    money = float(bit.split("|")[1])
                    data[com] = money
                else:
                    info = bit.split("|")[1]
                    data[com] = info
        fr.close()
        return data
    except FileNotFoundError:
        print('Пользователя с таким именем нет в сисетме.')
        exit()


def password_hash(password):
    symbol_sum = 0
    symbol_product = 0
    for symbol in password:
        symbol_sum += ord(symbol)
        symbol_product *= ord(symbol)
    return str(symbol_sum % 1234001651) + str(symbol_product % 1234001651)


def exit_program():
    print("Спасибо за пользование нашей программой, до свидания!")
    quit()  # Exit the program


print("Добро пожаловать!")

menu = {
    1: create_acc,
    2: password_check,
    3: add_money,
    4: money_withdraw,
    5: add_transaction,
    6: trans_stats,
    7: apply_trans,
    8: filtering_transactions,
    9: set_limit,
    10: print_balance,
    11: upload_acc,
    12: exit_program
}

dic = {
    3: 'user_info["Деньги"] = menu[3](user_info["Деньги"], user_info["Лимит"])',
    4: 'user_info["Деньги"] = menu[4](user_info["Деньги"])',
    5: 'user_transactions = menu[5](user_transactions)',
    6: 'menu[6](user_transactions)',
    7: 'user_transactions, acc_money = menu[7](user_transactions, user_info["Деньги"], user_info["Лимит"])',
    8: 'menu[8](user_transactions)',
    9: 'user_info["Деньги"] = menu[9]()',
    10: 'menu[10](user_info["Деньги"])',
    11: 'user_info, user_transactions = menu[11]()',
    12: 'menu[12]()'
}

if __name__ == "__main__":
    while True:
        print()
        if len(user_info) != 0:
            print(f'Пользователь: {user_info["ФИО"]}')
        else:
            print(f'Пользователь: ---')

        if password_val == 0:
            password_check_phrase = "Пароль не введен"
        else:
            password_check_phrase = "Пароль введен"
        print(f'Выбирете операцию, которую хотите совершить:'
              f'\n1.Создать аккаунт\n'
              ,'-'*10,
              f'\n(При остуствии пользователя в сессии,'
              f'\nсоданный аккаунт автоматически входит в аккаунт. '
              f'\nПри присутствии пользователя в сессии,'
              f'\nзаменяет существующего пользователя на созданого).\n'
              ,'-'*10,
              f'\n2.Ввести пароль ({password_check_phrase}).'
              f'\n3.Положить деньги на счет.\n4.Снять деньги.\n5.Создать новую транзакцию.'
              f'\n6.Статистика по ожидаемым пополнениям.\n7.Применит ожидаймые транзакции к счету.'
              f'\n8.Фильтрация ожидаемых транзакций.\n9.Выставить лимит на счет.\n10.Вывести баланс на экран.'
              f'\n11.Войти или сменить в аккунт.\n12.Выйти из программы.')
        print()

        try:
            menu_option = int(input("Введите номер операции здесь:"))

            if menu_option in menu:
                if menu_option == 1:
                    user_info, login_and_password, acc_created = create_acc()
                elif menu_option == 2 and acc_created == 1:
                    password_val = password_check(login_and_password["Пароль"])
                elif acc_created == 1 and password_val == 1:
                    for i in dic:
                        if menu_option == i:
                            exec(dic[i])
                elif menu_option == 11:
                    user_name = input("Введите ваше ФИО:")
                    user_info = upload_acc(user_name, "user_info")
                    user_info["Год.рождения"] = int(user_info["Год.рождения"])
                    user_transactions = upload_acc(user_name, "user_transactions")
                    login_and_password = upload_acc(user_name, "login-password")
                    acc_created = 1
                elif menu_option == 12:
                    exec(dic[12])
                else:
                    print("Невозможно выполнить операцию. Ваш аккаунт еще не создан или не введен пароль.")
            else:
                print("Неправильно введен номер операции.")

        except ValueError:
            print("Недопустимый ввод!")
            print()

        if len(user_info) != 0:
            save_acc(user_info, "user_info")
            save_acc(user_transactions, "user_transactions")
            save_acc(login_and_password, "login-password", login_and_password["Логин"])
