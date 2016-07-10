# coding: utf-8

from lxml.cssselect import CSSSelector
from pydash.objects import get

def querySelectorAll(tree, css):
    sel = CSSSelector(css)
    return sel(tree)

def querySelector(tree, css):
    doms = querySelectorAll(tree, css)
    return get(doms, 0)

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

