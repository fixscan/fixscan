from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

main_keyboard = [
        ["📸 Определить крепёж"],
        ["🔩 Подобрать крепёж"],
        ["✍️ Обратная связь"]
    ]

TOKEN = os.getenv("TOKEN")

# --- СТАРТ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "🔩 Добро пожаловать в FixScan\n\n"
        "Помогу определить крепёж по фото или подобрать крепёж для вашей задачи\n\n"
        "👇 Выберите действие",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )


# --- ОБРАБОТКА ФОТО ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Фото получено.\n"
        "🚧 Функция анализа находится в разработке."
    )


# --- ОСНОВНАЯ ЛОГИКА ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    wall_keyboard = [
        ["🧱 Бетон", "🧱 Кирпич"],
        ["🪨 Газобетон", "🪵 Гипсокартон"]
    ]

    # --- КНОПКИ ---
    if "подобрать" in text:
        keyboard = [
            ["📚 Полка", "📺 Телевизор"],
            ["🪞 Зеркало", "🪟 Карниз"],
            ["🍽️ Кухонный шкаф"]
        ]

        await update.message.reply_text(
            "Что нужно закрепить?",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if "полка" in text:
        context.user_data["object"] = "полка"

        await update.message.reply_text(
            "Какая стена?",
            reply_markup=ReplyKeyboardMarkup(wall_keyboard, resize_keyboard=True)
        )
        
        return

    if "телевизор" in text:
        context.user_data["object"] = "телевизор"

        await update.message.reply_text(
            "Какая стена?",
            reply_markup=ReplyKeyboardMarkup(wall_keyboard, resize_keyboard=True)
        )
        
        return

    if "зеркало" in text:
        context.user_data["object"] = "зеркало"

        await update.message.reply_text(
            "Какая стена?",
            reply_markup=ReplyKeyboardMarkup(wall_keyboard, resize_keyboard=True)
        )
        
        return

    if "карниз" in text:
        context.user_data["object"] = "карниз"

        await update.message.reply_text(
            "Какая стена?",
            reply_markup=ReplyKeyboardMarkup(wall_keyboard, resize_keyboard=True)
        )
        
        return

    if "кухонный шкаф" in text:
        context.user_data["object"] = "кухонный шкаф"

        await update.message.reply_text(
            "Какая стена?",
            reply_markup=ReplyKeyboardMarkup(wall_keyboard, resize_keyboard=True)
        )
         
        return
   
    if text == "🧱 бетон":

        obj = context.user_data.get("object")

        if obj == "полка":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель 6×40\n"
            "• Саморез 4×50\n\n"
            "⚠️ Проверить горизонталь уровнем\n"
            "⚠️ Учитывать предполагаемую нагрузку"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "телевизор":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Анкер 10×80\n\n"
            "⚠️ Использовать все точки крепления кронштейна\n"
            "⚠️ Проверить надёжность крепления кронштейна\n"
            "⚠️ Не превышать допустимый вес крепления"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return
        
        elif obj == "зеркало":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель 6×40\n"
            "• Саморез 4×50\n\n"
            "⚠️ Учитывать вес зеркала\n"
            "⚠️ Не устанавливать на повреждённую поверхность\n"
            "⚠️ Проверить надёжность крепления"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "карниз":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель 6×40\n"
            "• Саморез 4×50\n\n"
            "⚠️ Проверить отсутствие проводки над окном\n"
            "⚠️ Соблюдать одинаковое расстояние от потолка"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "кухонный шкаф":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Анкер 10×80\n"
            "• Не менее 4 точек крепления\n\n"
            "⚠️ Учитывать вес посуды и содержимого\n"
            "⚠️ Проверить прочность стены\n"
            "⚠️ Использовать все предусмотренные точки крепления"
            )
   
            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

    if text == "🧱 кирпич":

        obj = context.user_data.get("object")

        if obj == "полка":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель 6×40\n"
            "• Саморез 4×50\n\n"
            "⚠️ Проверить горизонталь уровнем\n"
            "⚠️ Учитывать предполагаемую нагрузку"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "телевизор":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Анкер 10×80\n\n"
            "⚠️ Использовать все точки крепления кронштейна"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "зеркало":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель 6×40\n"
            "• Саморез 4×50\n\n"
            "⚠️ Учитывать вес зеркала\n"
            "⚠️ Не устанавливать на повреждённую поверхность\n"
            "⚠️ Проверить надёжность крепления"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "карниз":
             await update.message.reply_text(
             "Рекомендуемый крепёж:\n"
             "• Дюбель 6×40\n"
             "• Саморез 4×50\n\n"
             "⚠️ Проверить отсутствие проводки над окном\n"
             "⚠️ Соблюдать одинаковое расстояние от потолка"
             )

             await update.message.reply_text(
             "👇 Выберите действие",
             reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
             )
             return

        elif obj == "кухонный шкаф":
             await update.message.reply_text(
             "Рекомендуемый крепёж:\n"
             "• Анкер 10×80\n"
             "• Не менее 4 точек крепления\n\n"
             "⚠️ Учитывать вес посуды и содержимого\n"
             "⚠️ Проверить прочность стены\n"
             "⚠️ Использовать все предусмотренные точки крепления"
             )

             await update.message.reply_text(
             "👇 Выберите действие",
             reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
             )
             return    
        

    if text == "🪨 газобетон":
        
        obj = context.user_data.get("object")

        if obj == "полка":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель для газобетона\n"
            "• Саморез 5×60\n\n"
            "⚠️ Проверить горизонталь уровнем\n"
            "⚠️ Учитывать предполагаемую нагрузку"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return  

        elif obj == "телевизор":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Специальный анкер для газобетона\n\n"
            "⚠️ Использовать все точки крепления кронштейна\n"
            "⚠️ Проверить прочность основания"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "зеркало":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель для газобетона\n"
            "• Саморез 5×60\n\n"
            "⚠️ Учитывать вес зеркала\n"
            "⚠️ Проверить надёжность крепления"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "карниз":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель для газобетона\n"
            "• Саморез 5×60\n\n"
            "⚠️ Проверить отсутствие проводки над окном\n"
            "⚠️ Соблюдать одинаковое расстояние от потолка"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "кухонный шкаф":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Химический анкер\n"
            "• Не менее 4 точек крепления\n\n"
            "⚠️ Учитывать вес посуды и содержимого\n"
            "⚠️ Проверить прочность основания"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return
        

    if text == "🪵 гипсокартон":

        obj = context.user_data.get("object")

        if obj == "полка":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель Molly\n\n"
            "⚠️ Учитывать предполагаемую нагрузку\n"
            "⚠️ Проверить горизонталь уровнем"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return 

        elif obj == "телевизор":
            await update.message.reply_text(
            "❌ Крепление запрещено.\n\n"
            "Причина:\n"
            "• Недостаточная прочность гипсокартона.\n\n"
            "Рекомендуется крепление через закладную или к несущей стене."
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "зеркало":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель Molly\n\n"
            "⚠️ Учитывать вес зеркала\n"
            "⚠️ Проверить надёжность крепления"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "карниз":
            await update.message.reply_text(
            "Рекомендуемый крепёж:\n"
            "• Дюбель Molly\n\n"
            "⚠️ Проверить отсутствие проводки\n"
            "⚠️ Соблюдать одинаковое расстояние от потолка"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return

        elif obj == "кухонный шкаф":
            await update.message.reply_text(
            "⚠️ Крепление только через закладную.\n\n"
            "⚠️ Учитывать вес шкафа и содержимого\n"
            "⚠️ Проверить прочность основания"
            )

            await update.message.reply_text(
            "👇 Выберите действие",
            reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
            )
            return
        

    if "определить" in text:
        await update.message.reply_text("📸 Скинь фото крепежа 👇")
        return

    if "обратная" in text:
        context.user_data["feedback"] = True
        await update.message.reply_text("Напиши что улучшить:")
        return

    # --- ФИДБЭК ---
    if context.user_data.get("feedback"):
        print("FEEDBACK:", update.message.text)
        context.user_data["feedback"] = False
        await update.message.reply_text("Спасибо! 👍")
        return

    step = context.user_data.get("step")

    # --- СТЕНА ---
    if step == "wall":
        context.user_data["wall"] = text
        context.user_data["step"] = "load"
        await update.message.reply_text("Какая нагрузка? (лёгкая / средняя / тяжёлая)")
        return

    # --- НАГРУЗКА ---
    if step == "load":
        wall = context.user_data.get("wall", "")
        load = text

        if "кирпич" in wall:
            if "лёг" in load:
                result = "🔧 Дюбель 6x30\n💡 Можно 6x40"
            elif "сред" in load:
                result = "🔧 Дюбель 6x40 или 8x40\n💡 Лучше 8x40"
            else:
                result = "🔧 Анкер 8x60+"

        elif "бетон" in wall:
            if "лёг" in load:
                result = "🔧 Дюбель 6x30"
            elif "сред" in load:
                result = "🔧 Дюбель 6x40 или 8x40"
            else:
                result = "🔧 Анкер 8x60+"

        elif "гипс" in wall:
            if "лёг" in load:
                result = "🔧 Бабочка / молли"
            elif "сред" in load:
                result = "🔧 Молли"
            else:
                result = "⚠️ Нужен профиль"

        else:
            result = "Напиши материал стены точнее"

        keyboard = [["👍 Да", "👎 Нет"]]

        await update.message.reply_text(
            result + "\n\nПодходит?",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

        context.user_data["step"] = None
        return

    # --- КНОПКИ ОТВЕТА ---
    if "да" in text:
        await update.message.reply_text("🔥 Отлично!")
        return

    if "нет" in text:
        await update.message.reply_text("Ок, напиши подробнее или скинь фото")
        return


# --- ЗАПУСК ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT, handle_text))

print("BOT STARTED")
app.run_polling()
