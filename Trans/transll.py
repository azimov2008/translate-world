import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

translator = Translator()

LANGUAGES = {
    'en': 'English',
    'ru': 'Russian',
    'es': 'Spanish',
    'de': 'German',
    'fr': 'French',
    'it': 'Italian'
}


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang], callback_data=lang) for lang in LANGUAGES]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите язык для перевода:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    language = query.data

    context.user_data['target_language'] = language

    query.edit_message_text(text=f"Вы выбрали язык: {LANGUAGES[language]}. Напишите текст для перевода:")


def set_language(update: Update, context: CallbackContext) -> None:

    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang], callback_data=lang) for lang in LANGUAGES]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите новый язык для перевода:', reply_markup=reply_markup)


def translate_text(update: Update, context: CallbackContext) -> None:
    target_language = context.user_data.get('target_language', 'en')
    text_to_translate = update.message.text

    try:
        translated = translator.translate(text_to_translate, dest=target_language)
        update.message.reply_text(f"Перевод: {translated.text}")

        keyboard = [
            [InlineKeyboardButton("Сменить язык", callback_data="change_language")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Хотите сменить язык для перевода?', reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка при переводе: {str(e)}")


def change_language(update: Update, context: CallbackContext) -> None:

    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang], callback_data=lang) for lang in LANGUAGES]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.edit_text('Выберите новый язык для перевода:', reply_markup=reply_markup)


def main():
    TOKEN = '7260894808:AAFgO1QHBf556QTBa7ThJ7pUZV8HSu3zZGc'
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("setlanguage", set_language))

    dispatcher.add_handler(CallbackQueryHandler(button, pattern="^(?!change_language$).*$"))

    dispatcher.add_handler(CallbackQueryHandler(change_language, pattern="^change_language$"))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
