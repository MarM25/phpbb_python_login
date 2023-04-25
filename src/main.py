import os

import requests
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv


def main():
    login_page = requests.get(f'{os.getenv("PHPBB_BASEURL")}/ucp.php?mode=login').text
    soup = BeautifulSoup(login_page)
    sid = soup.find('input', {'name': 'redirect'}).attrs['value'].replace('./ucp.php?mode=login&sid=', '')
    creation_time = soup.find('input', {'name': 'creation_time'}).attrs['value']
    form_token = soup.find('input', {'name': 'form_token'}).attrs['value']

    data = {
        'username': os.getenv('PHPBB_USERNAME'),
        'password': os.getenv('PHPBB_PASSWORD'),
        'creation_time': creation_time,
        'form_token': form_token,
        'sid': sid,
        'login': 'Anmelden',
    }
    time.sleep(1)
    response = requests.post(f'{os.getenv("PHPBB_BASEURL")}/ucp.php?mode=login', data=data)


if __name__ == '__main__':
    load_dotenv()
    main()
