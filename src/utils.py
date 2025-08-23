import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

ERROR_LOAD_PAGE = 'Возникла ошибка при загрузке страницы {url}: {error}'
ERROR_TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding: str = 'utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        response.raise_for_status()  # проверка кода ответа
        return response
    except RequestException as e:
        logging.error(f'Не удалось загрузить страницу {url}: {e}')
        return None


def find_tag(soup, tag, attrs=None):
    search_attrs = attrs or {}  # для поиска
    searched_tag = soup.find(tag, attrs=search_attrs)
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def fetch_soup(session, link, features='lxml'):
    response = get_response(session, link)
    if response is None:
        logging.warning(f'Не удалось получить страницу {link}')
        return None
    return BeautifulSoup(response.text, features)
