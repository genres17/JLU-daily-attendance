import requests
import json
import re
import time
import random
import config
from datetime import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup


class Attendance(object):
    def __init__(self):
        self.login_url = 'https://ehall.jlu.edu.cn/sso/login'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        }
        self.data = {
            'username': config.username,
            'password': config.password,

        }

    def get_cookies(self):
        # 模拟登录，获取用户的cookie
        session = requests.Session()
        session.post(self.login_url, headers=self.headers, data=self.data)
        return session

    def health_info_attendance(self) -> dict:
        session = self.get_cookies()
        # 要拿到开始跳转后真实url地址，需要先拿到一个csrf_token
        response1 = session.get('https://ehall.jlu.edu.cn/infoplus/form/JLDX_YJS_XNYQSB/start', headers=self.headers)
        soup = BeautifulSoup(response1.text, 'lxml')
        csrf_token = soup.find(attrs={'itemscope': 'csrfToken'})['content']
        data1 = {
            'idc': 'JLDX_YJS_XNYQSB',
            'csrfToken': csrf_token,
            'formData': '{"_VAR_URL": "https://ehall.jlu.edu.cn/infoplus/form/JLDX_YJS_XNYQSB/start", "_VAR_URL_Attr": "{}"}',
        }
        self.headers['Referer'] = 'https://ehall.jlu.edu.cn/infoplus/form/JLDX_YJS_XNYQSB/start'
        response2 = session.post('https://ehall.jlu.edu.cn/infoplus/interface/start', headers=self.headers, data=data1)
        target_url = json.loads(response2.text)['entities'][0]
        # 提取stepID
        stepID = re.search(r'https://ehall.jlu.edu.cn/infoplus/form/(\d+)/render', target_url).group(1)
        data2 = {
            'stepId': stepID,
            'instanceId': '',
            'admin': 'false',
            'rand': str(random.random() * 999),
            'width': '1536',
            'lang': 'zh',
            'csrfToken': csrf_token,
        }
        self.headers['Referer'] = target_url
        response3 = session.post('https://ehall.jlu.edu.cn/infoplus/interface/render', headers=self.headers, data=data2)
        individual_info = json.loads(response3.text)['entities'][0]
        if individual_info:
            data3 = {
                'actionId': '1',
                'formData': json.dumps(individual_info['data']),
                'remark': '',
                'rand': str(random.random() * 999),
                'nextUsers': '{}',
                'stepId': stepID,
                'timestamp': int(time.time()),
                'csrfToken': csrf_token,
                'lang': 'zh',
                'boundFields': ','.join(individual_info['fields'].keys())
            }
            response4 = session.post('https://ehall.jlu.edu.cn/infoplus/interface/doAction', headers=self.headers,
                                     data=data3)
            print(response4.text)
            if json.loads(response4.text)['ecode'] != 'SUCCEED':
                raise Exception('The server returned a non-successful status.')
            return {'code': 1, 'info': '提交成功！'}
        else:
            return {'code': 0, 'info': '需要先填写一遍个人信息才能使用的喵QAQ'}

    def do_daily_attendance(self) -> dict:
        session = self.get_cookies()
        # 也是要一开始拿到csrf_token
        start_response = session.get('https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start', headers=self.headers)
        soup = BeautifulSoup(start_response.text, 'lxml')
        csrf_token = soup.find(attrs={'itemscope': 'csrfToken'})['content']
        # print(csrf_token)
        data1 = {
            'idc': 'YJSMRDK',
            'release': '',
            'csrfToken': csrf_token,
            'formData': '{"_VAR_URL":"https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start","_VAR_URL_Attr":"{}"}',
        }
        self.headers['Referer'] = 'Referer: https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
        # 获取表单url，这里可能因为错过打卡时间而出现错误的json数据
        post_response = session.post('https://ehall.jlu.edu.cn/infoplus/interface/start', headers=self.headers,
                                     data=data1)
        print(post_response.text)
        json_info = json.loads(post_response.text)
        if json_info['ecode'] == 'EVENT_CANCELLED':
            return {'code': 0, 'info': '错过了打卡时间喵QAQ'}
        elif json_info['ecode'] == 'SUCCEED':
            target_url = json_info['entities'][0]
            stepID = re.search(r'https://ehall.jlu.edu.cn/infoplus/form/(\d+)/render', target_url).group(1)
            # print(stepID)
            data2 = {
                'stepId': stepID,
                'instanceId': '',
                'admin': 'false',
                'rand': str(random.random() * 999),
                'width': '1536',
                'lang': 'zh',
                'csrfToken': csrf_token,
            }
            self.headers['Referer'] = target_url
            render_response = session.post('https://ehall.jlu.edu.cn/infoplus/interface/render', headers=self.headers,
                                           data=data2)
            user_info = json.loads(render_response.text)['entities'][0]
            if not user_info:
                # 如果没有返回数据，说明表单为空，需要提交一次数据
                user_info['fieldZY'] = config.major
                user_info['fieldSQnj_Name'] = config.grade
                user_info['fieldSQxq_Name'] = config.school_district
                user_info['fieldSQgyl_Name'] = config.department
                user_info['fieldSQqsh'] = config.room_number
                user_info['fieldSQssbs'] = '1'

            if parse('7:00') <= datetime.now() <= parse('8:00'):
                # 早打卡
                user_info['fieldZtw'] = '1'
            elif parse('11:00') <= datetime.now() <= parse('12:00'):
                # 中午打卡
                user_info['fieldZhongtw'] = '1'
            elif parse('17:00') <= datetime.now() <= parse('18:00'):
                # 晚打卡
                user_info['fieldWantw'] = '1'

            data3 = {
                'actionId': '1',
                'formData': json.dumps(user_info['data']),
                'remark': '',
                'rand': str(random.random() * 999),
                'nextUsers': '{}',
                'stepId': stepID,
                'timestamp': int(time.time()),
                'csrfToken': csrf_token,
                'lang': 'zh',
                'boundFields': ','.join(user_info['fields'].keys())
            }
            response4 = session.post('https://ehall.jlu.edu.cn/infoplus/interface/doAction', headers=self.headers,
                                     data=data3)
            print(response4.text)
            if json.loads(response4.text)['ecode'] != 'SUCCEED':
                raise Exception('The server returned a non-successful status.')
            return {'code': 1, 'info': '提交成功！'}


if __name__ == '__main__':
    a = Attendance()
    a.health_info_attendance()
    a.do_daily_attendance()
