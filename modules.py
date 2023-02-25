import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import bot_token
from random import randrange

vk = vk_api.VkApi(token=bot_token)
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

def send_photo(user_id, message, attachments):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': ','.join(attachments),
                                    'random_id': randrange(10 ** 7), })
    except TypeError:
        for event in longpoll.listen():
                      write_msg(event.user_id,'К сожалению, не могу показать фото.')
                      break
        print('ошибка TypeError в модуле send_photo')
        pass
    else:
        return

