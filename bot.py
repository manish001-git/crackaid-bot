from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import os

TOKEN = os.getenv("TOKEN")  # Add your token in Render Environment
WEBHOOK_URL = "https://crackaid-bot-1.onrender.com"  # ✅ your Render app URL

# === In-memory storage (for testing) ===
user_data = {}

# === Start command ===
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("SSC", callback_data='ssc')],
        [InlineKeyboardButton("Railway", callback_data='railway')],
        [InlineKeyboardButton("Banking", callback_data='banking')],
        [InlineKeyboardButton("Contact Us", callback_data='contact')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎯 Choose a category:", reply_markup=reply_markup)

# === Main category handler ===
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    user_data.setdefault(user_id, {"score": 0, "attempted": 0, "last_question": None})

    if query.data == 'ssc':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='ssc_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='ssc_reasoning')],
            [InlineKeyboardButton("English", callback_data='ssc_english')],
            [InlineKeyboardButton("GK/GS", callback_data='ssc_gk')],
        ]
        query.edit_message_text("📚 SSC Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'railway':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='railway_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='railway_reasoning')],
            [InlineKeyboardButton("GK/GS", callback_data='railway_gk')],
        ]
        query.edit_message_text("🚆 Railway Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'banking':
        keyboard = [
            [InlineKeyboardButton("Maths", callback_data='banking_maths')],
            [InlineKeyboardButton("Reasoning", callback_data='banking_reasoning')],
            [InlineKeyboardButton("English", callback_data='banking_english')],
            [InlineKeyboardButton("GK/GS", callback_data='banking_gk')],
        ]
        query.edit_message_text("🏦 Banking Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'contact':
        keyboard = [
            [InlineKeyboardButton("📷 Instagram", url='https://instagram.com/yourusername')],
            [InlineKeyboardButton("📢 Telegram", url='https://t.me/yourchannel')],
            [InlineKeyboardButton("🌐 Website", url='https://yourwebsite.com')],
        ]
        query.edit_message_text("📬 Contact Info:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data in ['ssc_maths', 'railway_maths', 'banking_maths']:
        ask_question(query, user_id)

    elif query.data in ['A', 'B', 'C', 'D']:
        handle_answer(query, user_id, query.data)

    elif query.data == 'next':
        ask_question(query, user_id)

    elif query.data == 'back':
        keyboard = [
            [InlineKeyboardButton("SSC", callback_data='ssc')],
            [InlineKeyboardButton("Railway", callback_data='railway')],
            [InlineKeyboardButton("Banking", callback_data='banking')],
        ]
        score_info = user_data[user_id]
        text = f"🏁 Quiz Summary:\nAttempted: {score_info['attempted']}\nCorrect: {score_info['score']}"
        query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# === Sample questions ===
questions = [
    {
        "question": "What is 10% of 200?",
        "options": ["A. 10", "B. 20", "C. 30", "D. 40"],
        "answer": "B",
        "explanation": "10% of 200 = (10/100)*200 = 20"
    },
    {
        "question": "What is the formula for Profit?",
        "options": ["A. SP - CP", "B. CP - SP", "C. CP + SP", "D. None"],
        "answer": "A",
        "explanation": "Profit = Selling Price - Cost Price"
    },
]

# === Ask a question ===
def ask_question(query, user_id):
    index = user_data[user_id].get("last_question", 0)
    if index >= len(questions):
        query.edit_message_text("🎉 No more questions!")
        return

    q = questions[index]
    user_data[user_id]["last_question"] = index
    keyboard = [
        [InlineKeyboardButton(q["options"][0], callback_data='A')],
        [InlineKeyboardButton(q["options"][1], callback_data='B')],
        [InlineKeyboardButton(q["options"][2], callback_data='C')],
        [InlineKeyboardButton(q["options"][3], callback_data='D')],
    ]
    query.edit_message_text(f"❓ {q['question']}", reply_markup=InlineKeyboardMarkup(keyboard))

# === Handle answer ===
def handle_answer(query, user_id, selected):
    index = user_data[user_id]["last_question"]
    q = questions[index]

    user_data[user_id]["attempted"] += 1
    if selected == q["answer"]:
        user_data[user_id]["score"] += 1
        result = "✅ Correct!"
    else:
        result = f"❌ Wrong! Correct answer is: {q['answer']}"

    explanation = f"{result}\n\n💡 Explanation: {q['explanation']}"

    keyboard = [
        [InlineKeyboardButton("Next", callback_data='next')],
        [InlineKeyboardButton("🔙 Back to Categories", callback_data='back')],
    ]
    user_data[user_id]["last_question"] += 1
    query.edit_message_text(explanation, reply_markup=InlineKeyboardMarkup(keyboard))

# === Main ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    # For Render Deployment (Webhook)
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8443)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

    updater.idle()

if __name__ == '__main__':
    main()
