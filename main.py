import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import logging



# Set your Telegram bot token
TOKEN = ':'
# Set your Google Custom Search JSON API key
API_KEY = '--'
# Set your Engine ID for search
ENGINE_ID = ''

def start(update: Update, context):
    """Обработчик команды /start"""
    update.message.reply_text('Привет! Я бот для поиска изображений в Google. Просто отправь мне запрос, и я найду для тебя картинки!')


def search_image(update: Update, context):
    """Обработчик текстового сообщения"""
    query = update.message.text

    # Выполняем поиск изображений в Google
    search_url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': ENGINE_ID,
        'q': query,
        'searchType': 'image'
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    # Получаем URL всех найденных изображений
    if 'items' in data and len(data['items']) > 0:
        image_urls = [item['link'] for item in data['items']]
        for image_url in image_urls[:50]:  # Отправляем только первые 5 изображений
            update.message.reply_document(image_url)
    else:
        update.message.reply_text('Изображения не найдены.')


def error(update: Update, context):
    """Обработчик ошибок"""
    logging.error(f'Update {update} caused error {context.error}')


def main():
    """Основная функция для запуска бота"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, search_image))
    dp.add_error_handler(error)

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()
