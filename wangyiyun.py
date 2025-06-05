import requests
import json
import pandas as pd
import time

headers = {
    'Referer': 'https://music.163.com/',
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}

song_id = '1403204015'  #换成要爬的那个音乐的id

def get_comments(song_id, limit=1000):
    comments = []
    offset = 0
    total = 0

    while len(comments) < limit:
        url = f'https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit=100&offset={offset}'
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print("请求失败")
            break

        data = res.json()
        new_comments = data['comments']
        total = data.get('total', 0)
        if not new_comments:
            break

        for c in new_comments:
            comments.append({
                'user': c['user']['nickname'],
                'comment': c['content'],
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(c['time'] // 1000)),
                'like': c['likedCount']
            })

        offset += 100
        time.sleep(0.3)  # 防止封IP

    return pd.DataFrame(comments)

# 执行爬取
df = get_comments(song_id, limit=1200)
df.to_csv('Comments.csv', index=False, encoding='utf-8-sig')
print(f"共爬取评论数: {len(df)}")
