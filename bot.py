from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import base64
from datetime import datetime
import os

# --- настройки ---
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = 1099598015
MAX_REQUESTS = 5

TOTAL_LIMIT = 500
total_requests = 0

client = OpenAI(api_key=OPENAI_API_KEY)
user_limits = {}

# --- старт ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📸 Сканировать крепёж"],
        ["📩 Обратная связь"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "FixScan определяет крепёж по фото за 5 секунд.\n\n"
        "Полезно:\n— на объекте\n— при заказчике\n— когда сомневаешься\n\n"
        "Отправь фото 👇",
        reply_markup=reply_markup
    )

# --- обратная связь ---
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Напишите отзыв")
    context.user_data["feedback"] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "📩 Обратная связь":
        await feedback(update, context)
        return

    if context.user_data.get("feedback"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Отзыв:\n{update.message.text}"
        )
        await update.message.reply_text("✅ Спасибо!")
        context.user_data["feedback"] = False
        return

    if update.message.text == "📸 Сканировать крепёж":
        await update.message.reply_text("📷 Отправь фото")
        return

    await update.message.reply_text("Нажми кнопку ниже 👇")

# --- обработка фото ---
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_requests

    if total_requests >= TOTAL_LIMIT:
        await update.message.reply_text("⚠️ Сервис временно перегружен. Попробуй позже 🙌")
        return
        
    user_id = update.message.from_user.id
    today = datetime.now().date()

    if user_id not in user_limits:
        user_limits[user_id] = {"count": 0, "date": today}

    if user_limits[user_id]["date"] != today:
        user_limits[user_id] = {"count": 0, "date": today}

    if user_limits[user_id]["count"] >= MAX_REQUESTS:
        await update.message.reply_text("❌ Лимит 5 фото в день...")
        return

    user_limits[user_id]["count"] += 1
    total_requests += 1

    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("photo.jpg")

    await update.message.reply_text("🔍 Анализирую...")

    with open("photo.jpg", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": """Определи:
1. Тип
2. Размер
3. Назначение

Формат:
Тип: ...
Размер: ...
Назначение: ...

Если не видно → "нет данных"
"""},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ]
        }]
    )

    result = response.output_text or "Ошибка"

    await update.message.reply_text(result)
    await update.message.reply_text("Правильно определил?\n👍 Да / 👎 Нет")
    
# --- запуск ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, photo))

print("BOT STARTED")

app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://fixscan-wj3x.onrender.com/webhook",
    url_path="webhook"
)
