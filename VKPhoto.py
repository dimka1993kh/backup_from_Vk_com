import requests
from pprint import pprint

class VKPhoto():
    def __init__(self, photo_info):
        self.photo_info = photo_info
        self.likes = photo_info['likes']['count']
        self.sizes = photo_info['sizes']
        self.max_size = self.find_max_size()['max_size']
        self.max_size_url = self.find_max_size()['url']
        self.date = photo_info['date']

    
    def test(self):
        pprint(self.photo_info)

    def find_max_size(self):
        # сравним размер фото в альбоме с элементами types_of_photo_sizes, записанными по убыванию размера фото
        types_of_photo_sizes = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        for max_size in types_of_photo_sizes:
            for available_size in self.sizes:
                if available_size['type'] == max_size:
                    return {'max_size' : available_size['type'], 'url' : available_size['url']}



