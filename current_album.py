import os
import requests
import datetime
from pprint import pprint

class Current_album():
    def __init__(self, VKUser, number_current_album):
        self.VKUser = VKUser
        self.number_current_album = number_current_album
        self.current_album_object = self.VKUser.albums[self.number_current_album]
        self.photos_in_current_album = self.current_album_object.photos_in_album
        self.urls_photos = [photo.max_size_url for photo in self.photos_in_current_album]

    def create_new_folder(self):
        access_rights = 0o755
        folder_name = f'Альбом {self.current_album_object.title} пользователя VK {self.VKUser.first_name} {self.VKUser.last_name}'
        path = os.path.join(folder_name)
        # проверим наличие данной папки на ПК
        if not os.path.exists(folder_name):
            os.mkdir(folder_name, access_rights)
            print(f'Создана новая папка "{path}".')
        else:
            print(f'Папка "{path}" уже существует.')
        print('Загрузка фотографий будет осуществлена в данную папку.')
        return path
    
    def load_photos(self, path, number_photos):
        for index, url in enumerate(self.urls_photos):
            if index < number_photos:
                resp_photo = requests.get(url)
                resp_photo.raise_for_status()
                # Запишем 2 разных пути сохранения фото. В первом случае станадртное название, во втором - при название изменится, если такое название уже есть (правда 1 раз. если попадется еще одна такая же фотка, что результат перезапишется)
                path_to_save = os.path.join(path, str(self.photos_in_current_album[index].likes) + ' лайков' + '.jpg')
                alternative_path_to_save = os.path.join(path, str(self.translation_from_unixtime(self.photos_in_current_album[index].date))[:10] + ' ' + str(self.photos_in_current_album[index].likes) + ' лайков.jpg')
                if not os.path.exists(path_to_save):
                    with open(os.path.join(path_to_save), 'wb') as f:
                        f.write(resp_photo.content)
                else:
                    with open(os.path.join(alternative_path_to_save), 'wb') as f:
                        f.write(resp_photo.content)
# метод перевода unixtime в 'человеческий' вид
    def translation_from_unixtime(self, date_unix):
        return datetime.datetime.fromtimestamp(date_unix).strftime('%Y-%m-%d %H:%M:%S')

        

