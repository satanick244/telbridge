import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8642147238:AAF5NID8XIqrDEKdMGxqVTXizDsmGypJ6cI"
OPENCLAW_WEBHOOK = "https://your-openclaw-gateway.com/webhook"  # 需要替换

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        # 转发到 OpenClaw
        response = requests.post(OPENCLAW_WEBHOOK, json={
            'chat_id': chat_id,
            'text': text
        })
        
        # 获取回复并发送回 Telegram
        if response.status_code == 200:
            reply = response.json().get('text', '收到')
            send_message(chat_id, reply)
    
    return 'OK'

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
