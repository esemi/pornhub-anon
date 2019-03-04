import os
from pathlib import Path

STOP_TAGS = {
    'cartoon',
    'animation',
    'drawn',
    'hentai'
    'alien',
    '3d',
    'famous',
}

HOME_DIR = Path.home()
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

DOWNLOAD_LOCK = 500
DB_FILE_CACHE_PATH = '/tmp/xvideos.com-db.csv'
DB_FILE_URL = 'https://static-egc.xvideos-cdn.com/xvideos.com-db.csv.zip'
SOURCE_PATH = str(HOME_DIR.joinpath('pornanon-sources'))
FACES_PATH = str(HOME_DIR.joinpath('pornanon-faces'))
TMP_PATH = '/tmp/pornanon'
FIND_LINK_TIMEOUT = 25

HAAR_CASCADE_XML = os.path.join(APP_DIR, 'data', 'haarcascade_frontalface_default.xml')
LBP_CASCADE_XML = os.path.join(APP_DIR, 'data', 'lbpcascade_frontalface_improved.xml')
