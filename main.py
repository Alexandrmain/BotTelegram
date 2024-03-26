from aiogram import F, Router
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





import sqlite3

from aiogram.client.session.aiohttp import AiohttpSession

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# Объект бота
# session = AiohttpSession(proxy="http://proxy.server:3128/")


connect = sqlite3.connect('links.db')
c = connect.cursor()
# Создаем таблицу для хранения ссылок, если ее еще не существует
c.execute('''CREATE TABLE IF NOT EXISTS links
             (link TEXT PRIMARY KEY)''')
connect.commit()

bot = Bot(token="6905517366:AAFxqTsI3m5vBIf7eLAbTpJ_IWmyBC_q3Uk")
# Диспетчер
dp = Dispatcher()

links = []

router = Router()


x= ['@Aleksanddatoest']
class Link(StatesGroup):
    link_new = State()

klava = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/new')]
], resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer("Hello!", reply_markup=klava)




@dp.message(Command('new'))
async def add_link_command(message: types.Message, state: FSMContext):
    await message.answer("Введите новую ссылку", reply_markup=klava)
    await state.set_state(Link.link_new)


# Обработка введенной пользователем ссылки
@dp.message(Link.link_new)
async def update_link(message: types.Message, state: FSMContext):
    user_input = message.text.strip()  # Текст, введенный пользователем

    # Проверяем наличие ссылки в базе данных
    c.execute('SELECT * FROM links WHERE link=?', (user_input,))
    result = c.fetchone()
    if result:
        await message.answer("Такая ссылка уже есть", reply_markup=klava)
    else:
        # Если ссылка отсутствует в базе данных, добавляем ее
        c.execute('INSERT INTO links (link) VALUES (?)', (user_input,))
        connect.commit()
        await message.answer("Вы добавили новую ссылку", reply_markup=klava)

    await state.clear()


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот начал работу")
    asyncio.run(main())

