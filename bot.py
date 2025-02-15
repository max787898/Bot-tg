import asyncio
import os
import random
from telethon import TelegramClient

# Данные первого аккаунта
API_ID_1 = int(os.getenv("API_ID_1"))  # API ID первого аккаунта
API_HASH_1 = os.getenv("API_HASH_1")  # API Hash первого аккаунта

# Данные второго аккаунта
API_ID_2 = int(os.getenv("API_ID_2"))  # API ID второго аккаунта
API_HASH_2 = os.getenv("API_HASH_2")  # API Hash второго аккаунта

# ID группы, из которой берем участников
GROUP_ID = os.getenv("GROUP_ID")  # ID группы

# Сообщения для отправки (разделены "|")
MESSAGE_TEXTS = os.getenv("MESSAGE_TEXTS", "Привет!|Как дела?|Рад знакомству!").split("|")

# Создаем клиентов для двух аккаунтов
client1 = TelegramClient('session_1', API_ID_1, API_HASH_1)
client2 = TelegramClient('session_2', API_ID_2, API_HASH_2)

async def send_messages(client, account_name):
    """ Функция для отправки сообщений от одного аккаунта """
    async for user in client.iter_participants(GROUP_ID):
        try:
            message = random.choice(MESSAGE_TEXTS)  # Выбираем случайное сообщение
            await client.send_message(user.id, message)
            print(f"✅ {account_name}: Отправлено сообщение пользователю {user.id}: {message}")
            await asyncio.sleep(180)  # Интервал 3 минуты перед отправкой от второго аккаунта
        except Exception as e:
            print(f"⚠ {account_name}: Ошибка при отправке пользователю {user.id}: {e}")

async def main():
    """ Главная функция, которая чередует отправку сообщений от двух аккаунтов """
    await client1.start()
    await client2.start()
    
    print("🤖 Бот запущен! Отправка сообщений начнется...")
    
    while True:
        await send_messages(client1, "Аккаунт 1")  # Первый аккаунт отправляет сообщения
        await send_messages(client2, "Аккаунт 2")  # Второй аккаунт отправляет сообщения

# Запускаем бота
with client1, client2:
    client1.loop.run_until_complete(main())
