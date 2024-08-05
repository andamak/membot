from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dbman import check_subs


def subs_kb(user_id, orgs):
    inline_kb_list = []
    for org in orgs:
        if check_subs(org[0], user_id):
            inline_kb_list.append([InlineKeyboardButton(text=f'Отписаться от уведомлений по орг {org[3]}',
                                                        callback_data=f'del_sub_{org[0]}_{user_id}')])
        else:
            inline_kb_list.append([InlineKeyboardButton(text=f'Подписаться на уведомления по орг {org[3]}',
                                                        callback_data=f'add_sub_{org[0]}_{user_id}')])

    inline_kb_list.append([InlineKeyboardButton(text=f'Скрыть все варианты',
                                                callback_data=f'remove_inline_keyboard')])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)