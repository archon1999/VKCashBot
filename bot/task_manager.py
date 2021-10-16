import time
import traceback

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config
from states import States

from backend.models import BotUser, CashLink, TaskManager
from backend.templates import Messages, Keys


def send_message(api, chat_id, text, keyboard=None, random_gen=time.time, **kwargs):
    if keyboard:
        keyboard = keyboard.get_keyboard()

    api.messages.send(
        chat_id=chat_id,
        message=text,
        keyboard=keyboard,
        random_id=int(random_gen()),
        **kwargs,
    )


def main():
    vk_session = vk_api.VkApi(token=config.TOKEN)
    api = vk_session.get_api()
    while True:
        if (task := TaskManager.unfulfilled.last()) is None:
            time.sleep(5)
            continue

        try:
            if task.type == TaskManager.Type.ASK_FOR_LOANS_1:
                user = task.user
                user.bot_state = States.ASK_FOR_LOANS_1
                user.save()
                chat_id = user.chat_id
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button(Keys.YES, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button(Keys.NO, color=VkKeyboardColor.PRIMARY)
                send_message(api, chat_id, Messages.ASK_FOR_LOANS, keyboard)
            elif task.type == TaskManager.Type.ASK_FOR_LOANS_2:
                user = task.user
                user.bot_state = States.ASK_FOR_LOANS_2
                user.save()
                chat_id = user.chat_id
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button(Keys.YES, color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button(Keys.NO, color=VkKeyboardColor.PRIMARY)
                send_message(api, chat_id, Messages.ASK_FOR_LOANS, keyboard)

            task.done = True
        except Exception:
            print(traceback.format_exc())
        finally:
            task.save()
            time.sleep(5)


if __name__ == '__main__':
    main()
