from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup # type: ignore
from telegram.ext import Updater, CommandHandler, CallbackContext # type: ignore
import os

TOKEN = os.getenv("TOKEN")


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("SSC", callback_data='ssc')],
        [InlineKeyboardButton("Railway", callback_data='railway')],
        [InlineKeyboardButton("Banking", callback_data='banking')],
        [InlineKeyboardButton("Current Affairs", callback_data='current')],
        [InlineKeyboardButton("Contact", url='https://t.me/your_contact')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to CrackAid Quiz Bot! 👇 Select a category:", reply_markup=reply_markup)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
