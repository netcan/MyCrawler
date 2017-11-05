from lxml.html import fromstring
import sqlite3
from sqlite3 import IntegrityError


class Exam:
    chapter_range = {
        'mzdsxhzgteshzylltx': (1, 12),
        'marxism': (0, 7),
        'zgjdsgy': (1, 7),
        'sxddxyyfljc': (0, 7)
    }

    def __init__(self, uid=2016218700):
        self.uid = uid
        self.db = sqlite3.connect('exam.db')
        for table in Exam.chapter_range.keys():
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
        html = open('/Users/netcan/Downloads/合肥工业大学在线练习系统.html', 'r', encoding='gbk').read()
        chapter = 0
        subject = 'marxism'
        root = fromstring(html)
        questions = [q.value for q in root.cssselect('input[id^="question"]')]
        ans = [a.value for a in root.cssselect('input[id^="answer"]')]
        for id, (question, ans) in enumerate(zip(questions, ans)):
            data = {
                'chapter': str(chapter),
                'question': question,  # 题目
                'answer': ans,
                'a': str(),
                'b': str(),
                'c': str(),
                'd': str(),
            }
            data['type'] = 1 if data['answer'] in '01' else \
                           2 if len(data['answer']) == 1 else 3

            try:
                if data['type'] != 1:  # 选择题
                    for s in list('abcd'):
                        data[s] = root.cssselect('input[id$="{}{}"]'.format(s, id + 1))[0].value
                    self.db.execute('''
                        INSERT INTO {} (type, subject, a, b, c, d, answer, chapter) 
                                VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")
                    '''.format(subject, data['type'], data['question'],
                               data['a'], data['b'], data['c'], data['d'],
                               data['answer'], chapter))
                else:
                    self.db.execute('''
                        INSERT INTO {} (type, subject, a, b, c, d, answer, chapter) 
                                VALUES ("{}", "{}", NULL, NULL, NULL, NULL, "{}", "{}")
                    '''.format(subject, data['type'], data['question'],
                               data['answer'], chapter))
            except IntegrityError:
                pass

            # print(data)
        print('已抓取', len(self.db.execute('select * from {}'.format(subject)).fetchall()), '条')
        self.db.commit()


if __name__ == '__main__':
    exam = Exam()
    exam.crawler()