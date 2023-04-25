import os

import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

params = {
    'mode': 'login',
}


def main():
    login_page = requests.get(f'{os.getenv("BASEURL")}/ucp.php', params=params).text
    soup = BeautifulSoup(login_page)
    sid_raw = soup.find('input', {'name': 'redirect'}).attrs['value']
    sid = sid_raw.replace('./ucp.php?mode=login&sid=', '')
    creation_time = soup.find('input', {'name': 'creation_time'}).attrs['value']
    form_token = soup.find('input', {'name': 'form_token'}).attrs['value']

    data = {
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'creation_time': creation_time,
        'form_token': form_token,
        'sid': sid,
        'login': 'Anmelden',
    }

    response = requests.post(f'http{os.getenv("BASEURL")}/ucp.php', params=params, data=data)
    # response will show you are logfged in!


if __name__ == '__main__':
    load_dotenv()
    main()
