def analyze_message(text):
    scam_words = [
        "вы выиграли",
        "переведите деньги",
        "подтвердите карту",
        "код из смс",
        "срочно",
        "ваш аккаунт заблокирован"
    ]

    text_lower = text.lower()

    for word in scam_words:
        if word in text_lower:
            return "⚠️ Возможное мошенничество"

    return "✅ Сообщение выглядит безопасным"


# пример проверки
message = "Ваш аккаунт заблокирован, срочно подтвердите карту"
result = analyze_message(message)

print(result)
print("FixScan AI started")
