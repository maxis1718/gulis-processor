# coding: utf-8

import requests

def crawl(url):
    """
    article list > https://www.ptt.cc/bbs/Beauty/index1700.html
    article > https://www.ptt.cc/bbs/Beauty/M.1453477203.A.D04.html
    """
    res = requests.get(url)
    return res.text

def get_page_url(link):
    return link.split('/')[-1]

def get_element_attr(element, attr, default=''):
    """
    Return the attr of an html element

    element: HtmlElement
    attr: the filed of element.attrib
    default: the default attr when the element is None
    """
    return element is not None and attr in element.attrib and element.attrib[attr] or default

def get_element_text(element, default=''):
    """
    Return the text content of an html element

    element: HtmlElement
    default: the default text when the element is None
    """
    return element is not None and element.text or default

def decorate_strip(f):
    def d_f(*args, **kargs):
        return f(*args, **kargs).strip()
    return d_f

@decorate_strip
def get_element_content(element, attr=False, default=''):
    if not attr or attr is '':
        return get_element_text(element, default=default)
    elif attr:
        return get_element_attr(element, attr=attr, default=default)

