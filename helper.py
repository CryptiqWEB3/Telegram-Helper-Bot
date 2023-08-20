import os
import logging
import requests
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL_WHITEPAPER = os.getenv("URL_WHITEPAPER")
URL_WEBSITE = os.getenv("URL_WEBSITE")
URL_CRYPTIQ = os.getenv("URL_CRYPTIQ")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def companion(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    welcome_image_url = 'https://cryptiq.online/wp-content/uploads/2023/08/Capture-1536x829.png'
    
    # Download the image
    response = requests.get(welcome_image_url)
    response.raise_for_status()

    # Send the image
    context.bot.send_photo(chat_id=chat_id, photo=BytesIO(response.content))

    keyboard = [
        [
            InlineKeyboardButton("DOWNLOAD_BROWSER", url=URL_CRYPTIQ),
        ],
        [
            InlineKeyboardButton("Whitepaper", url=URL_WHITEPAPER),
            InlineKeyboardButton("Website", url=URL_WEBSITE),
        ],
        [
            InlineKeyboardButton("Socials", callback_data="socials"),
        ],
        [
            InlineKeyboardButton("Utilities", callback_data="bot_catalogue"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Welcome to the Cryptiq Companion, bringing you up to date information on our products and services as well as links to buy and our social networks", reply_markup=reply_markup)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "socials":
        keyboard = [
            [
                InlineKeyboardButton("Twitter", url="https://twitter.com/_cryptiq"),
                InlineKeyboardButton("Instagram", url="https://instagram.com/cryptiqweb3"),
            ],
            [
                InlineKeyboardButton("Back", callback_data="back_main"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Socials:", reply_markup=reply_markup)

    elif query.data == "bot_catalogue":
        keyboard = [
            [
                InlineKeyboardButton("Cryptiq Chat", url="https://chat.cryptiq.online"),
                InlineKeyboardButton("Shibarium ChitChat", url="https://shibarium.cc"),
            ],
            [
                InlineKeyboardButton("Cryptiq Music", url="https://music.cryptiq.online"),
                InlineKeyboardButton("Cryptiq Media", url="https://media.cryptiq.online"),
            ],
            [
                InlineKeyboardButton("Cryptiq AI", url="https://ai.cryptiq.online"),
                InlineKeyboardButton("Cryptiq Draw", url="https://draw.cryptiq.online"),
            ],
            [
                InlineKeyboardButton("Back", callback_data="back_main"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Bot Catalogue:", reply_markup=reply_markup)

    elif query.data == "back_main":
        keyboard = [
            [
                InlineKeyboardButton("DOWNLOAD BROWSER", url=URL_CRYPTIQ),
            ],
            [
                InlineKeyboardButton("Whitepaper", url=URL_WHITEPAPER),
                InlineKeyboardButton("Website", url=URL_WEBSITE),
            ],
            [
                InlineKeyboardButton("Socials", callback_data="socials"),
            ],
            [
                InlineKeyboardButton("Utilities", callback_data="bot_catalogue"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Choose an option:", reply_markup=reply_markup)

def main():
    updater = Updater(token=TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("companion", companion))
    dp.add_handler(MessageHandler(Filters.text(["bot", "Bot"]), companion))
    dp.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
