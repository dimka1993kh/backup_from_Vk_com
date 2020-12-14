import requests
from pprint import pprint
import os
from progress.bar import IncrementalBar
import time
import datetime

class YaUploader:
    def __init__(self, token: str):
        self.token = token  

    def upload_from_URL(self, current_album, path_folder, number_photos):
        result = []
        self.create_folder(path_folder)
        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        
        names_files = {}
        for index, url in enumerate(current_album.urls_photos):
            if index < number_photos:
                # Запишем 2 разных пути сохранения фото. В первом случае станадртное название, во втором - при название изменится, если такое название уже есть (правда 1 раз. если попадется еще одна такая же фотка, что результат перезапишется)
                path_to_save = str(current_album.photos_in_current_album[index].likes) + ' лайков' + '.jpg'
                alternative_path_to_save = str(current_album.translation_from_unixtime(current_album.photos_in_current_album[index].date))[:10] + ' ' + str(current_album.photos_in_current_album[index].likes) + ' лайков.jpg'
                if path_to_save in names_files:
                    names_files.update({alternative_path_to_save: url})
                    result.append({'file_name' : alternative_path_to_save, 'size' : current_album.photos_in_current_album[index].max_size})
                else:
                    names_files.update({path_to_save: url})
                    result.append({'file_name' : path_to_save, 'size' : current_album.photos_in_current_album[index].max_size})
        # Выполним запрос на загрузку фотографии на Яндекс.Диск по URL фотографий
        headers = {'Authorization' : self.token}
        bar = IncrementalBar('Загрузка фотографий на Яндекс.Диск:', max = len(names_files)) 
        for name_file in names_files.items():
            params = {'url': name_file[1], 'path' :path_folder + '/' + name_file[0], 'overwrite' : 'True'}
            resp = requests.post(URL, params=params, headers=headers)
            # Проверка на успешность запроса
            resp.raise_for_status()
            bar.next()
        bar.finish()
        return result

    def upload_from_PC(self, path_folder):
        """Метод загруджает файл file_path на яндекс диск"""
        self.create_folder(path_folder)
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        names_files = os.listdir(path=path_folder)
        # Выполним запрос, в котором получим ссылку на загрузку нашего файла
        headers = {'Authorization' : self.token}
        bar = IncrementalBar('Загрузка фотографий на Яндекс.Диск:', max = len(names_files)) 
        for name_file in names_files:
            params = {'path' :path_folder + '/' + name_file, 'overwrite' : 'True'}
            resp = requests.get(url, params=params, headers=headers)
            # Проверка на успешность запроса
            resp.raise_for_status()
            # Получили ссылку для загрузки файла
            href = resp.json()['href']
            # Прочитаем файл на компьютере и отправим файл на диск
            with open(os.path.join(path_folder, name_file), 'rb') as f:
                resp = requests.put(href, files={"file": f})
                resp.raise_for_status()
                bar.next()
        bar.finish()

    def create_folder(self, YaDisk_folder):
        params = {'path' : YaDisk_folder, 'overwrite' : 'True'}
        headers = {'Authorization' : self.token}
        resp = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        resp.raise_for_status()
        return YaDisk_folder


