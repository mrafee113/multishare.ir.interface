import os

MainUrl = 'https://mul.ir/'
PublicTorUrl = 'https://www.mul.ir/torrent/public?'

ROOT_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(ROOT_DIR, 'credentials.ini')
CHROMEDRIVER_PATH = os.path.join(ROOT_DIR, 'chromedriver')
COOKIES_PATH = os.path.join(ROOT_DIR, 'cookies.json')
