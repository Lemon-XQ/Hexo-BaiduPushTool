# -*- coding:utf-8 -*-
import importlib,sys 
importlib.reload(sys)


import platform
import os
import string
import urllib.request
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

	def hexo(self):
		url = self.blogURL + "/archives"
		user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

		request = urllib.request.Request(url)
		request.add_header('User-Agent',user_agent)
		# request.add_header('Host','')
		request.add_header('Accept','*/*')
		request.add_header('Referer',self.blogURL)
		request.add_header('GET',url)

		mypage = urllib.request.urlopen(request).read()
		pageNum = self.pageCount(mypage)
		self.findData(self.blogURL,pageNum)

	def pageCount(self,mypage):		
		pattern = re.compile(u'<a class="page-number" href="/archives/page/(\d+?)/">',re.S)
		mypage = mypage.decode('utf-8')#python3
		result = pattern.findall(mypage)

		if(result):
			pageNum = int(result[-1])
		else:
			pageNum = 1 # if there is only one page, url is /archives instead of /archives/page/1

		print("[+] PageCount : ",pageNum)

		return pageNum

	def findData(self,blogurl,pageNum):
		file = open('urls.txt','wb+') # Write into urls.txt
		articleCount = 0

		for i in range(1,pageNum+1):
			print("[+] Reading Page",i)

			if(i == 1):
				url = blogurl + "/archives"
			else:
				url = blogurl + "/archives/page/" +str(i)
			
			user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

			request = urllib.request.Request(url)
			request.add_header('User-Agent',user_agent)
			# request.add_header('Host','')
			request.add_header('Accept','*/*')
			request.add_header('Referer',url)
			request.add_header('GET',url)

			mypage = urllib.request.urlopen(request).read().decode("utf-8")

			articleUrls = re.findall(themeTags[self.blogTheme],mypage,re.S)

			if(articleUrls):
				for articleUrl in articleUrls:
					if(type(articleUrl) == tuple):
						_articleUrl = articleUrl[0] 
						self.datas.append(self.blogURL + _articleUrl + "\n")
						print(_articleUrl.encode('utf-8').decode('utf-8'))
					else:
						self.datas.append(self.blogURL + articleUrl + "\n")
						if(platform.system() =="Windows"):
						    print(articleUrl.encode('utf-8').decode('utf-8'))
						elif(platform.system() == "Linux"):
						    print(articleUrl.encode('utf-8'))
					articleCount = articleCount + 1
					
			else:
				continue

		for data in self.datas:
			file.write(data.encode('utf-8'))
		file.close()

		print('[+] Generate urls.txt Success! Total Records: ',articleCount)

# URL Fromat Check
def checkURLValid(url):
	# Begin with http or https, like http://lemonxq.cn
	result = re.search('https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9]+)+$',url)
	if(result):
		return True
	else:
		return False

# Read infos from _urlconfig.yml
file = open('_urlconfig.yml','r')
config = yaml.load(file)
url = config['URL']
theme = config['Theme']
api = config['API']
curl_cmd = "curl -H 'Content-Type:text/plain' --data-binary @urls.txt " + "\"" + str(api) + "\""

if(checkURLValid(url) and api != None):
	spider = BlogURLSpider(url,theme)
	spider.hexo()
	print('[+] Begin pushing urls to baidu...')
	os.system(curl_cmd)
	print('\n[+] Push Complete')
else:
	print("[-] Please input your infos in _urlconfig.yml ")

