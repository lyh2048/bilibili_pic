import requests
import argparse
import re
import os


# 根据BV号获取视频封面的URL
def get_pic_url(bv):
    url = 'https://www.bilibili.com/video/' + bv
    r = requests.get(url=url)
    html = r.text
    pic_url = re.findall(r'"videoData":\{.*?"pic":"(.*?)".*?\}', html, re.DOTALL)
    if len(pic_url) != 0:
        pic_url = pic_url[0].encode('utf8').decode('unicode_escape')
        print("pic:", pic_url)
        return pic_url
    return ""


# 将视频封面保存到本地
def save_pic(pic_url, bv):
    path = './pic/' + bv
    if not os.path.exists(path):
        os.makedirs(path)
    r = requests.get(pic_url)
    with open(path + '/' + pic_url.split('/')[-1], 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bilibili Pic')
    parser.add_argument('-bv', required=True)
    args = parser.parse_args()
    bv = args.bv
    pic_url = get_pic_url(bv)
    if len(pic_url) != 0:
        save_pic(pic_url, bv)
        print('保存成功')
    else:
        print('error: 无法获取到视频封面的URL')