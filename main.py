import asyncio
import datetime as dt
import logging
import os
import json

import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, BotCommand, CallbackQuery
from dotenv import load_dotenv
from dbman import sel_orgs, check_user, create_user, get_org_ru, write_la, check_adm_chat
from dbman import get_users, add_sub, del_sub, get_subs, sel_orgs_for_subs, upd_subs
from keyboards import subs_kb

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('chat_id')

bot = Bot(token=TOKEN)
dp = Dispatcher()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Запись в файл
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Запись в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

async def on_startup():
    await bot.send_message(chat_id=CHAT_ID, text='чат бот онлайн')
    bot_commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/help', description='Если ничего не работает')
    ]
    await bot.set_my_commands(bot_commands)
    logger.info("Мы запустились")


async def on_shutdown():
    await bot.send_message(chat_id=CHAT_ID, text='чат бот оффлайн')
    logger.info("Мы закрылись")



@dp.message(Command("start"))
async def start_command(message):
    await message.answer('<b>Hello!</b>', parse_mode=ParseMode.HTML)
    user_id = check_user(message.from_user.id)
    if user_id == 0:
        user_id = create_user(message.from_user.first_name, message.from_user.last_name, message.from_user.full_name,
                              message.from_user.id, message.from_user.is_premium, message.from_user.language_code)
        logger.info(f"Зарегистрирован новый пользователь {message.from_user.full_name} c id {message.from_user.id}")

    orgs = sel_orgs(user_id)
    if orgs:
        layout = []
        for org in orgs:
            layout.append([KeyboardButton(text=f'Кол-во нов заказов {org[2]}'),
                           KeyboardButton(text=f'Вывести список заказов {org[2]}')])

        keyboard = ReplyKeyboardMarkup(keyboard=layout, resize_keyboard=True,
                                       input_field_placeholder='Нажмите кнопку...')

        await message.answer('Нажмите кнопку ..', reply_markup=keyboard)
    else:
        await message.answer('Для настроек обратитесь к администратору.')


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(f'Для появления нужных команд обратитесь к администратору')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())