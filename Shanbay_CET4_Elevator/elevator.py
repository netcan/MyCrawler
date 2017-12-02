from functools import wraps

import json
import requests


class Elevator:
    api = 'https://www.shanbay.com/api/v2/elevator'
    rest_url = 'https://rest.shanbay.com/api/v2/elevator'
    login_url = 'https://rest.shanbay.com/api/v1/account/login'
    user_agent = 'bayAgent/1.1 Android/5.1.1 com.shanbay.words/7.9.120 tencent-channel/0 HUAWEI/HUAWEI_M2-A01W ' \
                 'frontend/1.8 api/2.3 '

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers['User-Agent'] = Elevator.user_agent
        self.__logined = False

    def login(self):
        if not self.__logined:
            data = {
                'username': self.username,
                'password': self.password,
                'token': None
            }
            self.session.put(Elevator.login_url, data=data)
            r = json.loads(self.session.put(Elevator.login_url, data=data).text)
            if r['msg'] == 'SUCCESS':
                print('登陆成功')
                self.__logined = True

    def login_required(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            if not self.__logined:
                self.login()
            fun(self, *args, *kwargs)
        return wrapper

    @login_required
    def grammar(self):
        """
        爬取阶梯训练语法部分
        :return:
        """
        grammar_lists = json.loads(self.session.get(Elevator.api + '/parts/bclhtz/stages/').text)['data']
        for id, section in enumerate(grammar_lists):
            content = json.loads(self.session.get(self.rest_url + '/tasks/{}/'.format(section['object_id'])).text)['data']
            print('=====================')
            print(id, section['title'])
            try:
                print(content['intro'])
                print(content['knowledge'])
            except KeyError:
                print('NULL')


