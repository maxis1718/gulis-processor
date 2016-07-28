from nose.tools import *
from gulis import utils
from lxml import etree, html

# gulis.utils.get_element_text

def setup_func():
    "set up test fixtures"

def teardown_func():
    "tear down test fixtures"

@with_setup(setup_func, teardown_func)
def test_get_page_url():
    link = '../data/list/index1217.html'
    assert utils.get_page_url(link) == 'index1217.html'

def test_get_element_attr_with_attr():
    dom = html.fromstring('<a href="/foo/bar">some text</a>')
    assert utils.get_element_attr(dom, attr='href', default='') == '/foo/bar'

def test_get_element_attr_without_attr():
    dom = html.fromstring('<a>some text</a>')
    assert utils.get_element_attr(dom, attr='href', default='') == ''

def test_get_element_attr_with_attr():
    dom = html.fromstring('<a href="/foo/bar">some text</a>')
    assert utils.get_element_attr(dom, attr='href', default='') == '/foo/bar'

def test_get_element_text_with_text():
    dom = html.fromstring('<a href="/foo/bar">some text</a>')
    assert utils.get_element_text(dom, default='') == 'some text'

def test_get_element_text_without_text():
    dom = html.fromstring('<a href="/foo/bar"></a>')
    assert utils.get_element_text(dom, default='') == ''

def test_get_element_content():
    dom = html.fromstring('<a href="/foo/bar">some text</a>')
    assert utils.get_element_content(dom, attr='href') == '/foo/bar'
    assert utils.get_element_content(dom, attr='') == 'some text'
    assert utils.get_element_content(dom) == 'some text'
