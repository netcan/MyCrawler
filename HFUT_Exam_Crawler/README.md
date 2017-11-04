# HFUT_Exam_Crawler
合肥工业大学思政题库爬虫

# 介绍
支持抓取的科目：
* 毛中特
* 思修
* 马克思
* 近代史

# 原理
php使用curl模拟登陆，然后dom分析html抓取至数据库。多进程支持。

# 使用方法：
Linux下执行：
```
# bash ./multi_process.sh
```

参数修改：

如果需要改变抓取的题库，在`crawler.php`中修改参数：
```
/* Subject选项：（抓取的科目）
	毛中特: mzdsxhzgteshzylltx
	马克思: marxism
	近代史: zgjdsgy
	思修: sxddxyyfljc
*/
/* Chapter选项:（对应章节）
	毛中特: 1-12
	马克思: 0-7
	近代史: 1-7
	思修: 0-7
*/

$Options = array(
	'Chapter'=>5,
	'Subject'=>'mzdsxhzgteshzylltx',
	'Uid'=>'2014218000'
);
```

