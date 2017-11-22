# -*- coding:utf-8 -*-
import os
import string
import urllib2
import re
import time
import yaml

themeTags = {'Next': u'<a class="post-title-link" href="([^"]*)" itemprop="url">',
			 'Jacman': u'<a.*?href="([^"]*)" title="([^"]*)" itemprop="url".*?>',
			 'Yelee': u'<a.*?class="archive-article-title" href="([^"]*)"',
			 'Apollo': u'<a.*?href="([^"]*)" class="post-title-link.*?>'}

class BlogURLSpider:

	def __init__(self, url,theme):
		self.blogURL = url
		self.blogTheme = theme
		self.datas = []
		print u'爬虫启动……'

	def hexo(self):
		url = self.blogURL + "/archives"
		user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

		request = urllib2.Request(url)
		request.add_header('User-Agent',user_agent)
		# request.add_header('Host','')
		request.add_header('Accept','*/*')
		request.add_header('Referer',self.blogURL)
		request.add_header('GET',url)

		mypage = urllib2.urlopen(request).read()
		pageNum = self.pageCount(mypage)
		self.findData(self.blogURL,pageNum)

	def pageCount(self,mypage):		
		pattern = re.compile(u'<a class="page-number" href="/archives/page/(\d+?)/">',re.S)
		result = pattern.findall(mypage)

		if(result):
			pageNum = int(result[-1])
		else:
			pageNum = 1 # 只有一页时url为/archives，没有page

		print u"[+] Find: 一共 %d 页" % pageNum

		return pageNum

	def findData(self,blogurl,pageNum):
		file = open('urls.txt','w+') # 写入urls.txt文件
		articleCount = 0

		for i in range(1,pageNum+1):
			print u"[+] 爬取第 %d 页中……" % i

			if(i == 1):
				url = blogurl + "/archives"
			else:
				url = blogurl + "/archives/page/" +str(i)
			
			user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

			request = urllib2.Request(url)
			request.add_header('User-Agent',user_agent)
			# request.add_header('Host','')
			request.add_header('Accept','*/*')
			request.add_header('Referer',url)
			request.add_header('GET',url)

			mypage = urllib2.urlopen(request).read().decode("utf-8")

			pattern = re.compile(themeTags[self.blogTheme])
			# articleUrls = pattern.findall(mypage)
			articleUrls = re.findall(themeTags[self.blogTheme],mypage,re.S)

			if(articleUrls):
				for articleUrl in articleUrls:
					# print type(articleUrl)
					if(type(articleUrl) == tuple):
						_articleUrl = articleUrl[0] 
						self.datas.append(self.blogURL + _articleUrl + "\n")
						print _articleUrl
					else:
						self.datas.append(self.blogURL + articleUrl + "\n")
						print articleUrl
					
					articleCount = articleCount + 1
					
			else:
				continue

		for data in self.datas:
			file.write(data.encode('utf-8'))
		file.close()

		print u'[+] 生成 urls.txt 成功！共 %d 条记录' % articleCount

# URL校验
def checkURLValid(url):
	# http或https开头，其后为A.B格式，A可以为-、字母、数字，B为字母、数字
	result = re.search('https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9]+)+$',url)
	if(result):
		return True
	else:
		return False

# 读取配置文件中的博客URL
file = open('_urlconfig.yml','r')
config = yaml.load(file)
url = config['URL']
theme = config['Theme']
api = config['API']
curl_cmd = "curl -H 'Content-Type:text/plain' --data-binary @urls.txt " + "\"" + str(api) + "\""

if(checkURLValid(url) and api != None):
	spider = BlogURLSpider(url,theme)
	spider.hexo()
	print u'[+] 开始主动推送至百度……'
	os.system(curl_cmd)
	print u'\n[+] 推送完成'
else:
	print u"[-] 请在 _urlconfig.yml 中填入相关配置信息"


