import requests
from requests.exceptions import HTTPError
from settings import user_token, V

class Handler:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = user_token
        self.version = V
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_user_info(self, user_id):
        user_info_url = self.url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'city',
            'name_case': 'nom'
        }
        response = requests.get(user_info_url, params={**self.params, **user_params}).json()
        for url in [user_info_url]:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP-ошибка: {http_err}')
            except Exception as err:
                print(f'Другая ошибка: {err}')
            else:
                print('Успешное соединение')
        print(response)
        return response

    def users_search(self, get_user_info, sex, status, age_from, age_to, city_id):
        for _ in get_user_info['response']:
            users_search_url = self.url + 'users.search'
            user_params = {
                'count': 20,
                'sort': 0,
                'has_photo': 1,
                'is_closed': 0,
                'sex': sex,
                'status': status,
                'age_from': age_from,
                'age_to': age_to,
                'city': city_id
            }
            response = requests.get(users_search_url, params={**self.params, **user_params}).json()
            for url in [users_search_url]:
                try:
                    resp = requests.get(url)
                    resp.raise_for_status()
                except HTTPError as http_err:
                    print(f'HTTP-ошибка: {http_err}')
                except Exception as err:
                    print(f'Другая ошибка: {err}')
                else:
                    print('Успешное соединение')
            persone_id_list = [item.get('id') for item in response['response']['items']]
            return persone_id_list

    def get_photos(self, persone_id):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': persone_id,
            'album_id': 'profile',
            'extended': '1',
            'can_comment': '0',
            'count': '20',
            'photo_sizes': '1'
        }
        try:
            response = requests.get(photos_url, params={**self.params, **photos_params}).json()
            photo_list = []
            best_photo_list = []
            for value in response.values():
                items = value.get('items')
                print(items)
                for item in items:
                    like_id_list = []
                    likes = item.get('likes')
                    like = likes.get('count')
                    like_id_list.append(like)
                    comment_id_list = []
                    comments = item.get('comments')
                    comment = comments.get('count')
                    comment_id_list.append(comment)
                    photo_id = item.get('id')
                    like_id_list.append(photo_id)
                    comment_id_list.append(photo_id)
                    photo_list.append(like_id_list)
                    photo_list.append(comment_id_list)
            photo_list.sort()
            print(photo_list)
            if len(photo_list) >= 3:
                best_photo_list.append(photo_list[-1])
                best_photo_list.append(photo_list[-2])
                best_photo_list.append(photo_list[-3])
            elif len(photo_list) == 2:
                best_photo_list.append(photo_list[-1])
                best_photo_list.append(photo_list[-2])
            else:
                best_photo_list.append(photo_list[-1])
            print(best_photo_list)
        except TypeError:
            print('ошибка TypeError в модуле get_photos')
            pass
        else:
            return best_photo_list

    def messages_send(self, get_photos, persone_id):
        global attachments
        try:
            if len(get_photos) == 3:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                photo2 = f'photo{persone_id}_{get_photos[1][1]}'
                photo3 = f'photo{persone_id}_{get_photos[2][1]}'
                attachments = [photo1, photo2, photo3]
            elif len(get_photos) == 2:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                photo2 = f'photo{persone_id}_{get_photos[1][1]}'
                attachments = [photo1, photo2]
            elif len(get_photos) == 1:
                photo1 = f'photo{persone_id}_{get_photos[0][1]}'
                attachments = [photo1]
        except TypeError:
            print ('ошибка TypeError в модуле messages_send')
            pass
        else:
            return attachments
