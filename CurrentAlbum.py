import os
import requests
import datetime
from pprint import pprint
from progress.bar import IncrementalBar
import time

class CurrentAlbum():
    def __init__(self, VKUser, number_current_album):
        self.VKUser = VKUser
        self.number_current_album = number_current_album
        self.current_album_object = self.VKUser.albums[self.number_current_album]
        self.photos_in_current_album = self.current_album_object.photos_in_album
        self.urls_photos = [photo.max_size_url for photo in self.photos_in_current_album]
    
    def load_photos(self, path, number_photos):
        bar = IncrementalBar('Загрузка фотографий:', max = number_photos)
        date = datetime.datetime.now()
        for index, url in enumerate(self.urls_photos):
            if index < number_photos:
                if int((datetime.datetime.now() - date).microseconds) > 350000:
                    time.sleep(0.35)
                resp_photo = requests.get(url)
                resp_photo.raise_for_status()
                # Запишем 2 разных пути сохранения фото. В первом случае станадртное название, во втором - при название изменится, если такое название уже есть (правда 1 раз. если попадется еще одна такая же фотка, что результат перезапишется)
                path_to_save = os.path.join(path, str(self.photos_in_current_album[index].likes) + ' лайков' + '.jpg')
                alternative_path_to_save = os.path.join(path, str(self.translation_from_unixtime(self.photos_in_current_album[index].date))[:10] + ' ' + str(self.photos_in_current_album[index].likes) + ' лайков.jpg')
                if not os.path.exists(path_to_save):
                    with open(os.path.join(path_to_save), 'wb') as f:
                        f.write(resp_photo.content)
                        bar.next()
                else:
                    with open(os.path.join(alternative_path_to_save), 'wb') as f:
                        f.write(resp_photo.content)
                        bar.next()
                date = datetime.datetime.now()
        bar.finish()
# метод перевода unixtime в 'человеческий' вид
    def translation_from_unixtime(self, date_unix):
        return datetime.datetime.fromtimestamp(date_unix).strftime('%Y-%m-%d %H:%M:%S')


        

