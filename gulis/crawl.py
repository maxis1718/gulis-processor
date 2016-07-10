# coding: utf-8

import requests
from lxml import html
from pydash.objects import get
from urlparse import urljoin
from collections import namedtuple
from utils import querySelector, querySelectorAll
# from lxml import etree
# from functional import seq
import utils
import json

InfoField = namedtuple('InfoField', 'name css attr')

def crawl(url):
    """
    article list > https://www.ptt.cc/bbs/Beauty/index1700.html
    article > https://www.ptt.cc/bbs/Beauty/M.1453477203.A.D04.html
    """
    res = requests.get(url)
    return res.text

def load_page(fn):
    """
    article list > dev/index1700.html
    article > dev/M.1453477203.A.D04.html
    """
    with open(fn) as fr:
        text = fr.read()
    return text

def parse_to_tree(text):
    return html.fromstring(text)

def extract_info(tree, fields, cssroot):
    """
    e.g., 
    [{'author': 'princessigot',
      'date': ' 1/22',
      'mark': 'M',
      'push': '爆',
      'title': '[正妹] 華航空姐 笑咪咪'
     },
     ...
    ]
    """

    blocks = querySelectorAll(tree, cssroot)
    return [
        { field.name : utils.get_element_content(querySelector(block, field.css), attr=field.attr)
            for field in fields
        } for block in blocks
    ]


def collect_raw_meta (tree):
    metaKeyXPath = '//span[@class="article-meta-tag"]/text()'
    metaValXPath = '//span[@class="article-meta-value"]/text()'

    keys = tree.xpath(metaKeyXPath)
    vals = tree.xpath(metaValXPath)

    if len(keys) != len(vals):
        return {}
    else:
        '''
        { 
          '作者': 'gaiaesque (一起來浸水桶吧)',
          '看板': 'Beauty',
          '標題': '[正妹] 平祐奈 甜美正妹',
          '時間': 'Thu Oct 22 22:30:31 2015'
        }
        '''
        return dict(zip(keys, vals))

def collect_content (tree):
    # TODO: crop real content
    fields = [
        InfoField('content', '#main-content', '')
    ]
    return extract_info(tree, fields, "#main-container")

def collect_images (tree):
    fields = [
        InfoField('link', 'img', 'src')
    ]
    imgs = extract_info(tree, fields, ".richcontent")
    for obj in imgs:
        obj['link'] = obj['link'].replace('//', 'http://')
    return imgs

def collect_pushs (tree):
    fields = [
        InfoField('tag', '.push-tag', ''),
        InfoField('userid', '.push-userid', ''),
        InfoField('content', '.push-content', ''),
        InfoField('ipdatetime', '.push-ipdatetime', ''),
    ]
    result = extract_info(tree, fields, ".push")
    for push in result:
        push["content"] = push["content"][2:]
    return result


if __name__ == '__main__':

    # get a dom tree
    tree = parse_to_tree(load_page('dev/index1700.html'))

    article_list_fields = [
        InfoField('link',   '.title a',     'href'),
        InfoField('title',  '.title a',     ''),
        InfoField('mark',   '.mark',        ''),
        InfoField('push',   '.nrec span',   ''),
        InfoField('date',   '.meta .date',  ''),
        InfoField('author', '.meta .author','')
    ]

    btn_group_fields = [
        InfoField('prev',   'a.btn:nth-child(3)',  'href')
    ]

    article_info = extract_info(tree, article_list_fields, '.r-ent')

    prevbtn_info = extract_info(tree, btn_group_fields, '.btn-group-paging')

    # 'https://www.ptt.cc/bbs/Beauty/index1701.html'
    prevlink = urljoin('https://www.ptt.cc', get(prevbtn_info, '0.prev'))

    print json.dumps(article_info, indent=2, ensure_ascii=False)
    print prevlink

    # retrieve atricle info
    article_tree = parse_to_tree(load_page('dev/M.1453477203.A.D04.html'))
    print json.dumps(collect_raw_meta(article_tree), indent=2, ensure_ascii=False)
    print json.dumps(collect_content(article_tree), indent=2, ensure_ascii=False)
    print json.dumps(collect_images(article_tree), indent=2, ensure_ascii=False)
    print json.dumps(collect_pushs(article_tree), indent=2, ensure_ascii=False)