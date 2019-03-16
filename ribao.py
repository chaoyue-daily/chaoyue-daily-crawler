#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import re
from bs4 import BeautifulSoup
import pymysql
'''连接数据库'''
# db = pymysql.connect(host='',user='',password='',port=3306)
# cursor = db.cursor()
# data = cursor.fetchone()
# cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET UTF8MB4")
# db.close()

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

def get_article_url(offset):
    '''
    获取专栏链接，标题(日期)
    :param offset: url参数
    '''
    data={
        'include':'data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics',
        'offset':offset,
        'limit':20,
        'sort_by':'created'
    }

    url ='https://www.zhihu.com/api/v4/members/chen-shu-shu-39-66/articles?'

    response = requests.get(url,headers=headers,data=data)
    json_response = json.loads(response.text)
    title = json_response['data']
    for i in title:
        yield {
            "title" : i['title'],
            "zhuanlan_url" : i['url']
        }

def save_article_html(url,title):
    '''
    保存内页数据
    :param url: 文章链接
    :param title: 标题(日期有几个标题和内容对不上->0102..)
    :return:
    '''
    response = requests.get(url,headers=headers).text
    soup = BeautifulSoup(response,'lxml')
    text = soup.find_all(name=['p','ol','noscript','a','h2'])
    '''保存到文件'''
    # for i in text:
    #     i = str(i)
    #     if 'www.zhihu.com/people/chen-shu-shu-39-66' in i or 'aria-label' in i or 'TopicLink' in i:
    #         pass
    #     else:
    #         with open(title+'.html','a+',encoding='utf-8')as f:
    #             #f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'+'\n')
    #             f.write(i+'\n')


if __name__ == '__main__':
    '''翻页启动，没有检查更新'''
    # for i in range(5):
    #     home_page_message = get_article_url(i * 20)
    #     for url in home_page_message:
    #         '''url筛选'''
    #         if re.findall('(超越日报.*?全网要闻)',str(url)):
    #             save_article_html(url['zhuanlan_url'],url['title'])


'''某一天的数据传入url和日期'''
#save_article_html('https://zhuanlan.zhihu.com/p/59170460','0313')