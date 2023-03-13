import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

#получение API-ключа
    def get_api_key(self, email: str, password: str):

        headers = {
            'email': email,
            'password': password
        }

        response = requests.get(self.base_url+'/api/key', headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except :
            result = response.text

        return status, result

#Получение списка питомцев
    def get_list_of_pets(self, auth_key: json, filter: str = ""):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# Добавление питомца
    def add_new_pet(self, auth_key:json, name:str, animal_type:str, age:int, pet_photo:str):

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )

        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }

        response = requests.post(self.base_url + '/api/pets', data=data, headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except :
            result = response.text
        print(result)
        return status, result

#удаление питомца
    def delete_pet(self, auth_key: json, pet_id: str):
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#изменение информации о питомце
    def update_pet_info(self, auth_key, pet_id, name,animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except :
            result = res.text
        print(result)
        return status, result

#добавление питомца без фото
    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        """
        Этот метод позволяет добавить информацию о новом питомце без фото
        :return:
        """
        headers = {'auth_key': auth_key['key']}
        formData = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = requests.post(f'{self.base_url}/api/create_pet_simple', headers=headers, data=formData)
        status = response.status_code
        try:
            result = response.json()
        except BaseException:
            result = response.text

        return status, result

# Добавление фото питомца
    def add_pet_photo(self, auth_key, pet_id, pet_photo):
      data = MultipartEncoder(
          fields={
                     'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
      headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

      res = requests.post(f'{self.base_url}/api/pets/set_photo/{pet_id}', data=data, headers=headers)
      status = res.status_code
      try:
        result = res.json()
      except:
        result = res.text
      print(result)
      return status, result
