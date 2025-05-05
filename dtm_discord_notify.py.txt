import requests
import os
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

def get_sales_info():
    url = 'https://www.pluginboutique.com/deals'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    sales = []
    for item in soup.select('.product'):
        title = item.select_one('.product-title').get_text(strip=True)
        link = 'https://www.pluginboutique.com' + item.select_one('a')['href']
        sales.append(f"{title}\n{link}")

    return '\n\n'.join(sales)

def send_discord_notify(message):
    payload = {'content': message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("通知を送信しました！")
    else:
        print("エラーが発生しました:", response.status_code, response.text)

if __name__ == '__main__':
    sales_message = get_sales_info()
    send_discord_notify(f"【今日のDTMセール情報】\n{sales_message}")
