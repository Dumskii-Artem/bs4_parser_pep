from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

ERROR_LOAD_PAGE = 'Возникла ошибка при загрузке страницы {url}: {error}'
ERROR_TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding: str = 'utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as e:
        raise ConnectionError(ERROR_LOAD_PAGE.format(url=url, error=e))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def fetch_soup(session, link, features='lxml'):
    return BeautifulSoup(get_response(session, link).text, features)
