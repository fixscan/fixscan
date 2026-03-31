from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import base64
from openai import OpenAI

from datetime import datetime

import json

limits = {}
history = []

# создаем приложение
app = FastAPI()

# подключаем статику (иконка + manifest)
app.mount("/static", StaticFiles(directory="static"), name="static")

# подключаем OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# главная страница
@app.get("/")
def home():
    return HTMLResponse("""
<html>
<head>
    <title>FixScan</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 30px;
        }

        .box {
            background: #1e293b;
            padding: 20px;
            border-radius: 20px;
            max-width: 400px;
            margin: auto;
            overflow: hidden;
        }

        button {
            background: #4ade80;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            width: 100%;
            margin-top: 10px;
        }
        input  {
            margin-top: 10px;
        }
        #result {
            max-height: 140px;
            overflow-y: auto;
            word-break: break-word;
            text-align: left;
            font-size: 14px;
            line-height: 1.5;
        }
    </style>
</head>

<body>

<h1>🔧 FixScan</h1>

<div class="box">

<input type="file" id="fileInput">

<button onclick="sendFile()">Определить крепеж</button>

<p id="status"></p>

<div id="result" style="
text-align: left;
margin-top: 10px;
line-height: 1.6;
font-size: 14px;
"></div>

<p style="color:#aaa; font-size:14px;">
💡 Добавьте монету или линейку для точности
</p>

</div>

<script>
async function sendFile() {
    const input = document.getElementById("fileInput");
    const file = input.files[0];

    if (!file) return alert("Выберите файл");

    // 🔥 ЛИМИТ 5 МБ
    if (file.size > 5 * 1024 * 1024) {
        return alert("Файл слишком большой (макс 5 МБ)");
    }

    // 🔥 ТОЛЬКО КАРТИНКИ
    if (!file.type.startsWith("image/")) {
        return alert("Только изображения");
    }

    document.getElementById("status").innerText = "Отправка...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        const text = data.result //"";

        const formatted = text
            .replace("Тип:", "<b>Тип:</b>")
            .replace("Размер:", "<b>Размер:</b>")
            .replace("Материал:", "<b>Материал:</b>")
            .replace("Совет:", "<b>Совет:</b>");

    if (!data.result) {
        document.getElementById("result").innerText = "Ошибка сервера";
    } else {
        document.getElementById("result").innerHTML = formatted;
    }           
        document.getElementById("status").innerText = "Готово ✅";

    } catch (e) {
        document.getElementById("status").innerText = "Ошибка сети";
    }
}
</script>

</body>
</html>
""")


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        client_ip = request.client.host
        today = datetime.now().date()

        if client_ip not in limits:
            limits[client_ip] = {"date": today, "count": 0}

        if limits[client_ip]["date"] != today:
            limits[client_ip] = {"date": today, "count": 0}

        if limits[client_ip]["count"] >= 20:
            return {"result": "Лимит 20 запросов в день достигнут"}

        limits[client_ip]["count"] += 1  

        contents = await file.read()

        image_base64 = base64.b64encode(contents).decode("utf-8")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """Определи крепеж по фото и ответь строго в формате:

Тип: ...
Размер: ...
Материал: ...
Совет: ...

Пиши кратко, без лишнего текста."""
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }]
        )

        result_text = response.output_text

        history.append(result_text)

        return {"result": result_text}

        entry = {
           "time": str(datetime.now()),
           "ip": client_ip,
           "result": result_text
        }

        with open("history.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    except Exception as e:
        return {"result": f"Ошибка: {str(e)}"}

    @app.get("/history")
    def get_history():
        return history