from VKUser import *
from CurrentAlbum import *
from YaDisk import *
import os
import datetime


def create_new_folder(title, VKUser):
    access_rights = 0o755
    folder_name = f'Альбом _{title}_ пользователя VK _{VKUser.first_name} {VKUser.last_name}_'
    path = os.path.join(folder_name)
    # проверим наличие данной папки на ПК
    if not os.path.exists(folder_name):
        os.mkdir(folder_name, access_rights)
        print(f'Создана новая папка "{path}".')
    else:
        print(f'Папка "{path}" уже существует.')
        print('Загрузка фотографий будет осуществлена в данную папку.')
    return path    


def number_load_photo(person_input):
    if person_input == '':
        return 5
    elif person_input.isdigit():
        return int(person_input)
    else:
        raise Exception('Ошибка ввода количества фотографий. Нужно ввести число')

def condition(person_input):
    if person_input == '0':
        return False
    elif person_input == '1':
        return True
    else:
        raise Exception('Ошибка при вводе. Нужно ввести 0 или 1.')


# создадим пользователя
# выведем необходимые строки в консоль для понимания
# также попросим пользователя ввести необходимые данные для работы программы
user = VKUser(f"{ input('Введите id пользователя VK.com: ') }")
print('Введите интересующий Вас альбом из предложенных: ')
for number_album in range(1, user.number_albums + 1):
    print(f"{number_album} - {user.info_for_albums[number_album - 1]['title']} - {user.info_for_albums[number_album - 1]['size']} фотографий")
current_album_number = int(input()) - 1
print(f'Будет выполнена загрузка из альбома "{user.info_for_albums[current_album_number]["title"]}". В данном альбоме {user.info_for_albums[current_album_number]["size"]} фотографий. Сколько хотите загрузить (по-умолчанию - 5)?')
number_load_photo = number_load_photo(input())

current_album = CurrentAlbum(user, current_album_number)
print('Скачать данные фотографии на ПК?')
print('0 - Нет')
print('1 - Да')
download_condition_on_PC = condition(input())


print('Загрузить данные фотографии на Яндекс.Диск?')
print('0 - Нет')
print('1 - Да')
download_condition_on_YaDisk = condition(input())


folder_name = f'Альбом _{user.info_for_albums[current_album_number]["title"]}_ пользователя VK _{user.first_name} {user.last_name}_'

if download_condition_on_PC:
    path = create_new_folder(user.info_for_albums[current_album_number]["title"], user)
    current_album.load_photos(path, number_load_photo)
    print('Фотографии были загружены на ПК')
else:
    print('Фотографии НЕ загружены на ПК')
if download_condition_on_YaDisk:
    yadisk = YaUploader(input('Введите токен с Полигона Яндекс.Диска: '))
    result = yadisk.upload_from_URL(current_album, folder_name, number_load_photo)
    print('Фотографии были загружены на Яндекс.Диск')
else:
    print('Фотографии НЕ загружены на Яндекс.Диск')

print('Завершение работы программы')

pprint(result)




    
    


