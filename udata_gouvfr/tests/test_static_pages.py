import pytest
import requests

from flask import url_for

from udata.app import cache
from udata_gouvfr.pages.utils import (
    get_pages_gh_urls,
    get_menu_list,
    get_menu_gh_url,
)
from .tests import GouvFrSettings


@pytest.mark.usefixtures('clean_db')
class StaticPagesTest:
    settings = GouvFrSettings
    modules = []

    def test_page_does_not_exist(self, client, rmock):
        raw_url, gh_url = get_pages_gh_urls('doesnotexist')
        rmock.get(raw_url, status_code=404)
        response = client.get(url_for('gouvfr.show_page', slug='doesnotexist'))
        assert response.status_code == 404

    def test_page_error_no_cache(self, client, rmock):
        raw_url, gh_url = get_pages_gh_urls('doesnotexist')
        rmock.get(raw_url, status_code=500)
        response = client.get(url_for('gouvfr.show_page', slug='doesnotexist'))
        assert response.status_code == 503

    def test_page_timeout_no_cache(self, client, rmock):
        raw_url, gh_url = get_pages_gh_urls('doesnotexist')
        rmock.get(raw_url, exc=requests.exceptions.ConnectTimeout)
        response = client.get(url_for('gouvfr.show_page', slug='doesnotexist'))
        assert response.status_code == 503

    def test_page_error_w_cache(self, client, rmock, mocker):
        cache_mock_set = mocker.patch.object(cache, 'set')
        mocker.patch.object(cache, 'get', return_value='dummy_from_cache')
        raw_url, gh_url = get_pages_gh_urls('cache1')
        # fill cache
        rmock.get(raw_url, text="""#test""")
        response = client.get(url_for('gouvfr.show_page', slug='cache1'))
        assert cache_mock_set.called
        rmock.get(raw_url, status_code=500)
        response = client.get(url_for('gouvfr.show_page', slug='cache1'))
        assert response.status_code == 200
        assert b'dummy_from_cache' in response.data
        assert rmock.call_count == 2

    def test_page(self, client, rmock):
        raw_url, gh_url = get_pages_gh_urls('test')
        rmock.get(raw_url, text="""#test""")
        response = client.get(url_for('gouvfr.show_page', slug='test'))
        assert response.status_code == 200
        assert b'<h1>test</h1>' in response.data

    def test_menu(self, client, rmock, mocker):
        cache_mock_set = mocker.patch.object(cache, 'set')
        url = get_menu_gh_url()
        rmock.get(url, json=[{
            'name': 'test.md',
            'download_url': 'https://dl.me/page'
        }])
        rmock.get('https://dl.me/page', text="""---
title: test
menu:
    - footer
---
# test
""")
        menu = get_menu_list('footer')
        assert cache_mock_set.called
        assert rmock.call_count == 2
        assert len(menu) == 1
        assert menu[0][0] == 'test'
        assert menu[0][1] == url_for('gouvfr.show_page', slug='test', _external=True)

    def test_menu_cache_error(self, mocker, rmock):
        url = get_menu_gh_url()
        mocker.patch.object(cache, 'get', return_value=['dummy_from_cache'])
        rmock.get(url, status_code=500)
        menu = get_menu_list('footer')
        assert rmock.call_count == 1
        assert len(menu) == 1
        assert menu[0] == 'dummy_from_cache'

    def test_menu_cache_timeout(self, mocker, rmock):
        url = get_menu_gh_url()
        mocker.patch.object(cache, 'get', return_value=['dummy_from_cache'])

        # timeout when fetching list
        rmock.get(url, exc=requests.exceptions.ConnectTimeout)
        menu = get_menu_list('footer')
        assert len(menu) == 1
        assert menu[0] == 'dummy_from_cache'

        # timeout when fetching page content
        rmock.get(url, json=[{
            'name': 'test.md',
            'download_url': 'https://dl.me/page'
        }])
        rmock.get('https://dl.me/page', exc=requests.exceptions.ConnectTimeout)
        menu = get_menu_list('footer')
        assert len(menu) == 1
        assert menu[0] == 'dummy_from_cache'
