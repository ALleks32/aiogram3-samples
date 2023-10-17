from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class SupportKeyboard:
    @staticmethod
    def session_create_down():
        kb = [KeyboardButton(text="Написать поддержке")]
        return ReplyKeyboardMarkup(
            keyboard=[kb],
            resize_keyboard=True
        )

    @staticmethod
    def session_exit_down():
        kb = [KeyboardButton(text="Завершить сеанс")]
        return ReplyKeyboardMarkup(
            keyboard=[kb],
            resize_keyboard=True
        )
