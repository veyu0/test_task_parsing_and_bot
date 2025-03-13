import logging
import pandas as pd
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode

from database import insert_data, create_table
from parser import parse_price

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token="1864328239:AAEHD7aPYmtXqpihP9ggqx-jmakJMh_-g4Y")
dp = Dispatcher()


# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Загрузить файл"))
    await message.answer(
        "Привет! Нажми кнопку, чтобы загрузить файл Excel с данными для парсинга.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

# Обработка кнопки Загрузить файл
@dp.message(F.text == "Загрузить файл")
async def load_file(message: types.Message):
    await message.answer("Следующим сообщением отправьте ваш файл Excel.")


# Обработка файла
@dp.message(
    lambda message: message.document and message.document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
async def handle_file(message: types.Message):
    # Скачивание файла
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "data.xlsx")

    # Чтение файла Excel
    try:
        df = pd.read_excel("data.xlsx")
        # Вывод содержимого файла пользователю
        await message.answer(f"Содержимое файла:\n<pre>{df.to_string(index=False)}</pre>", parse_mode=ParseMode.HTML)

        # Сохранение данных в базу данных
        for index, row in df.iterrows():
            insert_data(row['title'], row['url'], row['xpath'])

        await message.answer("Данные успешно сохранены в базу данных.")

        prices = []
        for index, row in df.iterrows():
            price = parse_price(row['url'], row['xpath'])
            if price:
                prices.append(price)

        if prices:
            average_price = sum(prices) / len(prices)
            await message.answer(f"Средняя цена зюзюблика: {average_price:.2f}")
        else:
            await message.answer("Не удалось получить цены с сайтов.")

    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await message.answer("Произошла ошибка при обработке файла. Пожалуйста, проверьте формат файла.")


# Обработка неизвестных команд
@dp.message()
async def unknown(message: types.Message):
    await message.answer("Извините, я не понимаю эту команду.")


# Запуск бота
async def main():
    # Создание таблицы в базе данных
    create_table()

    # Запуск polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
