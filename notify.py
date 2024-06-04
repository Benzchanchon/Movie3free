from datetime import datetime
import requests
import schedule
import time

LINE_ACCESS_TOKEN = "BL321rX+ahraG/puP1A+UpOuOo+LJLzoKlxxae7JX2dZVV5wsaECnT5ZEVrlii3AMGq6YDb0psmctdmcWjHNHTopgTBw+oMSL0Gp7zVFUDslUYn8AsqWgmHI5iet9jYXzpLwPLs8tqPwlrpgiVbjOQdB04t89/1O/w1cDnyilFU="
LINE_API_URL = "https://api.line.me/v2/bot/message/broadcast"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
}

payload = {
    "messages": [
        {
            "type": "text",
            "text": "วันเสาร์แล้วมาหาหนังดูกันเถอะ!!"
        }
    ]
}

def send_message():
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    print("Message sent. Response Status Code:", response.status_code)

def check_using():
    return

# Schedule job to run every Saturday at 7 PM
schedule.every().saturday.at("19:00").do(send_message)

# Infinite loop to run the scheduler
try:
    while True:
        schedule.run_pending()
        print(datetime.now())
        time.sleep(50)
except KeyboardInterrupt:
    print("Stopping the scheduler.")
