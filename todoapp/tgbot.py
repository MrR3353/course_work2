import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import requests

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f"Привет! Твой telegram chat id: `{message.chat.id}`", parse_mode=ParseMode.MARKDOWN)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


def send_notification(tg_chat_id, text):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    try:
        response = requests.post(url, data={'chat_id': tg_chat_id, 'text': text})
        if response.status_code != 200:
            print(response.text)
            raise Exception
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Bot running')
    dp.run_polling(bot)



