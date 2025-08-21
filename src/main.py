import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import MAIN_DOC_URL, WHATS_NEW_DIR, DOWNLOADS_FILE_NAME, \
    BASE_DIR, MAIN_PEP_URL, EXPECTED_STATUS
from configs import configure_argument_parser, configure_logging
from outputs import control_output, save_to_file
from exceptions import ParserFindTagException
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, WHATS_NEW_DIR)
    response = get_response(session, whats_new_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    # main_div = soup.fiind('section', attrs={'id': 'what-s-new-in-python'})
    main_div = find_tag(soup, 'section', {'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', {'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = session.get(version_link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, DOWNLOADS_FILE_NAME)
    response = get_response(session, downloads_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})

    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    print(archive_url)
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')

def pep(session):
    results = []
    results = [('Статус','Количество')]
    parsed_data = []
    response = get_response(session, MAIN_PEP_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    main_section = find_tag(soup, 'section', {'id':'index-by-category'})
    save_to_file(str(main_section),'main_section.html')

    sections = main_section.find_all('section')
    for section in sections:
        try:
            title = find_tag(section, 'h3').text
        except ParserFindTagException as e:
            title = None

        if title:
            table_body = find_tag(section, 'tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                td_tags = row.find_all('td')
                if len(td_tags) < 3:
                    continue

                status = td_tags[0].text[1:]
                link = f'{MAIN_PEP_URL}{td_tags[2].find("a")["href"]}'
                response = get_response(session, link)
                response.encoding = 'utf-8'

                soup = BeautifulSoup(response.text, 'lxml')
                field_table = find_tag(soup, 'dl', {'class':'field-list'})
                status_dt = field_table.select_one('dt:-soup-contains("Status")')
                status_dd = status_dt.find_next_sibling("dd")
                status_on_page = status_dd.text.strip()
                parsed_data.append((status, status_on_page))
    status_counter = Counter()

    for short, full in parsed_data:
        status_counter[short] += 1
        expected = EXPECTED_STATUS.get(short, ())
        if full not in expected:
            print(
                f"Несовпадение: {short} -> {full}, ожидалось одно из {expected}")

    for code, count in sorted(status_counter.items()):
        code_display = code or "Draft"
        results.append(
            (code_display, count)
        )
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
