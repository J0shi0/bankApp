from datetime import date

import pytest
import os
import main  # The main which contains the call to input


def test_input_initials(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "John Doe Smith")
    assert main.input_initials() == "John Doe Smith"


def test_initials_with_spaces(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "   John   Doe   Smith   ")
    assert main.input_initials() == "John Doe Smith"


def test_input_initials_two_words(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'John Doe')
    assert main.input_initials() is None


def test_more_than_three_words(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "John Doe Smith Johnson")
    assert main.input_initials() is None


def test_digits_only(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "123 456 789")
    assert main.input_initials() is None


def test_digits_and_stings(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "John 456 Johnson")
    assert main.input_initials() is None


def test_digits_in_stings(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "John D0e Johnson")
    assert main.input_initials() is None


def test_cyrillic_characters(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Иванов Иван Иванович")
    assert main.input_initials() == "Иванов Иван Иванович"


def test_non_alphabetic_characters(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "John-Doe-Smith")
    assert main.input_initials() is None


def test_empty_string(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "")
    assert main.input_initials() is None


today = date.today()


def test_valid_birth_year(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1990")
    assert main.input_birthyear() == 1990


def test_invalid_birth_year_less_than_4_digits(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '90')
    assert main.input_birthyear() is None


def test_future_birth_year(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '2050')
    assert main.input_birthyear() is None


def test_invalid_birth_year_not_number(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'abc')
    assert main.input_birthyear() is None


def test_returns_1_when_correct_password_entered(monkeypatch):
    password = main.password_hash('password')
    monkeypatch.setattr('builtins.input', lambda _: 'password')
    assert main.password_check(password) == 1


def test_returns_0_when_wrong_password_entered(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'password')
    assert main.password_check("wrongword") == 0


def test_returns_0_when_nothing_password_entered(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'password')
    assert main.password_check("") == 0


def test_add_money_within_limit(monkeypatch):
    money = 100.0
    limit = 200.0
    added_money = 50.0
    monkeypatch.setattr('builtins.input', lambda _: added_money)
    result = main.add_money(money, limit)
    assert result == money + added_money


def test_add_money_no_limit(monkeypatch):
    money = 100.0
    limit = 0
    added_money = 50.0
    monkeypatch.setattr('builtins.input', lambda _: added_money)
    result = main.add_money(money, limit)
    assert result == money + added_money


def test_return_correct_balance(monkeypatch):
    money = 100.0
    limit = 200.0
    added_money = 300.0
    monkeypatch.setattr('builtins.input', lambda _: added_money)
    result = main.add_money(money, limit)
    assert result == money


def test_return_correct_balance_without_adding_money(monkeypatch):
    money = 100.0
    limit = 200.0
    added_money = 0.0
    monkeypatch.setattr('builtins.input', lambda _: added_money)
    result = main.add_money(money, limit)
    assert result == money


def test_handle_non_float_input(monkeypatch):
    money = 100.0
    limit = 200.0
    added_money = "word"
    monkeypatch.setattr('builtins.input', lambda _: added_money)
    result = main.add_money(money, limit)
    assert result == money


def test_withdraw_less_than__money(monkeypatch):
    money = 1000
    withdraw_amount = 500
    monkeypatch.setattr('builtins.input', lambda _: withdraw_amount)
    result = main.money_withdraw(money)
    assert result == money - withdraw_amount


def test_withdraw_equal_to_money(monkeypatch):
    money = 1000
    withdraw_amount = 1000
    monkeypatch.setattr('builtins.input', lambda _: withdraw_amount)
    result = main.money_withdraw(money)
    assert result == money - withdraw_amount


def test_withdraw_more_than_money(monkeypatch):
    money = 1000
    withdraw_amount = 1500
    monkeypatch.setattr('builtins.input', lambda _: withdraw_amount)
    result = main.money_withdraw(money)
    assert result == money


def test_withdraw_str_input(monkeypatch):
    money = 1000
    withdraw_amount = "str"
    monkeypatch.setattr('builtins.input', lambda _: withdraw_amount)
    main.money_withdraw(money)
    assert money == money


def test_add_transaction_empty_dict(monkeypatch):
    transactions = {}
    monkeypatch.setattr('builtins.input', lambda _: 100.0)
    monkeypatch.setattr('builtins.input', lambda _: 'Test')
    new_transactions = main.add_transaction(transactions)
    assert new_transactions == transactions


def test_add_transaction_new_comment(monkeypatch):
    transactions = {'comment1': 100}
    monkeypatch.setattr('builtins.input', lambda _: 200)
    monkeypatch.setattr('builtins.input', lambda _: 'Test')
    new_transactions = main.add_transaction(transactions)
    assert new_transactions == transactions


def test_add_transaction_existing_comment(monkeypatch):
    transactions = {'comment1': 100}
    monkeypatch.setattr('builtins.input', lambda _: 200)
    monkeypatch.setattr('builtins.input', lambda _: 'comment1')
    new_transactions = main.add_transaction(transactions)
    assert new_transactions == transactions


def test_add_transaction_invalid_sum(monkeypatch):
    transactions = {'comment1': 100}
    monkeypatch.setattr('builtins.input', lambda _: 'test')
    monkeypatch.setattr('builtins.input', lambda _: 'comment1')
    new_transactions = main.add_transaction(transactions)
    assert new_transactions == transactions


def test_count_payments(capsys):
    trans = {'payment1': 100, 'payment2': 200, 'payment3': 100, 'payment4': 300, 'payment5': 200}
    expected_output = '100 руб.: 2 платеж(а)\n200 руб.: 2 платеж(а)\n300 руб.: 1 платеж(а)\n'
    main.trans_stats(trans)
    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_empty_dictionary():
    trans = {}
    result = main.trans_stats(trans)
    assert result is None


def est_limit_not_exceeded():
    transac = {'transaction1': 100, 'transaction2': 200, 'transaction3': 300}
    money = 500
    limit = 1500
    expected_transac = {}
    expected_money = 1100

    result_transac, result_money = main.apply_trans(transac, money, limit)

    assert result_transac == expected_transac
    assert result_money == expected_money


def test_limit_zero():
    transac = {'transaction1': 100, 'transaction2': 200, 'transaction3': 300}
    money = 500
    limit = 0
    expected_transac = {}
    expected_money = 1100

    result_transac, result_money = main.apply_trans(transac, money, limit)

    assert result_transac == expected_transac
    assert result_money == expected_money


def test_limit_greater_than_sum():
    transac = {'transaction1': 100, 'transaction2': 200, 'transaction3': 300}
    money = 500
    limit = 1000
    expected_transac = {'transaction3': 300}
    expected_money = 800

    result_transac, result_money = main.apply_trans(transac, money, limit)

    assert result_transac == expected_transac
    assert result_money == expected_money


def test_expected_combinations():
    iterable = [1, 2, 3]
    r = 2
    expected_result = [[1, 2], [1, 3], [2, 3]]
    result = list(main.all_transactions(iterable, r))

    assert result == expected_result


def test_expected_number_of_combinations():
    iterable = [1, 2, 3, 4]
    r = 2
    expected_result_length = 6

    result = list(main.all_transactions(iterable, r))

    assert len(result) == expected_result_length


def test_empty_list_when_r_greater_than_length():
    iterable = [1, 2, 3]
    r = 4

    result = list(main.all_transactions(iterable, r))

    assert result == []


def test_type_error_when_iterable_not_iterable():
    iterable = 123
    r = 2

    with pytest.raises(TypeError):
        list(main.all_transactions(iterable, r))


def setup_found_str_value(test_case, file=None):
    part, str_name, file_name, expected_value = test_case
    if file == "create":
        with open(f'{file_name + "_"}{part}.txt', "w") as f:
            f.write(f'{str_name}|{expected_value}\n')
            f.close()
    elif file == "delete":
        os.remove(f'C:/Users/joji/PycharmProjects/bankingApp/{file_name + "_"}John Doe.txt')
    else:
        pass
    actual_value = main.found_str_value(part, str_name, file_name)
    assert actual_value == expected_value


def test_found_str():
    test_case = (
        "John Doe",
        "Money",
        "user_info",
        100.00
    )

    setup_found_str_value(test_case, "create")


def test_non_existing_str():
    test_case = (
        "John Doe",
        "Non-Existent Str",
        "user_info",
        100.0
    )
    with pytest.raises(RuntimeError):
        setup_found_str_value(test_case)


def test_non_existing_user():
    test_case = (
        "Who is this",
        "Money",
        "user_info",
        100.0
    )
    with pytest.raises(RuntimeError):
        setup_found_str_value(test_case, "delete")


def test_overwrite_string_value():
    part = "test_part"
    str_name = "test_string"
    file_name = "test_file"
    new_value = "new_value"

    with open(f'{file_name + "_"}{part}.txt', "w") as f:
        f.write(f'{str_name}|old_value\n')
        f.close()

    main.overwrite_string_value(part, str_name, file_name, new_value)

    with open(f'{file_name}_{part}.txt', "r") as f:
        lines = f.read().split("\n")[:-1]
        f.close()

    os.remove(f'C:/Users/joji/PycharmProjects/bankingApp/{file_name + "_"}{part}.txt')

    assert lines[0].split("|")[1] == new_value


def test_overwrites_file_to_origin_if_nonexistent_string():
    part = "test_part"
    str_name = "nonexistent_string"
    file_name = "test_file"
    new_value = "new_value"

    with open(f'{file_name + "_"}{part}.txt', "w") as f:
        f.write(f'other_string|old_value\n')
        f.close()

    main.overwrite_string_value(part, str_name, file_name, new_value)

    with open(f'{file_name}_{part}.txt', "r") as f:
        lines = f.read().split("\n")[:-1]
        f.close()

    assert lines[0].split("|")[0] == 'other_string'
    assert lines[0].split("|")[1] == 'old_value'
