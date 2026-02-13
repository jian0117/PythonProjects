import requests
from bs4 import BeautifulSoup
import ai
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('credentials', 'apiKey')
secret_key = config.get('credentials', 'secretKey')
b = ai.BaiduAI(api_key, secret_key)


# 获取热搜关键词

def crawl_baidu():
    response = requests.get('https://top.baidu.com/board?tab=realtime')
    soup = BeautifulSoup(response.text, 'html.parser')
    record_tags = soup.find_all('div', {'class': 'category-wrap_iQLoo'})
    titles, urls, hot_indices = [], [], []
    for item in record_tags:
        title_tag = item.find('div', {'class': 'c-single-text-ellipsis'})
        url_a = item.find_all('a', {'class': 'img-wrapper_29V76'})
        url = ""
        for a in url_a:
            url = a.get('href')
        hot_index_tag = item.find('div', {'class': 'hot-index_1Bl1a'})
        if (title_tag is not None) and (hot_index_tag is not None) and (urls is not None):
            titles.append(title_tag.text.strip())
            urls.append(url)
            hot_indices.append(hot_index_tag.text.strip())
    titles_and_urls = dict(zip(titles, urls))
    return titles_and_urls


# 发送模型平台生成文章

def create_texts(subject: str):
    texts = b.nlp_poem(subject)
    return texts


# 平台发送文章


# 调试
if __name__ == '__main__':
    poems_d = dict()
    kk = crawl_baidu()
    for k in kk.items():
        print(k)
        # poems_d[k] = create_texts(k)
    # print(poems_d)