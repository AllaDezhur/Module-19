from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()
#1 Положительный сценарий - получение API-ключа
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')


#2 Положительный сценарий - получение списка всех питомцев
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#3 Положительный сценарий - добавление нового питомца
def test_add_new_pet_with_valid_data(name='Пушистик', animal_type='кот',
                                     age='1', pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['id'] != ''

#4 Отрицательный сценарий - добавление нового питомца с отрицательным возрастом БАГ
def test_add_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, 'Пушистик', 'кот', '-1', 'images/cat.jpg')
    assert status == 200
    assert result['name'] == 'Пушистик'
    assert result['id'] != ''

#5 Отрицательный сценарий - добавление нового питомца с очень большим значением возрата БАГ
def test_add_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, 'Пушистик', 'кот', '2000', 'images/cat.jpg')
    assert status == 200
    assert result['name'] == 'Пушистик'
    assert result['id'] != ''

#6 Отрицательный сценарий - добавление нового питомца с отсутствующим именем  БАГ
def test_add_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, ' ', 'кот', '2000', 'images/cat.jpg')
    assert status == 200
    assert result['name'] == ' '
    assert result['id'] != ''

#7 Отрицательный сценарий - добавление нового питомца с отсутствующим видом  БАГ
def test_add_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, 'Пушистик ', ' ', '2000', 'images/cat.jpg')
    assert status == 200
    assert result['name'] == 'Пушистик '
    assert result['id'] != ''

#8 Положительный сценарий - удаление питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Злюка", "собака", "3", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

#9 Положительный сценарий - изменение данных питомца
def test_successful_update_self_pet_info (name='Царапка', animal_type='камышовый кот', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        print(result)
    else:
        raise Exception("У меня нет питомцев")

#10 Положительный сценарий - добавление нового питомца без фото
def test_add_new_pet_without_photo(name = "Толстяк",animal_type="такса",age =5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    print(result)

#11 Положительный сценарий - добавление фото
def test_add_pet_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')

    if len(result['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, result['pets'][0]['id'], 'images/dog.jpeg')
    else:
        _, result = pf.add_new_pet(auth_key, 'Murder', 'killer', 10, 'images/dog2.jpg')
        status, result = pf.add_pet_photo(auth_key, result['pets'][0]['id'], 'images/dog.jpeg')
    assert status == 200
    assert result['id']

#12 Отрицательный сценарий - получение API-ключа с неправильным паролем
def test_get_api_key_for_valid_user(email=valid_email, password=unvalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')

#13 Отрицательный сценарий - получение API-ключа с неправильным e-mail
def test_get_api_key_for_valid_user(email=unvalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')

#14 Отрицательный сценарий - получение API-ключа с неправильным e-mail и паролем


def test_get_api_key_for_valid_user(email=unvalid_email, password=unvalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')



