from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import base64
from datetime import datetime

user_limits = {}
MAX_REQUESTS = 50

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📸 Сканировать крепёж"],
        ["📩 Обратная связь"]
]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
         "👋 Привет! Я FixScan AI\n\n"

         "📸 Отправь фото крепежа — определю:\n"
         "• тип\n"
         "• размер\n"
         "• назначение\n\n"

         "👇 Нажми кнопку ниже и отправь фото",
     reply_markup=reply_markup
)

ADMIN_ID = 1099598015  # сюда свой ID

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Напишите отзыв или идею для улучшения")
    context.user_data["feedback"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 1. если нажал кнопку обратной связи
    if update.message.text == "📩 Обратная связь":
        await feedback(update, context)
        return

    # 2. если пользователь пишет отзыв
    if context.user_data.get("feedback"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Новый отзыв:\n\n{update.message.text}"
        )  
        await update.message.reply_text("✅ Спасибо за отзыв!")
        context.user_data["feedback"] = False
        return

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 Отправь фото крепежа")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    today = datetime.now().date()

    # если новый пользователь
    if user_id not in user_limits:
        user_limits[user_id] = {"count": 0, "date": today}

    # если новый день — сброс
    if user_limits[user_id]["date"] != today:
        user_limits[user_id] = {"count": 0, "date": today}

    # проверка лимита
    if user_limits[user_id]["count"] >= MAX_REQUESTS:
        await update.message.reply_text("❌ Лимит 5 фото в день. Попробуйте завтра")
        return

    # увеличиваем счётчик
    user_limits[user_id]["count"] += 1

    photo = update.message.photo[-1]
    file = await photo.get_file()

    await file.download_to_drive("photo.jpg")

    await update.message.reply_text("Анализирую...")

    with open("photo.jpg", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text":"""Ты определяешь крепёж по фото.
1. Правила
- Не угадывай
- Если не уверен — пиши "нет данных"
- Не завышай размер
- Не пиши лишний текст

2. Главный приоритет определения
- Сначала смотри на НАКОНЕЧНИК
- Потом на ГОЛОВКУ
- Потом на ШЛИЦ

3. Типы
- Саморез — острый наконечник
- Болт — тупой конец + шестигранная головка
- Винт — тупой конец + есть шлиц

4. Жёсткие правила (самое важное)
- Острый наконечник → ВСЕГДА саморез
- Шестигранная внешняя головка → ВСЕГДА болт
- Если есть шлиц и нет шестигранной головки → винт

5. Шлиц
- Учитывай только если явно виден
- Внешняя шестигранная головка — это НЕ шлиц

6. Размер
- Можно оценивать размер по визуальному масштабу (палец, поверхность, пропорции)
- Если объект хорошо виден — ОБЯЗАТЕЛЬНО укажи размер
- Не завышай диаметр
- Используй мм
- Сначала диаметр, потом длину
- Формат: 4 x 40 мм

- Пиши "нет данных" ТОЛЬКО если:
  • объект плохо виден
  • нет понимания масштаба
- Если крепёж хорошо виден — старайся определить размер, не пропускай его

7. Назначение
- Крупная редкая резьба → крепление дерева
- Мелкая частая резьба → крепление металла
- Неясно → универсальное крепление

8. Определи
1. Тип
2. Размер
3. Назначение

9. Формат ответа
1. Тип: ...
2. Размер: ...
3. Назначение: ...

10. Запрещено
- Писать "примерно", "на глаз"
- Добавлять пояснения
- Придумывать

11. Важно
- Если фото плохое → "нет данных"
- Отвечай строго по формату
"""},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ]
        }]
    )

    result = response.output_text

    await update.message.reply_text(   
    result + "\n\n📸 Отправьте ещё фото или выберите действие ниже"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Сканировать"), scan))
app.add_handler(MessageHandler(filters.PHOTO, photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("BOT STARTED")

app.run_polling()
