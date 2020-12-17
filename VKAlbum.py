import requests
from pprint import pprint
from VKPhoto import *
import time



api_url = 'https://api.vk.com/method/'
access_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

class VKAlbum():
    def __init__(self, album_info):
        self.album_id = album_info['id']    
        self.size = album_info['size']
        self.owner_id = album_info['owner_id']
        self.title = album_info['title']

        params_for_photo = {
            'access_token' : access_token,
            'v' : '5.126',
            'extended' : '1',
            'count' : '1000', 
            'owner_id' : album_info['owner_id'],
            'no_service_albums': '0',
            'photo_sizes' : '1',
                }
        self.photos_in_album = [VKPhoto(info) for info in self.find_photos_in_album(params_for_photo)]
        self.number_photos = len(self.photos_in_album)

    def find_photos_in_album(self, params_to_request):
        result = []
        time.sleep(0.35)
        data = ''
        # Альбом "фотографии с пользователем" с id -9000 не удается обработать стандартным способом. Используем необходимый метод, согласно документации VK API
        if self.album_id != -9000:
            data = requests.get(api_url + 'photos.get', params={**params_to_request, **{'album_id' : self.album_id}})
            data.raise_for_status()
        elif self.album_id == 'profile':
            data = requests.get(api_url + 'photos.get', params={**params_to_request, **{'album_id' : self.album_id}})
            data.raise_for_status()
        elif self.album_id == 'wall':
            data = requests.get(api_url + 'photos.get', params={**params_to_request, **{'album_id' : self.album_id}})
            data.raise_for_status()
        else:
            data = requests.get(api_url + 'photos.getUserPhotos', params={**params_to_request, **{'user_id' : self.owner_id}})
            data.raise_for_status()
        for i in data.json()['response']['items']:
            result.append(i)
        return result
