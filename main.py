from datetime import date
import re

acc_money = 0
acc_created = 0
password_val = 0
user_info = {}
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
        "Пароль": input_password(),
        'Деньги': 0,
        'Лимит': 0
    }
    acc_val = 1

    if info['ФИО'] is None or info['Год.рождения'] is None or info['Пароль'] is None:
        info = {}
        acc_val = 0
        print("Аккаунт не был зарегестрирован, из-за неправильного ввода данных.\n")

    else:
        print("Аккаунт успешно зарегистрирован!\n")

    return info, acc_val


def password_check(password):
    user_password = input("Введите пароль:")
    if user_password == password:
        pass_val = 1
        print("Пароль верный.")
        return pass_val
    else:
        pass_val = 0
        print("Пароль неверный! Завершаем операцию.")
        return pass_val


def add_money(money, limit):
    print(f'Лимит пополнения счета {limit}.')
    added_money = float(input("Введите сумму пополнения:"))
    if limit >= money + added_money or limit == 0:
        money += added_money
        print("Счёт успешно пополнен!")
    else:
        print("Превышен лимит.")
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


def save_acc(info, transactions):
    fw = open(str(user_info["ФИО"]) + 'data.txt', 'w')
    for bit in info:
        fw.write(str(bit) + "," + str(user_info[bit]) + ";")
    fw.write("\n")
    for name in transactions:
        fw.write(str(name) + "|" + str(transactions[name]) + "\n")
    fw.close()


def print_balance(money):
    print("Ваш баланс:", money)


def set_limit():
    limit = float(input("Введите максимальную сумму, которая должна быть на счету (лимит): "))
    if limit >= 0:
        print("Лимит успешно установлен.")
        return limit
    else:
        print('Лимит не может быть отрицательным.')


def upload_acc():
        us_in = {}
        name = input("Введите ваше ФИО:")
        fr = open(name + 'data.txt', 'r')
        u_d = fr.readline().split(";")[:-1]
        for item in u_d:
            key = item.split(",")[0]
            value = item.split(",")[1]
            us_in[key] = value
        tran_data = {}
        t_d = fr.read().split("\n")[:-1]
        for tran in t_d:
            com = tran.split("|")[0]
            money = float(tran.split("|")[1])
            tran_data[com] = money
        fr.close()
        print(f'Данные пользователя [{name}] успещно восстановлены.')
        return us_in, tran_data


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
        print(
            "Выбирете операцию, которую хотите совершить:\n1.Создать аккаунт\n2.Ввести пароль.\n"
            "3.Положить деньги на счет\n4.Снять деньги\n5.Создать новую транзакцию\n"
            "6.Статистика по ожидаемым пополнениям.\n7.Применит ожидаймые транзакции к счету.\n"
            "8.Фильтрация ожидаемых транзакций.\n9.Выставить лимит на счет\n10.Вывести баланс на экран\n"
            "11.Восстановить данные аккаунта данные аккаунта.\n12.Выйти из программы")
        print()

            menu_option = int(input("Введите номер операции здесь:"))

            if menu_option in menu:
                if menu_option == 1:
                    user_info, acc_created = create_acc()
                elif menu_option == 2 and acc_created == 1:
                    password_val = password_check(user_info["Пароль"])
                elif acc_created == 1 and password_val == 1:
                    for i in dic:
                        if menu_option == i:
                            exec(dic[i])
                elif menu_option == 11:
                    exec(dic[11])
                    user_info['Деньги'] = float(user_info['Деньги'])
                    user_info['Лимит'] = float(user_info['Лимит'])
                    acc_created = 1
                elif menu_option == 12:
                    exec(dic[12])
                else:
                    print("Невозможно выполнить операцию. Ваш аккаунт еще не создан или не введен пароль.")
            else:
                print("Неправильно введен номер операции.")


    if len(user_info) != 0:
        save_acc(user_info, user_transactions)