from time import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from django.utils import timezone

import config
from states import States

from backend.models import BotUser, CashLink, TaskManager
from backend.templates import Messages, Keys


def send_message(api, chat_id, text, keyboard=None, random_gen=time, **kwargs):
    if keyboard:
        keyboard = keyboard.get_keyboard()

    api.messages.send(
        chat_id=chat_id,
        message=text,
        keyboard=keyboard,
        random_id=int(random_gen()),
        **kwargs,
    )


def welcome_message_handler(api, event: Event):
    keyboard = VkKeyboard()
    keyboard.add_button(Keys.START, color=VkKeyboardColor.PRIMARY)
    send_message(api, event.chat_id, Messages.WELCOME, keyboard)


def start_key_handler(api, event: Event):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(Keys.AGE_LESS_18, color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(Keys.AGE_BETWEEN_18_21, color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(Keys.AGE_GREAT_21, color=VkKeyboardColor.PRIMARY)
    send_message(api, event.chat_id, Messages.QUESTION_AGE, keyboard)


def age_less_18_key_handler(api, event: Event):
    user = BotUser.objects.get(chat_id=event.chat_id)
    user.is_active = False
    user.save()

    send_message(api, event.chat_id, Messages.AGE_LESS_18)


def age_great_18_key_handler(api, event: Event):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(Keys.INCOME_NO_MATTER, color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(Keys.INCOME_UP_TO_30, color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(Keys.INCOME_BEETWEEN_30_45,
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(Keys.INCOME_FROM_40, color=VkKeyboardColor.PRIMARY)
    send_message(api, event.chat_id, Messages.QUESTION_INCOME, keyboard)


def income_less_30_key_handler(api, event: Event):
    chat_id = event.chat_id
    keyboard = VkKeyboard(inline=True)
    cash_links = CashLink.objects.filter(type=CashLink.Type.LESS_30)
    for index, cash_link in enumerate(cash_links, 1):
        keyboard.add_openlink_button(cash_link.title, cash_link.url)
        if index < len(cash_links):
            keyboard.add_line()

    send_message(api, chat_id, Messages.CASH_LINKS_LIST)
    send_message(api, chat_id, Messages.INCOME_LESS_30_ADVICE, keyboard)

    user = BotUser.objects.get(chat_id=chat_id)
    TaskManager.tasks.create(
        type=TaskManager.Type.ASK_FOR_LOANS_1,
        date=timezone.now()+timezone.timedelta(minutes=1),
        user=user,
    )


def income_great_30_key_handler(api, event: Event):
    chat_id = event.chat_id
    keyboard = VkKeyboard(inline=True)
    cash_links = CashLink.objects.filter(type=CashLink.Type.GREAT_30)
    for index, cash_link in enumerate(cash_links, 1):
        keyboard.add_openlink_button(cash_link.title, cash_link.url)
        if index < len(cash_links):
            keyboard.add_line()

    send_message(api, chat_id, Messages.CASH_LINKS_LIST, keyboard)

    user = BotUser.objects.get(chat_id=chat_id)
    TaskManager.tasks.create(
        type=TaskManager.Type.ASK_FOR_LOANS_1,
        date=timezone.now()+timezone.timedelta(minutes=1),
        user=user,
    )


def yes_key_handler(api, event: Event):
    chat_id = event.chat_id
    user = BotUser.objects.get(chat_id=chat_id)
    if user.bot_state == States.ASK_FOR_LOANS_1 or \
       user.bot_state == States.ASK_FOR_LOANS_2:
        send_message(api, chat_id, Messages.WRITE_REVIEW)
        send_message(api, chat_id, Messages.AFTER_WRITE_REVIEW)
        user.bot_state = None
        user.save()


def no_key_handler(api, event: Event):
    chat_id = event.chat_id
    user = BotUser.objects.get(chat_id=chat_id)
    if user.bot_state == States.ASK_FOR_LOANS_1:
        keyboard = VkKeyboard(inline=True)
        cash_links = CashLink.objects.filter(type=CashLink.Type.GREAT_30)
        for index, cash_link in enumerate(cash_links, 1):
            keyboard.add_openlink_button(cash_link.title, cash_link.url)
            if index < len(cash_links):
                keyboard.add_line()

        send_message(api, chat_id, Messages.LOANS_NO_RECEIVED, keyboard)

        TaskManager.tasks.create(
            type=TaskManager.Type.ASK_FOR_LOANS_2,
            date=timezone.now()+timezone.timedelta(minutes=1),
            user=user,
        )
        user.bot_state = None
        user.save()
    elif user.bot_state == States.ASK_FOR_LOANS_2:
        send_message(api, chat_id, Messages.GOOD_BYE)
        user.bot_state = None
        user.save()


def event_handler(event: Event):
    chat_id = event.chat_id
    user, success = BotUser.objects.get_or_create(chat_id=chat_id)
    if success:
        welcome_message_handler(api, event)

    print(event.text)
    if not user.is_active:
        return

    for text, message_handler in message_handlers.items():
        if event.text.endswith(text):
            message_handler(api, event)
            break


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
        '/start': welcome_message_handler,
        Keys.START: start_key_handler,
        Keys.AGE_LESS_18: age_less_18_key_handler,
        Keys.AGE_BETWEEN_18_21: age_great_18_key_handler,
        Keys.INCOME_NO_MATTER: income_less_30_key_handler,
        Keys.INCOME_UP_TO_30: income_less_30_key_handler,
        Keys.INCOME_BEETWEEN_30_45: income_great_30_key_handler,
        Keys.INCOME_UP_TO_30: income_great_30_key_handler,
        Keys.YES: yes_key_handler,
        Keys.NO: no_key_handler,
    }
    main()
