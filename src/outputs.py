import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    OUTPUT_PRETTY,
    OUTPUT_FILE,
    RESULTS_DIR
)

LOG_FILE_RESULTS_SAVED = 'Файл с результатами был сохранён: {file_path}'
LOG_FILE_TAGS_SAVED = 'Файл с тегами был сохранён: {file_path}'


def pretty_output(results, cli_args=None):
    """Вывод в красивой таблице."""

    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args=None):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    file_path = '{}/{}_{}.csv'.format(
        results_dir,
        cli_args.mode,
        dt.datetime.now().strftime(DATETIME_FORMAT)
    )
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, dialect=csv.unix_dialect).writerows(results)
    logging.info(LOG_FILE_RESULTS_SAVED.format(file_path=file_path))


def default_output(results, cli_args=None):
    for row in results:
        print(*row)


OUTPUT_HANDLERS = {
    OUTPUT_PRETTY: pretty_output,
    OUTPUT_FILE: file_output,
    None: default_output,
}


def control_output(results, cli_args):
    OUTPUT_HANDLERS[cli_args.output](results, cli_args)
