# coding: utf-8

import requests
from urlparse import urljoin
from collections import namedtuple
import json
import bs4
from bs4 import BeautifulSoup
from itertools import izip

def crawl(url):
    """
    article list > https://www.ptt.cc/bbs/Beauty/index1700.html
    article > https://www.ptt.cc/bbs/Beauty/M.1453477203.A.D04.html
    """
    res = requests.get(url)
    return res.text

def get_text(element):
    return element.text.strip()

def collect_raw_meta(soup):
    """
    { 
      '作者': 'gaiaesque (一起來浸水桶吧)',
      '看板': 'Beauty',
      '標題': '[正妹] 平祐奈 甜美正妹',
      '時間': 'Thu Oct 22 22:30:31 2015'
    }
    """
    keys = map(get_text, soup.select('#main-content .article-meta-tag'))
    vals = map(get_text, soup.select('#main-content .article-meta-value'))

    return {} if len(keys) != len(vals) else dict(zip(keys, vals))

def collect_content(soup):
    """
    find and concatenate unwrapped strings
    """
    return ''.join(filter(lambda x:type(x) == bs4.element.NavigableString, soup.select_one('#main-content').contents))

def collect_images(soup, protocol='http'):
    """
    [
        'http://i.imgur.com/ijXPYqV.jpg',
        'http://i.imgur.com/eMwxfm2.jpg',
        'http://i.imgur.com/7zcr6vq.jpg'
    ]
    """
    imgs = soup.select('.richcontent img')
    return map(lambda img: '' if 'src' not in img.attrs else protocol+':'+img.attrs['src'], imgs)

def collect_pushs(soup):
    """
    {
        'content': u'竟然在表特看到',
        'tag': u'推',
        'userid': u'LemonUrsus',
        'ipdatetime': u' 09/01 22:13'
    }
    """
    keys = ('tag', 'userid', 'content', 'ipdatetime')

    tags = map(get_text, soup.select('.push .push-tag'))
    userids = map(get_text, soup.select('.push .push-userid'))
    contents = map(get_text, soup.select('.push .push-content'))
    ipdatetimes = map(get_text, soup.select('.push .push-ipdatetime'))

    return [ dict(zip(keys, push)) for push in izip(tags, userids, contents, ipdatetimes) ]

def collect_raw_post_info_list(soup):
    """
    {
        'author': u'MissBB',
        'date': u' 9/02',
        'link': 'https://www.ptt.cc/bbs/Beauty/M.1409646948.A.F45.html',
        'mark': u'',
        'push': u'21',
        'title': u'[神人] 宮原眼科冰淇淋女孩'
    }
    """
    sections = soup.select('.r-ent')
    keys = ['push', 'mark', 'title', 'date', 'author']
    classNames = ['.nrec', '.mark', '.title a', '.meta .date', '.meta .author']
    post_info_list = []
    for section in sections:
        info = dict(zip(keys, (section.select_one(className).text for className in classNames)))
        info['link'] = urljoin('https://www.ptt.cc', section.select_one('.title a').attrs['href'])

        # artifact
        # TODO: convert date to datetime object
        # TODO: convert mark to boolean
        # TODO: convert push to integer

        post_info_list.append(info)

    return post_info_list

def collect_prev_btn_link(soup):
    prev_btn = soup.select('.btn-group-paging .btn')[2]
    prev_btn_link = urljoin('https://www.ptt.cc', prev_btn.attrs['href'])
    return prev_btn_link

if __name__ == '__main__':

    LOCAL_DUMP = True
    LOCAL_DUMP_PATH = '../data/post/'

    ### process list
    soup = BeautifulSoup(open('../data/list/index1217.html'), 'html')

    raw_post_info_list = collect_raw_post_info_list(soup)
    prev_btn_link = collect_prev_btn_link(soup)

    for raw_post_info in raw_post_info_list:

        link = raw_post_info['link'] # https://www.ptt.cc/bbs/Beauty/M.1409577963.A.997.html

        # if(LOCAL_DUMP) {
        #     path = os.path.join(LOCAL_DUMP_PATH, os.path.split(link)[1])
        #     soup = BeautifulSoup(open(path), 'html')
        # } else {
        #     soup = BeautifulSoup(crawl(link))
        # }

        ### process post
        soup = BeautifulSoup(open('../data/post/M.1409577963.A.997.html'), 'html')

        raw_meta = collect_raw_meta(soup)
        content = collect_content(soup)
        images = collect_images(soup)
        pushes = collect_pushs(soup)

        # print json.dumps(collect_raw_meta(article_tree), indent=2, ensure_ascii=False)
        # print json.dumps(collect_content(article_tree), indent=2, ensure_ascii=False)
        # print json.dumps(collect_images(article_tree), indent=2, ensure_ascii=False)
        # print json.dumps(collect_pushs(article_tree), indent=2, ensure_ascii=False)
