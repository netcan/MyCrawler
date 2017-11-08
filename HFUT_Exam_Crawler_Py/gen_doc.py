import sqlite3
from DESCipher import DESCipher
from collections import namedtuple
import os


def gen_doc(db_name='exam_somarx.db', password=None):
    if not os.path.exists('output'):
        os.mkdir('output')
    cipher = DESCipher(password) if password else None
    db = sqlite3.connect(db_name)
    courses = ['mzdsxhzgteshzylltx', 'marxism', 'zgjdsgy', 'sxddxyyfljc']
    # 没有方法的类，只有属性
    Question = namedtuple('Question', ['chapter', 'type', 'subject', 'a', 'b', 'c', 'd', 'e', 'answer'])
    sql = 'SELECT chapter, type, subject, a, b, c, d, e, answer FROM {} ORDER BY ABS(chapter), ABS(type);'
    types = [None, '判断题', '单选题', '多选题']
    for course in courses:
        md = ''
        qs = [Question(*q) for q in
              db.execute(sql.format(course)).fetchall()]
        chapter = -1
        tye = -1

        for q in qs:
            if chapter != int(q.chapter):
                chapter = int(q.chapter)
                md += '## 第 {} 章\n'.format(chapter)
            if tye != q.type:
                tye = q.type
                md += '\n### {}\n'.format(types[tye])
                qid = 1

            md += "{}. {} **{}**\n".format(qid, (cipher.decrypt(q.subject) if cipher else q.subject).strip(),
                                           q.answer.replace('0', '错').replace('1', '对')
                                           if q.answer in '01' else q.answer)
            # 选择题
            if tye != 1:
                md += '```\n'
                for s in list('abcde'):
                    sel = q._asdict()[s]
                    if sel:
                        md += '{}. {}\n'.format(s.upper(),
                                                (cipher.decrypt(sel) if cipher else sel).strip())
                md += '```\n'
            qid += 1
            with open('output/{}.md'.format(course), 'w') as f:
                f.write(md)

