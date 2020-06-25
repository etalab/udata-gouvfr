import frontmatter
import logging
import requests

from flask import current_app, abort, url_for
from mongoengine.errors import ValidationError

from udata.app import cache, nav

CACHE_DURATION = 300  # in seconds
log = logging.getLogger(__name__)


@cache.cached(CACHE_DURATION)
def get_menu_list(menu):
    """Build a menu list from github repo"""
    repo = current_app.config.get('PAGES_GH_REPO_NAME')
    if not repo:
        return []
    branch = current_app.config.get('PAGES_REPO_BRANCH', 'master')
    url = f'https://api.github.com/repos/{repo}/contents/pages?ref={branch}'
    r = requests.get(url, timeout=5)
    if not r.ok:
        log.error(f'Error ({r.status_code}) while fetching pages list')
        return []
    pages = []
    for page in r.json():
        if page['name'].endswith('.md'):
            r = requests.get(page['download_url'])
            data = frontmatter.loads(r.text)
            menu_list = data.get('menu', [])
            if menu in menu_list:
                page_url = url_for('gouvfr.show_page', slug=page['name'][:-3], _external=True)
                pages.append(nav.Item(data['title'], None, url=page_url))
    return pages


def get_pages_gh_urls(slug):
    repo = current_app.config.get('PAGES_GH_REPO_NAME')
    if not repo:
        abort(404)
    branch = current_app.config.get('PAGES_REPO_BRANCH', 'master')
    raw_url = f'https://raw.githubusercontent.com/{repo}/{branch}/pages/{slug}.md'
    gh_url = f'https://github.com/{repo}/blob/{branch}/pages/{slug}.md'
    return raw_url, gh_url


@cache.cached(CACHE_DURATION)
def get_page_content(slug):
    raw_url, gh_url = get_pages_gh_urls(slug)
    # We let the error appear because:
    # - we dont want to cache false responses
    # - this is only visible on static page
    response = requests.get(raw_url, timeout=5)
    if response.status_code == 404:
        abort(404)
    response.raise_for_status()
    return response.text, gh_url


def get_object(model, id_or_slug):
    objects = getattr(model, 'objects')
    obj = objects.filter(slug=id_or_slug).first()
    if not obj:
        try:
            obj = objects.filter(id=id_or_slug).first()
        except ValidationError:
            pass
    return obj
