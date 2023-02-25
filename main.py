import sys
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from api import Handler
from database import Session, DB_User
from settings import bot_token, V
from vk_api.exceptions import ApiError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from modules import write_msg,send_photo

vk = vk_api.VkApi(token=bot_token)
longpoll = VkLongPoll(vk)

if __name__ == '__main__':


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            if request == 'бот':
                write_msg(event.user_id, 'Привет! Начнём поиск?')
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        request = event.text.lower()

                        if request == 'нет':
                            write_msg(event.user_id, 'Если буду нужен, вызови меня, напиши "бот"')
                            break
                        elif request != 'нет' and request != 'да':
                            write_msg(event.user_id, 'Нужно написать "да" или "нет"')
                        elif request == 'да':
                            write_msg(event.user_id,
                                      'Кого ищем?:\n1 - женщину;\n2 - мужчину')
                        while True:
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text.lower()

                                    try:
                                        sex = int(request)
                                        if  int (request) == 1 or str(request)== 2:
                                            pass
                                        else:
                                            write_msg(event.user_id, 'Нужно ввести 1, если ищем женщину, а если мужчину, то 2')
                                    except ValueError:
                                        write_msg(event.user_id,'Нужно ввести цифру 1, если ищем женщину, а если мужчину, то цифру 2')
                                        print('ошибка ввода цифры')
                                        break
                                    else:
                                        write_msg(event.user_id,
                                            'Выбери семейное положение кандидата:\n1 - не женат(не замужем);'
                                            '\n2 - встречается;\n3 - помолвлен(-а); \n4 - женат (замужем); \n5 - всё сложно;'
                                            '\n6 - в активном поиске; \n7 - влюблен(-а); \n8 - в гражданском браке.'
                                            )
                                        while True:
                                            for event in longpoll.listen():
                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                    request = event.text.lower()

                                                    try:
                                                        status = int(request)
                                                        if 0 < int(request) < 9:
                                                            pass
                                                        else:
                                                            write_msg(event.user_id, 'Введена неправильная цифра, надо выбрать от 1 до 8')
                                                            break
                                                    except ValueError:
                                                        write_msg(event.user_id,'Неправильный ввод, надо  выбрать ЦИФРУ от 1 до 8')
                                                        print('ошибка ввода цифры')
                                                        break
                                                    else:
                                                        write_msg(event.user_id, 'Укажите минимально возможный возраст для поиска')

                                                    while True:
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                request = event.text.lower()

                                                                try:
                                                                    age_from = int(request)
                                                                    if int(request) > 17:
                                                                        pass
                                                                    else:
                                                                        write_msg(event.user_id, 'Действует ограничение "не моложе 18 лет", введите другое значение возраста')
                                                                        break
                                                                except ValueError:
                                                                    write_msg(event.user_id,'Неправильный ввод, надо  выбрать ЦИФРУ от 18 и больше')
                                                                    print('ошибка ввода цифры')
                                                                    break
                                                                else:
                                                                    write_msg(event.user_id,
                                                                                'Укажите максимально возможный возраст для поиска')
                                                                while True:
                                                                    for event in longpoll.listen():
                                                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                            request = event.text.lower()
                                                                            try:
                                                                                age_to = int(request)
                                                                                if int(request) > age_from:
                                                                                    pass
                                                                                else:
                                                                                    write_msg(event.user_id,
                                                                                          'Значение верхней границы возраста должно быть больше выбранной нижней границы')
                                                                                    break
                                                                            except ValueError:
                                                                                write_msg(event.user_id,
                                                                                          'Неправильный ввод, надо  выбрать ЦИФРУ от 18 и больше')
                                                                                print('ошибка ввода цифры')
                                                                                break

                                                                            else:
                                                                                write_msg(event.user_id,
                                                                                          'Выберите город поиска, введите цифру: 1 - Москва, 2 - Cанкт-Петербург или другие цифры')
                                                                                while True:
                                                                                    for event in longpoll.listen():
                                                                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                                            request = event.text.lower()
                                                                                            try:
                                                                                                city_id = int(request)
                                                                                                if int(request) == 1:
                                                                                                    write_msg(event.user_id,'Вы выбрали Москву')
                                                                                                    pass
                                                                                                elif int(request) == 2:
                                                                                                    write_msg(event.user_id,'Вы выбрали Санкт-Петербург')
                                                                                                    pass
                                                                                                else:
                                                                                                    write_msg(event.user_id,'В данной версии программы предусмотрен выбор только двух городов')
                                                                                                    break
                                                                                            except ValueError:
                                                                                                write_msg(event.user_id,'Неправильный ввод, надо  выбрать ЦИФРУ')
                                                                                                print('ошибка ввода цифры')
                                                                                                break

                                                                                            else:
                                                                                                write_msg(event.user_id, 'Результаты поиска')
                                                                                                vk_client = Handler(bot_token, V)
                                                                                                get_user_info = vk_client.get_user_info(event.user_id)
                                                                                                users_search = vk_client.users_search(get_user_info, sex, status, age_from, age_to, city_id)

                                                                                                persones_list = []
                                                                                                while True:
                                                                                                    for persone_id in users_search:
                                                                                                        try:
                                                                                                            get_photos = vk_client.get_photos(persone_id)
                                                                                                            get_attachments = vk_client.messages_send(get_photos, persone_id)
                                                                                                            send_photo(event.user_id,f'Персона vk.com/id{persone_id}',get_attachments)
                                                                                                        except ApiError:
                                                                                                            print('Hет доступа к фото')
                                                                                                        persones_data = DB_User(name=f'vk.com/id{persone_id}')
                                                                                                        with Session() as session:
                                                                                                            try:
                                                                                                                session.add(persones_data)
                                                                                                                session.commit()
                                                                                                            except (IntegrityError, UniqueViolation):
                                                                                                                print('попытка дублирующей записи')
                                                                                                                write_msg(event.user_id,
                                                                                                                          'Пошли по второму кругу. Продолжить?')
                                                                                                                session.rollback()
                                                                                                            else:
                                                                                                                add_result = session.query(DB_User).all()

                                                                                                        for item in add_result:
                                                                                                            name = item.name
                                                                                                            persones_list.append(name)
                                                                                                        write_msg(event.user_id,'Продолжаем искать?')
                                                                                                        for event in longpoll.listen():
                                                                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                                                                request = event.text.lower()
                                                                                                                if request == 'да':
                                                                                                                    break
                                                                                                                else:
                                                                                                                    write_msg(
                                                                                                                        event.user_id,
                                                                                                                        f'Поиск закончен. '
                                                                                                                        f'Вот список найденных кандидатов.:{persones_list}'
                                                                                                                        f'\n Продолжить!'
                                                                                                                    )

                                                                                                                    for event in longpoll.listen():
                                                                                                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                                                                            request = event.text.lower()
                                                                                                                            if request != 'да':
                                                                                                                                write_msg(
                                                                                                                                    event.user_id, f'До свидания!')
                                                                                                                                session.close()
                                                                                                                                sys.exit()
                                                                                                                            else:
                                                                                                                                write_msg(
                                                                                                                                event.user_id,f'Продолжаем поиск по тем же критериям?')
                                                                                                                                break



