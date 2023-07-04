import os
import pickle
import re
import requests
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv


def create_session():
    try:
        os.remove('session')
    except OSError:
        pass
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
    session = requests.session()
    session.post(f'{os.getenv("PHPBB_BASEURL")}/ucp.php?mode=login', data=data)
    with open('session', 'wb') as f:
        pickle.dump(session.cookies, f)
    return session


def load_session():
    session = requests.session()  # or an existing session

    try:
        f = open('session', 'rb')
        session.cookies.update(pickle.load(f))
        f.close()
    except FileNotFoundError:
        return create_session()
    return session


def get_session():
    session = load_session()
    testee = session.get(f'{os.getenv("PHPBB_BASEURL")}/ucp.php?mode=login')
    if 'Du musst in diesem Forum registriert sein, um dich anmelden zu können.' in testee.text:
        session = create_session()
    return session


def get_mails(session_forum):
    mails = session_forum.get(f'{os.getenv("PHPBB_BASEURL")}/ucp.php?i=pm&folder=inbox')
    soup = BeautifulSoup(mails.text)
    mails = soup.find('ul', {'class': 'topiclist cplist pmlist responsive-show-all two-columns'}).findChildren('li')
    for child in mails:
        x = child.findChildren('div', {'class': 'list-inner'})[0].contents[6]
        topic = child.findChildren('a', {'class': 'topictitle'})[0].contents
        sender = child.findChildren('a', {'class': 'username-coloured'})[0].contents
        print(f'PN von {sender[0]} mit Betreff {topic[0]} am {x}')


def get_ips_of_user(session_forum):
    ips = []
    for i in range(0, 1025, 15):
        ips_page = session_forum.get(f'{os.getenv("PHPBB_BASEURL")}/mcp.php?&f=106&t=78742&p=2512501&i=main&mode=post_details&start_ips={i}')
        soup = BeautifulSoup(ips_page.text)
        ips += soup.findAll('tr', {'class': 'bg1'})
        ips += soup.findAll('tr', {'class': 'bg2'})
    ips_text = []
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    for ip_text in ips:
        ips_text.append(pattern.search(ip_text.text)[0])
    f = open('ip_adresses', 'w+')
    f.writelines(line + '\n' for line in ips_text)
    f.close()




if __name__ == '__main__':
    load_dotenv()
    session_forum = get_session()
    #get_mails(session_forum)
    get_ips_of_user(session_forum)
