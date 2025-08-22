# constants.py
from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
WHATS_NEW_DIR = 'whatsnew/'
DOWNLOADS_FILE_NAME = 'download.html'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_PEP_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

OUTPUT_PRETTY = 'pretty'
OUTPUT_FILE = 'file'

LOG_DIR = BASE_DIR  / 'logs'
LOG_FILE = BASE_DIR  / 'logs/parser.log'
DOWNLOADS_DIR = BASE_DIR / 'downloads'
RESULTS_DIR = BASE_DIR / 'results'