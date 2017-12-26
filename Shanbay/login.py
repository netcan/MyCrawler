import requests, json


def login(username, password):
    user_agent = 'bayAgent/1.1 Android/5.1.1 com.shanbay.words/7.9.120 tencent-channel/0 HUAWEI/HUAWEI_M2-A01W ' \
                 'frontend/1.8 api/2.3 '
    session = requests.Session()
    session.headers['User-Agent'] = user_agent
    login_url = 'https://rest.shanbay.com/api/v1/account/login'
    data = {
        'username': username,
        'password': password,
        'token': None
    }
    session.put(login_url, data=data)
    r = json.loads(session.put(login_url, data=data).text)
    return session if r['msg'] == 'SUCCESS' else None

