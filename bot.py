from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  # type: ignore
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler  # type: ignore
import os

# ✅ Read TOKEN securely from environment variables (set this in Render dashboard)
TOKEN = os.getenv("TOKEN")

# ✅ Start function – first menu with exam categories
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("SSC", callback_data='ssc')],
        [InlineKeyboardButton("Railway", callback_data='railway')],
        [InlineKeyboardButton("Banking", callback_data='banking')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose your exam category:", reply_markup=reply_markup)

# ✅ Button handler for categories and subjects
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'ssc':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='ssc_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='ssc_reasoning')],
            [InlineKeyboardButton("English", callback_data='ssc_english')],
            [InlineKeyboardButton("GK/GS", callback_data='ssc_gk')],
        ]
        query.edit_message_text("SSC Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'railway':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='railway_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='railway_reasoning')],
            [InlineKeyboardButton("GK/GS", callback_data='railway_gk')],
        ]
        query.edit_message_text("Railway Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'banking':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='banking_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='banking_reasoning')],
            [InlineKeyboardButton("English", callback_data='banking_english')],
            [InlineKeyboardButton("GK/GS", callback_data='banking_gk')],
        ]
        query.edit_message_text("Banking Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        query.edit_message_text(text=f"You selected: {query.data}")

# ✅ Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
