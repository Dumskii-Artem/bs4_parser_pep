# outputs.py
import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, OUTPUT_PRETTY, OUTPUT_FILE

LOG_FILE_RESULTS_SAVED = 'Файл с результатами был сохранён: {file_path}'
LOG_FILE_TAGS_SAVED = 'Файл с тегами был сохранён: {file_path}'

def control_output(results, cli_args):
    handler = OUTPUT_HANDLERS.get(cli_args.output, default_output)
    handler(results, cli_args)


def pretty_output(results, cli_args=None):
    """Вывод в красивой таблице."""

    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args=None):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)

    logging.info(LOG_FILE_RESULTS_SAVED.format(file_path=file_path))


def default_output(results, cli_args=None):
    for row in results:
        print(*row)


OUTPUT_HANDLERS = {
    OUTPUT_PRETTY: pretty_output,
    OUTPUT_FILE: file_output,
}