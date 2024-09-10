import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name

    return current_body

# Тест 1. Успешное создание пользователя

# Функция для позитивной проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
             + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Функция для негативной проверки
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)

    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"
# Тест 3
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Тест 4
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

# Тест 5
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

# Тест 8
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Функция для негативной проверки
    # В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400

    assert response.json()["code"] == 400

    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 10
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")

    negative_assert_no_first_name(user_body)

# Тест 11
def test_create_user_empty_first_name_get_error_response():
       user_body = get_user_body("")
       negative_assert_no_first_name(user_body)

# Тест 12
def test_create_user_number_type_first_name_get_error_response():
       user_body = get_user_body(12)
       response = sender_stand_request.post_new_user(user_body)
       assert response.json()["code"] == 400