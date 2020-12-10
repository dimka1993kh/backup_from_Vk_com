import requests
from pprint import pprint

api_url = 'https://api.vk.com/method/'



class VKUser():
    def __init__(self, user_id=None):
        self.user_id = user_id

        params = {
            'access_token' : '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v' : '5.126'
        }
        params_for_photo = {
           **params,
            'extended' : '1',
            'count' : '1000', 
            'album_id' : 'profile',
            'owner_id' : self.user_id
        }
        params_for_albums = {
            **params, 
            'need_system' : '1',
            'owner_id' : self.user_id
        }
        self.user_info = requests.get(api_url + 'users.get', params=params)
        self.user_info.raise_for_status()
        self.user_photo = requests.get(api_url + 'photos.get', params=params_for_photo)   
        self.user_photo.raise_for_status()
        self.user_albums = requests.get(api_url + 'photos.getAlbums', params=params_for_albums)
        self.user_albums.raise_for_status()

        let_list = []
        for i in self.user_albums.json()['response']['items']:
            let_list.append({'id' : i['id']})
        self.dict_user_albums = {key : value for key, value in zip(list(range(1, self.user_albums.json()['response']['count'] + 1)), let_list)}
        self.current_album = input(f'Введите номер альбома {[(x , y["title"]) for x, y in zip(self.dict_user_albums.keys(), self.user_albums.json()["response"]["items"])]}: ')

        # Далее будем ссылаться на нужный альбом и брать от туда фотки
p1 = VKUser('24415708')
# pprint(p1.user_photo.json())
# print(p1.user_albums.json()['response']['count'])
pprint(p1.dict_user_albums)
print(p1.current_album)
# pprint(p1.user_albums.json()['response']['items'])
# print()