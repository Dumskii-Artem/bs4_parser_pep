import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    MAIN_DOC_URL,
    WHATS_NEW_DIR,
    DOWNLOADS_FILE_NAME,
    BASE_DIR,
    MAIN_PEP_URL,
    EXPECTED_STATUS
)
from outputs import control_output
from utils import find_tag, get_response

LOG_CMD_ARGS = 'Аргументы командной строки: {args}'
LOG_PARSER_RUNNING = 'Парсер запущен!'
LOG_ARCHIVE_DONE = 'Архив был загружен и сохранён: {archive_file}'
LOG_PARSER_STOPED = 'Парсер завершил работу.'
LOG_UNKNOWN_ERROR = 'Произошла ошибка'
LOG_MISMATCH = 'Несовпадение: {short} -> {full}, ожидалось одно из {expected}'


def fetch_soup(session, link):
    """Делает запрос и возвращает объект BeautifulSoup."""
    response = get_response(session, link)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, WHATS_NEW_DIR)
    sections_by_python = fetch_soup(session, whats_new_url).select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1')

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = fetch_soup(session, version_link)
        results.append(
            (version_link,  find_tag(soup, 'h1').text,
             find_tag(soup, 'dl').text.replace('\n', ' '))
        )
    return results


def latest_versions(session):
    soup = fetch_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise LookupError("Не найден список с версиями Python")

    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return [
        ('Ссылка на документацию', 'Версия', 'Статус'),
        *results.items(),
    ]


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, DOWNLOADS_FILE_NAME)
    soup = fetch_soup(session, downloads_url)
    pdf_a4_link = soup.select_one(
        'table.docutils a[href$="pdf-a4.zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(parents=True, exist_ok=True)
    archive_file = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_file, 'wb') as file:
        file.write(response.content)
    logging.info(LOG_ARCHIVE_DONE.format(archive_file=archive_file))


def pep(session):
    results = []
    parsed_data = []
    soup = fetch_soup(session, MAIN_PEP_URL)
    main_section = find_tag(soup, 'section', {'id': 'index-by-category'})

    sections = main_section.find_all('section')
    for section in sections:
        table_body = find_tag(section, 'tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            td_tags = row.find_all('td')
            if len(td_tags) < 3:
                continue

            status = td_tags[0].text[1:]
            soup = fetch_soup(
                session,
                f'{MAIN_PEP_URL}{td_tags[2].find("a")["href"]}'
            )
            field_table = find_tag(
                soup,
                'dl', {'class': 'field-list'}
            )
            status_dt = field_table.select_one(
                'dt:-soup-contains("Status")')
            status_dd = status_dt.find_next_sibling("dd")
            status_on_page = status_dd.text.strip()
            parsed_data.append((status, status_on_page))
    status_counter = Counter()

    for short, full in parsed_data:
        status_counter[short] += 1
        expected = EXPECTED_STATUS.get(short, ())
        if full not in expected:
            logging.warning(
                LOG_MISMATCH.format(short=short, full=full, expected=expected))

    for code, count in sorted(status_counter.items()):
        code_display = code or "Draft"
        results.append(
            (code_display, count)
        )

    return [
        ('Статус', 'Количество'),
        *results.items(),
        ('Всего', sum(results.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    try:
        configure_logging()
        logging.info(LOG_PARSER_RUNNING)

        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(LOG_CMD_ARGS.format(args=args))

        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)

        logging.info(LOG_PARSER_STOPED)
    except Exception as e:
        logging.exception(LOG_UNKNOWN_ERROR, exc_info=e)
        print(f'{LOG_UNKNOWN_ERROR}: {e}')
        exit(1)


if __name__ == '__main__':
    main()
