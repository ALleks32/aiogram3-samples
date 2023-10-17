from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from core.config.config import bot, support_chat_id
from core.keyboard.user_support_keyboard import SupportKeyboard
from core.db.support_db import SupportTicket

user_key = {"key": "user"}
user_support_router = Router()
command_support_router = Router()


class SupportState(StatesGroup):
    set_data_dialog = State()
    user_session = State()


@command_support_router.message(F.text == 'Написать поддержке', flags=user_key)
async def ask_support(message: Message, state: FSMContext):
    await state.clear()
    await message_start_dialog(message.chat.id)
    thread_id = await support_thread_connect(message)
    await state.update_data(thread_id=thread_id)
    await state.set_state(SupportState.set_data_dialog)


async def message_start_dialog(chat_id: int):
    keyboard = SupportKeyboard().session_exit_down()
    await bot.send_message(
        text="Все ваши следующие сообщения получит техничский специалист",
        chat_id=chat_id,
        reply_markup=keyboard)


async def support_thread_connect(message: Message):
    if SupportTicket().check_user(message.from_user.id):
        thread_id = SupportTicket().id_thread(id_user=message.from_user.id)
    else:
        thread = await new_thread(chat_id=support_chat_id,
                                  user_name=message.from_user.full_name)
        thread_id = thread.message_thread_id
        SupportTicket().add_thread(thread_id, message.chat.id)
        await message_thread(thread_id, message.from_user.full_name)
    return thread_id


async def message_thread(thread_id: int, full_name: str):
    await bot.send_message(chat_id=support_chat_id,
                           message_thread_id=thread_id,
                           text='Вопрос от: ' + full_name)


async def new_thread(chat_id: int, user_name: str):
    return await bot.create_forum_topic(
        chat_id=chat_id,
        name='Вопрос от ' + user_name,
        icon_color=7322096)


@command_support_router.message(F.text == 'Завершить сеанс', flags=user_key)
async def ask_support(message: Message, state: FSMContext):
    await close_message(message)
    SupportTicket().delete_thread(message.from_user.id)
    try:
        await close_support_thread(message)
    except:
        print('Тема была удалена ранее чем ее закрыл пользователь')
    await state.clear()


async def close_message(message: Message):
    chat_id = message.chat.id
    text = "вы закрыли сессию с поддержкой"
    await bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=SupportKeyboard().session_create_down())


async def close_support_thread(message: Message):
    thread_id = SupportTicket().id_thread(id_user=message.from_user.id)
    await bot.edit_forum_topic(
        chat_id=support_chat_id,
        message_thread_id=thread_id,
        name=message.from_user.full_name + ' тема закрыта')
    await bot.close_forum_topic(
        chat_id=support_chat_id,
        message_thread_id=thread_id)


@user_support_router.message(SupportState.set_data_dialog, flags=user_key)
async def set_data_dialog(message: Message, state: FSMContext):
    try:
        thread_id = SupportTicket().id_thread(id_user=message.from_user.id)
        await bot.copy_message(chat_id=support_chat_id,
                               from_chat_id=message.chat.id,
                               message_id=message.message_id,
                               message_thread_id=thread_id)
    except:
        SupportTicket().delete_thread(message.from_user.id)
        thread = await new_thread(chat_id=support_chat_id,
                                  user_name=message.from_user.full_name)
        thread_id = thread.message_thread_id
        SupportTicket().add_thread(thread_id, message.chat.id)
        await message_thread(thread_id, message.from_user.full_name)
        await bot.copy_message(chat_id=support_chat_id,
                               from_chat_id=message.chat.id,
                               message_id=message.message_id,
                               message_thread_id=thread_id)
