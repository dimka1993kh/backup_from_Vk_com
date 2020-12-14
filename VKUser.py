import requests
from pprint import pprint
from VKAlbum import *
import time
from progress.bar import IncrementalBar

class VKUser():
    def __init__(self, user_id=None):
        if user_id == '':
            params = {
                'access_token' : access_token,
                'v' : '5.126'
            }
        else:
            params = {
                'user_ids' : user_id,
                'access_token' : access_token,
                'v' : '5.126'
            }


        self.user_info = requests.get(api_url + 'users.get', params=params)
        self.user_info.raise_for_status()
        self.user_id =  self.user_info.json()['response'][0]['id']

        params_for_albums = {
            **params, 
            'need_system' : '1',
            'owner_id' : self.user_id
        }
        # pprint(self.user_info.json())
        self.first_name = self.user_info.json()['response'][0]['first_name']
        self.last_name = self.user_info.json()['response'][0]['last_name']

        print(f'Пользователь: {self.first_name} {self.last_name}.')
        self.info_for_albums = self.find_info_for_albums(params_for_albums)
        self.number_albums = len(self.info_for_albums)

        print(f'У пользователя {self.number_albums} альбомов.')
        print()

        self.albums = self.create_VKAlbums(params_for_albums)

    def create_VKAlbums(self, params_to_request):
        result = []
        bar = IncrementalBar('Загрузка информции об альбомах.', max = self.number_albums) # КАК ОРГАНИЗОВАТЬ PB КАК ОТДЕЛЬНУЮ ФУНКЦИЮ????
        for info in self.info_for_albums:
            result.append(VKAlbum(info))
            bar.next()
        bar.finish()
        print('Загрузка информации об альбомах завершена.')
        return result
    
    def find_info_for_albums(self, params_to_request):
        result = []
        data = requests.get(api_url + 'photos.getAlbums', params=params_to_request)
        data.raise_for_status()
        for i in data.json()['response']['items']:
            info = {'id' : i['id'], 'size' : i['size'], 'owner_id' : i['owner_id'], 'title' : i['title']}  
            result.append(info)
        return result
    




            
      



# Можно добавить интрактив с пользователем: 
# 1. Введите id пользователя
# 2. Введите интересующий альбом из предложенных (вывести сообщение о том, сколько фотографий в альбоме и спросить, сколько фото хоитие "архивировать"? По-умолчанию 5)

# Можно во время загрузки программы сделать прогресс бар в консоли. Добавить сам прогресс бар и надпись "идет загрузка. Получена информация об N из K альбомах"