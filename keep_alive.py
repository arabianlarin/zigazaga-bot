import time
import requests

URL = "https://zigazaga-bot.onrender.com"  # your bot's public Render URL

while True:
    try:
        r = requests.get(URL)
        print(f"[PING] {r.status_code} at {time.strftime('%H:%M:%S')}")
    except Exception as e:
        print("Error:", e)
    time.sleep(14 * 60)  # 14 minutes