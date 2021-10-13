from time import time

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config


def send_message(chat_id, text, keyboard=None, random_gen=time, **kwargs):
    if keyboard:
        keyboard = keyboard.get_keyboard()

    api.messages.send(
        chat_id=chat_id,
        message=text,
        keyboard=keyboard,
        random_id=int(random_gen()),
        **kwargs,
    )


def menu_command_handler(api, event: Event):
    send_message(event.chat_id, 'Hello')


def event_handler(event: Event):
    for text, message_handler in message_handlers.items():
        if text == event.text:
            message_handler(api, event)
            break

    if event.text == "Начать":
        keyboard = VkKeyboard()
        keyboard.add_button('< 18', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('18 - 20', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('> 21', color=VkKeyboardColor.PRIMARY)
        send_message(event.chat_id, 'S', keyboard)


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_chat:
                event_handler(event)


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=config.TOKEN)
    longpoll = VkLongPoll(vk_session)
    api = vk_session.get_api()

    message_handlers = {
        '/menu': menu_command_handler,
    }
    main()
