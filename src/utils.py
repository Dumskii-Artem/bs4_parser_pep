import logging
from requests import RequestException

from exceptions import ParserFindTagException, ParserRequestException

ERROR_LOAD_PAGE = 'Возникла ошибка при загрузке страницы {url}: {error}'
ERROR_TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'

def get_response(session, url, encoding: str = 'utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as e:
        raise ParserRequestException(
            ERROR_LOAD_PAGE.format(url=url, error=str(e)))


def find_tag(soup, tag, attrs=None):
    search_attrs = attrs or {}  # для поиска
    searched_tag = soup.find(tag, attrs=search_attrs)
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag