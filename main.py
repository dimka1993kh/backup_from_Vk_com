from VKUser import *
from current_album import *
import os
import datetime


user_1 = VKUser(f"{ input('Введите id пользователя VK.com: ') }")
print('Введите интересующий Вас альбом из предложенных: ')
for number_album in range(1, user_1.number_albums + 1):
    print(f"{number_album} - {user_1.info_for_albums[number_album - 1]['title']} - {user_1.info_for_albums[number_album - 1]['size']} фотографий")
current_album = int(input()) - 1
print(f'Будет выполнена загрузка из альбома "{user_1.info_for_albums[current_album]["title"]}". В данном альбоме {user_1.albums[current_album].number_photos} фотографий. Сколько хотите загрузить (по-умолчанию - 5)?')
number_load_photo = int(input())

current_album_1 = Current_album(user_1, current_album)
path = current_album_1.create_new_folder()
current_album_1.load_photos(path, number_load_photo)

    


