import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from database import interact_with_db
from amplitude import send_amplitude_event

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    await send_amplitude_event(message)
    await interact_with_db(message)

    full_name_url = f"<a href='{message.from_user.url}'>{message.from_user.full_name}</a>"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Кнопка, которая ведёт в Telegram Web App',
                              web_app={'url': 'https://127.0.0.1:8000/bots/select_character'})]
    ])

    await message.answer(f"{full_name_url}, я отправляю приветственное сообщение с объяснением того, что я делаю!",
                         parse_mode=ParseMode.HTML, reply_markup=keyboard)


async def start_bot() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(start_bot())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
    except Exception as e:
        print(f'Error: {e}')
