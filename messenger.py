
__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from functools import lru_cache

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from telegram import Bot
import os
import imgkit, pdfkit


class TelegramSettings(BaseSettings):
    bot_token: str
    chat_id: str

    model_config = SettingsConfigDict(extra='ignore', env_prefix='TELEGRAM_')


@lru_cache
def get_telegram_settings() -> TelegramSettings:
    try:
        return TelegramSettings()
    except ValidationError:
        pass

    return TelegramSettings(_env_file='.env')


async def send_message(message: str) -> bool:
    settings = get_telegram_settings()
    bot = Bot(settings.bot_token)
    try:
        imgkit.from_string(message, f'{settings.chat_id}.jpg', options=options)
        with open(f'{settings.chat_id}.jpg', 'rb') as image:
            await bot.send_photo(settings.chat_id, image)

        # Delete the image after sending
        os.remove(f'{settings.chat_id}.jpg')
       
    except Exception:
        return False
    return True
