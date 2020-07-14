import frontmatter
import logging
import requests

from flask import current_app, abort, url_for
from mongoengine.errors import ValidationError

from udata.app import cache

log = logging.getLogger(__name__)

PAGE_CACHE_DURATION = 60 * 5  # in seconds
MENU_CACHE_DURATION = 60 * 60  # in seconds


def get_menu_gh_url():
    repo = current_app.config.get('PAGES_GH_REPO_NAME')
    if not repo:
        return
    branch = current_app.config.get('PAGES_REPO_BRANCH', 'master')
    return f'https://api.github.com/repos/{repo}/contents/pages?ref={branch}'


@cache.cached(MENU_CACHE_DURATION)
def get_menu_list(menu):
    """
    Build a menu list from github repo

    This has a double layer of cache:
    - @cache.cached decorator w/ short lived cache for normal operations
    - a long terme cache w/o timeout to be able to always render some content
    """
    cache_key = f'pages-menu-{menu}'
    url = get_menu_gh_url()
    if not url:
        log.warning('No url set for pages')
        return []
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.error(f'Error ({e}) while fetching pages list')
        return cache.get(cache_key) or []
    pages = []
    for page in r.json():
        if page['name'].endswith('.md'):
            try:
                r = requests.get(page['download_url'], timeout=5)
            except requests.exceptions.RequestException as e:
                log.error(f'Error ({e}) while fetching page content for {page["name"]}')
                return cache.get(cache_key) or []
            data = frontmatter.loads(r.text)
            menu_list = data.get('menu', [])
            if menu in menu_list:
                page_url = url_for('gouvfr.show_page', slug=page['name'][:-3], _external=True)
                pages.append((data['title'], page_url))
    cache.set(cache_key, pages)
    return pages


def get_pages_gh_urls(slug):
    repo = current_app.config.get('PAGES_GH_REPO_NAME')
    if not repo:
        abort(404)
    branch = current_app.config.get('PAGES_REPO_BRANCH', 'master')
    raw_url = f'https://raw.githubusercontent.com/{repo}/{branch}/pages/{slug}.md'
    gh_url = f'https://github.com/{repo}/blob/{branch}/pages/{slug}.md'
    return raw_url, gh_url


@cache.cached(PAGE_CACHE_DURATION)
def get_page_content(slug):
    '''
    Get a page content from gh repo (md).

    This has a double layer of cache:
    - @cache.cached decorator w/ short lived cache for normal operations
    - a long terme cache w/o timeout to be able to always render some content
    '''
    cache_key = f'pages-content-{slug}'
    raw_url, gh_url = get_pages_gh_urls(slug)
    try:
        response = requests.get(raw_url, timeout=5)
        # do not cache 404 and forward status code
        if response.status_code == 404:
            abort(404)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.exception(f'Error while getting {slug} page from gh: {e}')
        content = cache.get(cache_key)
    else:
        content = response.text
        cache.set(cache_key, content)
    # no cached version or no content from gh
    if not content:
        log.error(f'No content found inc. from cache for page {slug}')
        abort(503)
    return content, gh_url


def get_object(model, id_or_slug):
    objects = getattr(model, 'objects')
    obj = objects.filter(slug=id_or_slug).first()
    if not obj:
        try:
            obj = objects.filter(id=id_or_slug).first()
        except ValidationError:
            pass
    return obj
