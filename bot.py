import json
import os

import vk_api
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll

from db import *


class Bot:
    """
    Класс бота ВКонтакте
    """

    def __init__(self):
        """
        Инициализация бота при помощи получения доступа к API ВКонтакте
        """
        load_dotenv()
        self.VK_TOKEN = os.getenv('VK_TOKEN')
        self.vk_session = vk_api.VkApi(token=self.VK_TOKEN)
        self.session_api = self.vk_session.get_api()
        self.longpool = VkLongPoll(self.vk_session)

    def sender(self, user_id: str, text: str = None, attachment: str = None, keyboard: str = None,
               sticker: int = None, carousel_template: str = None) -> None:
        """
        Функция для отправки сообщений ботом
        :param user_id: id пользователя, который ведет диалог с ботом
        :param text: текст сообщения от бота
        :param attachment: файл, прикрепленный к сообщению бота
        :param keyboard: клавиатура
        :param sticker: id стикера
        :param carousel_template: строка с товарами
        :return: None
        """
        self.session_api.messages.send(
            user_id=user_id,
            message=text,
            random_id=0,
            attachment=attachment,
            sticker_id=sticker,
            template=carousel_template,
            keyboard=keyboard
        )

    def offers_data(self, offers_request: str) -> str:
        """
        Получение данных для передачи в carousel
        :param offers_request:
        :return: строка с товарами
        """
        offers = sql_request_data(offers_request)
        with open("carousel.json", "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            for elem in range(len(offers)):
                data['elements'][elem]['photo_id'] = offers[elem][2]
                data['elements'][elem]['buttons'][0]['action']['label'] = offers[elem][1]
            carousel = json.dumps(data, ensure_ascii=False).encode('utf-8')
            carousel = str(carousel.decode('utf-8'))
            return carousel

    def send_message(self) -> None:
        """
        Отправка сообщений
        """
        for event in self.longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = event.text.lower()
                    user_id = event.user_id

                    if msg == 'старт':
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, sticker=1)
                        self.sender(user_id=user_id, text='Добро пожаловать! Выберите действие',
                                    keyboard=keyboard.get_keyboard())

                    elif msg == 'главное меню':
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Торт", VkKeyboardColor.PRIMARY)
                        keyboard.add_button("Хлеб", VkKeyboardColor.PRIMARY)
                        keyboard.add_line()
                        keyboard.add_button("Пирожок", VkKeyboardColor.PRIMARY)
                        keyboard.add_button("Пицца", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Здравствуйте! Выберете интересующий вас товар!',
                                    keyboard=keyboard.get_keyboard())

                    elif msg == "хлеб":
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Каталог товаров в категории: Хлеб',
                                    carousel_template=self.offers_data(request_bread))
                        self.sender(user_id=user_id, text='Выберите товар, либо перейдите в главное меню',
                                    keyboard=keyboard.get_keyboard())

                    elif msg == "пирожки" or msg == "пирожок":
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Каталог товаров в категории: Пирожок',
                                    carousel_template=self.offers_data(request_pie))
                        self.sender(user_id=user_id, text='Выберите товар, либо перейдите в главное меню',
                                    keyboard=keyboard.get_keyboard())

                    elif msg == "торты" or msg == "торт":
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Каталог товаров в категории: Торт',
                                    carousel_template=self.offers_data(request_cake))
                        self.sender(user_id=user_id, text='Выберите товар, либо перейдите в главное меню',
                                    keyboard=keyboard.get_keyboard())

                    elif msg == "пиццы" or msg == "пицца":
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Каталог товаров в категории: Пицца',
                                    carousel_template=self.offers_data(request_pizza))
                        self.sender(user_id=user_id, text='Выберите товар, либо перейдите в главное меню',
                                    keyboard=keyboard.get_keyboard())

                    elif msg:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY)
                        self.sender(user_id=user_id, text='Текст не распознан, выберите одно из следующих действий',
                                    keyboard=keyboard.get_keyboard())
