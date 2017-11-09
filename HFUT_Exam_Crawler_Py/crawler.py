from lxml.html import fromstring
import sqlite3
import requests
from sqlite3 import IntegrityError


class Exam:
    chapter_range = {
        'mzdsxhzgteshzylltx': range(1, 12 + 1),
        'marxism': range(0, 7 + 1),
        'zgjdsgy': range(1, 7 + 1),
        'sxddxyyfljc': range(0, 8 + 1)
    }
    # 宣城校区
    url = "http://10.111.100.107/exercise/singleChapter.asp?subtable={}&chapter={}&sid={}"
    # 合肥校区？
    # url = "http://222.195.7.159/exercise/singleChapter.asp?subtable={}&chapter={}&sid={}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.75 Safari/537.36 '
    }

    def __init__(self, uid=2016218700):
        self.uid = uid
        self.db = sqlite3.connect('exam.db')
        for table in Exam.chapter_range:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS "{}"(
                [_id] integer PRIMARY KEY AUTOINCREMENT
                ,[type] INTEGER
                ,[subject] VARCHAR(255) COLLATE NOCASE UNIQUE
                ,[a] VARCHAR(200) COLLATE NOCASE
                ,[b] VARCHAR(200) COLLATE NOCASE
                ,[c] VARCHAR(200) COLLATE NOCASE
                ,[d] VARCHAR(200) COLLATE NOCASE
                ,[answer] VARCHAR(200) COLLATE NOCASE
                ,[chapter] VARCHAR(200) COLLATE NOCASE
                ,[collection] integer COLLATE NOCASE
                ,[myAnswer] varchar(200) COLLATE NOCASE
                );
            '''.format(table))

    def crawler(self):
        # 爬取题库并存储至sqlite数据库
        for subject in Exam.chapter_range:
            for chapter in Exam.chapter_range[subject]:
                retry_times = 0
                ques_count = 0
                while retry_times < 20:
                    cur_ques_count = len(self.db.execute('select * from {}'.format(subject)).fetchall())
                    if cur_ques_count != ques_count:
                        retry_times = 0
                        ques_count = cur_ques_count
                        print('{}已抓取'.format(subject), ques_count, '条，第 {}'.format(chapter), '章')
                    else:
                        retry_times += 1

                    if subject == 'mzdsxhzgteshzylltx':
                        if chapter > 7:
                            r = requests.get(Exam.url.format(subject + '2', chapter - 7, self.uid), headers=Exam.headers)
                        else:
                            r = requests.get(Exam.url.format(subject + '1', chapter, self.uid), headers=Exam.headers)
                    else:
                        r = requests.get(Exam.url.format(subject, chapter, self.uid), headers=Exam.headers)

                    r.encoding = 'gbk'
                    html = r.text
                    root = fromstring(html)

                    questions = [q.value for q in root.cssselect('input[id^="question"]')]
                    ans = [a.value for a in root.cssselect('input[id^="answer"]')]
                    for qid, (question, ans) in enumerate(zip(questions, ans)):
                        data = {
                            'chapter': str(chapter),
                            'question': question,  # 题目
                            'answer': ans,
                            'a': str(),
                            'b': str(),
                            'c': str(),
                            'd': str(),
                        }
                        # 1判断 2单选 3多选
                        data['answer'] = data['answer'].replace('O', '0')
                        data['type'] = 1 if data['answer'] in '01' else \
                                       2 if len(data['answer']) == 1 else 3

                        try:
                            if data['type'] != 1:  # 选择题
                                for s in list('abcd'):
                                    data[s] = root.cssselect('input[id$="{}{}"]'.format(s, qid + 1))[0].value
                                self.db.execute("INSERT INTO {} (type, subject, a, b, c, d, answer, chapter) VALUES ("
                                                "?, ?, ?, ?, ?, ?, ?, ?) ".format(subject),
                                                (data['type'], data['question'],
                                                 data['a'], data['b'], data['c'], data['d'],
                                                 data['answer'], data['chapter']))
                            else:
                                self.db.execute(
                                    'INSERT INTO {} (type, subject, a, b, c, d, answer, chapter) VALUES (?, ?, NULL, '
                                    'NULL, NULL, NULL, ?, ?)'.format(subject),
                                    (data['type'], data['question'],
                                     data['answer'], data['chapter']))
                        except IntegrityError:
                            pass

                print('{}已抓取'.format(subject), ques_count, '条')

        self.db.commit()


if __name__ == '__main__':
    exam = Exam()
    exam.crawler()