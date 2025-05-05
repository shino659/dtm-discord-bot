import requests
import os
from bs4 import BeautifulSoup
import openai

# OpenAI v1.x クライアント作成
client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Discord Webhook URL
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

def get_plugin_boutique():
    url = 'https://www.pluginboutique.com/deals'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.product'):
        title = item.select_one('.product-title').get_text(strip=True)
        link = 'https://www.pluginboutique.com' + item.select_one('a')['href']
        items.append(f"🔸 {title}\n🔗 {link}\n🌍 Plugin Boutique")
    return "\n\n".join(items) if items else "Plugin Boutique情報なし"

def get_waves():
    url = 'https://www.waves.com/specials'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.product-name'):
        title = item.get_text(strip=True)
        items.append(f"🔹 {title}\n🔗 https://www.waves.com/specials\n🌍 Waves")
    return "\n\n".join(items) if items else "Waves情報なし"

def get_native_instruments():
    url = 'https://www.native-instruments.com/en/specials/komplete/summer-of-sound-2024/'
    res = requests.get(url)
    if res.status_code == 200:
        return f"🔶 Native Instruments Summer of Sound セール\n🔗 {url}\n🌍 NI最大50%オフ、KOMPLETE, MASCHINE, KONTAKTなど注目！"
    else:
        return "Native Instruments情報取得失敗"

def get_sonicwire():
    url = 'https://sonicwire.com/sale'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.saleItemTitle'):
        title = item.get_text(strip=True)
        link = 'https://sonicwire.com' + item.get('href', '')
        items.append(f"🇯🇵 {title}\n🔗 {link}\n🌍 SONICWIRE")
    return "\n\n".join(items) if items else "SONICWIRE情報なし"

def get_hookup():
    url = 'https://hookup.co.jp/products/sale'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.product-list-title'):
        title = item.get_text(strip=True)
        link = item.get('href', '')
        items.append(f"🇯🇵 {title}\n🔗 {link}\n🌍 Hookup")
    return "\n\n".join(items) if items else "Hookup情報なし"

def get_splice():
    url = 'https://splice.com/sounds/packs'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.soundpack-title'):
        title = item.get_text(strip=True)
        link = 'https://splice.com' + item.get('href', '')
        items.append(f"🎧 {title}\n🔗 {link}\n🌍 Splice")
    return "\n\n".join(items) if items else "Splice情報なし"

def get_loopmasters():
    url = 'https://www.loopmasters.com/sales'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    for item in soup.select('.product-title'):
        title = item.get_text(strip=True)
        link = 'https://www.loopmasters.com' + item.get('href', '')
        items.append(f"🎼 {title}\n🔗 {link}\n🌍 Loopmasters")
    return "\n\n".join(items) if items else "Loopmasters情報なし"

def rank_with_chatgpt(all_products):
    prompt = (
        "以下のDTM製品リストから特に注目・おすすめ・人気のものに⭐をつけ、"
        "上位3つをランキング形式でまとめてください：\n\n" + all_products
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def send_discord_notify(message):
    payload = {'content': message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("通知を送信しました！")
    else:
        print(f"エラー: {response.status_code}\n{response.text}")

if __name__ == '__main__':
    sections = [
        get_plugin_boutique(),
        get_waves(),
        get_native_instruments(),
        get_sonicwire(),
        get_hookup(),
        get_splice(),
        get_loopmasters()
    ]

    combined_info = "\n\n====================\n\n".join(sections)
    ranking = rank_with_chatgpt(combined_info)

    final_message = f"🎹【今日のDTMセール・新リリースまとめ】🎹\n\n{combined_info}\n\n🔥【注目ランキング】🔥\n{ranking}"
    send_discord_notify(final_message)
