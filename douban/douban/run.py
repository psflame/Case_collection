# from scrapy.cmdline import execute
# execute(["scrapy","crawl","dou_ban"])

import re
pattern = re.compile(r'([a-z]+) ([a-z]+)', re.I)  # re.I 表示忽略大小写
m = pattern.findall('Hello World Wide Web')
print(m[1])