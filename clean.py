with open("bot.py","r",encoding="utf-8") as f:
    text=f.read()

t=t.replace("\u00A0"," ")

with open("bot.py","w",encoding="utf-8") as f:
    f.write(text)

print("clean ok")