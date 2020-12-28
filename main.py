import feedparser
import requests
import time
import os


token = os.getenv('TG_TOKEN')
latest_id = 0

while True:
    feed = feedparser.parse(os.getenv('URL_RSS'))
    feed.entries.reverse()
    with open('data/latest_id.txt', 'r+') as f:
        old_id = int(f.read())
    for entry in feed.entries:
        post_id = int(entry.get("post-id"))
        if post_id <= old_id:
            continue
        title = entry.get("title")
        if not title.startswith("Today’s"):
            continue
        link = entry.get("link")
        latest_id = post_id
        requests.get(f'https://api.telegram.org/bot{token}/sendMessage',
                     params=dict(
                         chat_id=os.getenv('CHANNEL_ID'),
                         parse_mode='Markdown',
                         disable_web_page_preview='True',
                         text=f'[{title[34:]}]({link})'
                     ))

    if latest_id >= old_id:
        with open('data/latest_id.txt', 'r+') as f:
            f.seek(0)
            f.write(str(latest_id))

    time.sleep(3600)
