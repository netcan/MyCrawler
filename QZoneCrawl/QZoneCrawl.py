from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, \
    StaleElementReferenceException, WebDriverException, ElementNotVisibleException
from PIL import Image
from pyzbar import pyzbar
from urllib.request import urlretrieve
from urllib.error import URLError
from functools import wraps
import qrcode, hashlib, os
import socket
from datetime import datetime
import pypandoc


class QZoneCrawl:
    url = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid" \
          "=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912" \
          "&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone" \
          "%26from%3Diqq&pt_qr_app=手机QQ空间&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq" \
          ".com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=0 "

    def __init__(self, qq, timeout=20, save_images=True, driver='Phantomjs'):
        socket.setdefaulttimeout(timeout)
        self.qq = qq
        self.__login = False
        self.save_images = save_images
        self.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/61.0.3163.100 Safari/537.36 '
        self.md = "此({})动态由https://github.com/netcan/QZoneCrawler于{}采集备份，欢迎Star/交流学习，禁止商用。\n\n"
        if driver == 'Phantomjs':
            opt = dict(DesiredCapabilities.PHANTOMJS)
            opt["phantomjs.page.settings.userAgent"] = self.userAgent
            self.driver = webdriver.PhantomJS(desired_capabilities=opt)
        else:
            opt = webdriver.ChromeOptions()
            opt.add_argument("user-agent=" + self.userAgent)
            self.driver = webdriver.Chrome(chrome_options=opt)

    def write_md(feed_info):
        @wraps(feed_info)
        def wrapper(self, *args, **kwargs):
            feed_ifo = feed_info(self, *args, **kwargs)
            self.md += '### ' + feed_ifo['time'] + '\n'
            if feed_ifo['content']:
                self.md += '```' + \
                    feed_ifo['content'] + \
                           '```\n\n'
            for url in feed_ifo['images']:
                filename = 'images/' + hashlib.sha256(url.encode()).hexdigest()
                self.md += '![]({})\n'.format(filename)

            self.md += '\n***\n\n'
            print(feed_ifo['content'])
        return wrapper

    @write_md
    def feed_info(self, feed):
        if not os.path.exists('images'):
            os.mkdir('images')

        feed_ifo = {'content': feed.find_element_by_css_selector('div.bd > pre').text,
                    'time': feed.find_element_by_css_selector('.goDetail').get_attribute('title'),
                    'images': []}
        # 保存图片
        if self.save_images:
            try:
                imgs = feed.find_elements_by_css_selector('.img-attachments-inner.clearfix > a')
            except StaleElementReferenceException:
                imgs = None
            for img in imgs:
                url = img.get_attribute('href')
                feed_ifo['images'].append(url)
                filename = 'images/' + hashlib.sha256(url.encode()).hexdigest()
                if url.startswith('http') and not os.path.exists(filename):
                    try:
                        urlretrieve(url, filename)
                    except (URLError, TimeoutError, socket.timeout):
                        pass
        return feed_ifo

    def login(self):
        # 扫描二维码，跳转到个人主页的说说页面
        self.driver.get(QZoneCrawl.url)
        self.driver.save_screenshot('qrcode.png')
        code = pyzbar.decode(Image.open('qrcode.png'))[0].data
        qrcode.make(code).save('qrcode.png')

        print('请扫描二维码登陆：./qrcode.png')
        try:
            WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pageContent')))
        except TimeoutException:
            print('登陆失败！')
            self.quit()
        else:
            print('登陆成功！')
            self.__login = True

    def login_required(crawl):
        @wraps(crawl)
        def wrapper(self, *args, **kwargs):
            if not self.__login:
                self.login()
            crawl(self, *args, **kwargs)
        return wrapper

    @login_required
    def crawl(self, start_page=1, callback=None):
        # 跳转到说说页面
        print("当前抓取对象：", self.qq)
        self.driver.get('https://user.qzone.qq.com/{}/311'.format(self.qq))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app_canvas_frame')))
        # 获取最大页码数量
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame('app_canvas_frame')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                             'div.box.bgr3 div.bd > pre')))

        while True:
            try:
                feed_pages = int(self.driver.find_element_by_css_selector('a[id^="pager_last"]').text)
                self.driver.find_element_by_css_selector('input[id^="pager_go"]').clear()
                if start_page != 1:
                    self.driver.find_element_by_css_selector('input[id^="pager_go"]').send_keys(start_page)
                    self.driver.find_element_by_css_selector('button[id^="pager_gobtn"]').click()
                lst_feeds = self.driver.find_elements_by_css_selector('div.box.bgr3')
                cur_page = int(self.driver.find_element_by_css_selector('p span.current').text)
            except (NoSuchElementException, WebDriverException):
                self.driver.implicitly_wait(1)
                continue
            else:
                if cur_page == start_page:
                    break

        # 开始爬取说说
        feed_num = 0
        # print(feed_pages)
        while cur_page <= feed_pages:  # <=2调试用
            print("page:", cur_page, '/', feed_pages)
            cur_feeds = self.driver.find_elements_by_css_selector('div.box.bgr3')
            # 刷新当前页面的说说
            while cur_feeds == lst_feeds and cur_page != 1:
                self.driver.implicitly_wait(1)
                cur_feeds = self.driver.find_elements_by_css_selector('div.box.bgr3')

            # 动态封存，跳出
            try:
                if self.driver.find_element_by_css_selector('img.empty_pic_message'):
                    print('动态无法读取，可能已封存，跳出中...')
                    break
            except NoSuchElementException:
                pass

            # 展开说说
            # more = self.driver.find_elements_by_css_selector('div.bd > div.f_toggle > a.has_more_con')
            # for m in more:
            #     if m.text == '展开查看全文':
            #         m.click()

            for feed in cur_feeds:
                print(feed_num)
                callback(feed) if callback else \
                    print(feed.find_element_by_css_selector('div.bd > pre').text)
                feed_num += 1

            # 翻页
            lst_page = cur_page
            if lst_page == feed_pages:
                break
            while True:
                try:
                    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        r'a[id^="pager_next"]')))
                    self.driver.find_element_by_css_selector(r'a[id^="pager_next"]').click()
                    cur_page = int(self.driver.find_element_by_css_selector('p span.current').text)
                except (StaleElementReferenceException, WebDriverException):
                    self.driver.implicitly_wait(1)
                    continue
                else:
                    if lst_page != cur_page:
                        break

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                 'div.box.bgr3 div.bd > pre')))
            lst_feeds = cur_feeds

    def save_feeds(self, fmt='epub'):
        if not os.path.exists('output'):
            os.mkdir('output')

        if self.md:
            pypandoc.convert_text(self.md.format(self.qq, datetime.now().strftime('%F %T')), fmt,
                                  'markdown', outputfile='output/{}.{}'.format(self.qq, fmt))
            # self.md = str()

    def quit(self):
        self.driver.quit()

