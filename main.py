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
        if "".join(password.split()):
            return password
        else:
            print(f"Пожалуйста, введите пароль без пробелов.\nОсталось {2 - trys} попытки.")
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
    pas_val = 0

    if info['ФИО'] is None or info['Год.рождения'] is None or acc_info['Пароль'] is None:
        info = {}
        acc_info = {}
        acc_val = 1
        pas_val = 0
        print("Аккаунт не был зарегестрирован, из-за неправильного ввода данных.\n")

    else:
        print("Аккаунт успешно зарегистрирован!\n")

    return info, acc_info, acc_val, pas_val


def password_check(password):
    inputed_password = password_hash(input("Введите пароль:"))
    if inputed_password == password:
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
    try:
        print(f"Ваш баланс: {money}")
        withdraw_amount = int(input("Введите сумму для снятия:"))
        if withdraw_amount <= money:
            money -= withdraw_amount
            print(f"Снятие успешно завершено, ваш баланс: {money}")
        else:
            print("Запрашиваемая сумма для снятния больше, чем ваш балланс.\nЗарешаем операцию.")
        return money
    except ValueError:
        print("Неправильный ввод. Небходимо ввести число.\nЗарешаем операцию.")
        return money


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


def found_str_value(part, str_name, file_name):
    try:
        with open(f"{file_name + "_"}{part}.txt", 'r') as f:
            lines = f.read().split("\n")[:-1]
            for line in lines:
                if line.split("|")[0] == str_name:
                    value = float(line.split("|")[1])
                else:
                    pass
            f.close()
        return value
    except (UnboundLocalError, FileNotFoundError) as error:
        raise RuntimeError("Скорее всего функция не нашла нужную строку или файл.") from error


def overwrite_string_value(part, str_name, file_name, new_value):
    with open(f'{file_name + "_"}{part}.txt', "r") as f:
        lines = f.read().split("\n")[:-1]
        f.close()
    with open(f'{file_name}_{part}.txt', "w") as b:
        for line in lines:
            if line.split("|")[0] != str_name:
                b.write(f'{line}\n')
            else:
                b.write(f'{line.split("|")[0]}|{new_value}\n')
        b.close()


def list_of_recipients(sender):
    with open('login-password.txt', "r") as fr:
        lines = fr.read().split("\n")[:-1]
        fr.close()
    for line in lines:
        if line.split("|")[1] != sender:
            yield line.split("|")[1]
        elif len(lines) == 1 and line.split("|")[1] == sender:
            return


def create_transactions(sender, sender_money, file_name):
    print(f'Отправитель: {sender}')

    print()
    print(f'Лист отправителей в системе:')
    for participient in list_of_recipients(sender):
        if participient is None:
            return sender_money
        else:
            print(participient)
    print()
    recipient = input(f'Введите имя получателя:')

    try:
        sender_money = found_str_value(sender, "Деньги", "user_info")
        print(f'Если на счете получателя недостаточно денег, '
              f'то будет операция будет оложена до пополнения счета отправителя.')
        transaction_amount = float(input(f'Введите сумму, которыую хотите отправить:'))
        recipient_money = found_str_value(recipient, "Деньги", "user_info")
        if sender_money >= transaction_amount:
            overwrite_string_value(sender, "Деньги", file_name, sender_money - transaction_amount)
            overwrite_string_value(recipient, "Деньги", file_name, recipient_money + transaction_amount)
            print(f'{transaction_amount} успешно отправлены.\n ')
            return sender_money - transaction_amount
        else:
            with open(f'delayed_transactions.txt', "a") as f:
                print(f'На вашем счету недостаточно средаств.\n Создан отложенный перевод:'
                      f' Отправитель:{sender}|Получатель:{recipient}|Сумма перевода:{transaction_amount}')
                f.write(f'{sender}|{recipient}|{transaction_amount}\n')
                f.close()
            return sender_money
    except (FileNotFoundError, RuntimeError):
        print(f'В системе нет пользователя с именем {recipient}.')
        return sender_money


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
        current_directory = os.getcwd()
        if not os.path.isfile(f"{current_directory}\\login-password.txt"):
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


def delete_line(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for index, line in enumerate(lines, 0):
            if index != line_number:
                file.write(line)


def delayed_transaction_execution(money, name=None):
    current_user_mon = money
    try:
        with open(f"delayed_transactions.txt", 'r') as f:
            lines = f.read().split("\n")[:-1]
            for line in lines:
                value = float(line.split("|")[2])
                sen_mon = found_str_value(line.split("|")[0], "Деньги", "user_info")
                res_mon = found_str_value(line.split("|")[1], "Деньги", "user_info")
                if sen_mon > value:
                    overwrite_string_value(line.split("|")[0], "Деньги", "user_info", sen_mon - value)
                    overwrite_string_value(line.split("|")[1], "Деньги", "user_info", res_mon + value)
                    delete_line("delayed_transactions.txt", lines.index(line))
                    if name == line.split("|")[0]:
                        current_user_mon = sen_mon - value
                else:
                    pass
        f.close()
        if current_user_mon is not None:
            return current_user_mon
        else:
            return sen_mon
    except FileNotFoundError:
        return current_user_mon


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
    9: create_transactions,
    10: set_limit,
    11: print_balance,
    13: exit_program
}

dic = {
    3: 'user_info["Деньги"] = menu[3](user_info["Деньги"], user_info["Лимит"])',
    4: 'user_info["Деньги"] = menu[4](user_info["Деньги"])',
    5: 'user_transactions = menu[5](user_transactions)',
    6: 'menu[6](user_transactions)',
    7: 'user_transactions, acc_money = menu[7](user_transactions, user_info["Деньги"], user_info["Лимит"])',
    8: 'menu[8](user_transactions)',
    9: 'user_info["Деньги"] =  menu[9](login_and_password["Логин"], user_info["Деньги"], "user_info")',
    10: 'user_info["Деньги"] = menu[10]()',
    11: 'menu[11](user_info["Деньги"])',
    13: 'menu[13]()'
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
              , '-' * 10,
              f'\n(При остуствии пользователя в сессии,'
              f'\nсоданный аккаунт автоматически входит в аккаунт. '
              f'\nПри присутствии пользователя в сессии,'
              f'\nзаменяет существующего пользователя на созданого).\n'
              , '-' * 10,
              f'\n2.Ввести пароль ({password_check_phrase}).'
              f'\n3.Положить деньги на счет.\n4.Снять деньги.\n5.Создать новую транзакцию.'
              f'\n6.Статистика по ожидаемым пополнениям.\n7.Применит ожидаймые транзакции к счету.'
              f'\n8.Фильтрация ожидаемых транзакций.\n9.Создать перевод.\n10.Выставить лимит на счет.'
              f'\n11.Вывести баланс на экран.\n12.Войти или сменить в аккунт.\n13.Выйти из программы.')
        print()

        try:
            menu_option = int(input("Введите номер операции здесь:"))

            if menu_option in menu or menu_option == 12:
                if menu_option == 1:
                    user_info, login_and_password, acc_created, password_val = create_acc()
                elif menu_option == 2 and acc_created == 1:
                    password_val = password_check(login_and_password["Пароль"])
                elif acc_created == 1 and password_val == 1:
                    for i in dic:
                        if menu_option == i:
                            exec(dic[i])
                elif menu_option == 12:
                    user_name = input("Введите ваше ФИО:")
                    user_info = upload_acc(user_name, "user_info")
                    user_info["Год.рождения"] = int(user_info["Год.рождения"])
                    user_transactions = upload_acc(user_name, "user_transactions")
                    login_and_password = upload_acc(user_name, "login-password")
                    acc_created = 1
                elif menu_option == 13:
                    exec(dic[menu_option])
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
            user_info["Деньги"] = delayed_transaction_execution(user_info["Деньги"], login_and_password["Логин"])
