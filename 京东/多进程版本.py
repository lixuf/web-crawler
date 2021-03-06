from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.phantomjs.webdriver import WebDriver
import json
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from random import randint
from multiprocessing import Semaphore,Process
import re
import os

def get_cookie():
	options=webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2,'profile.default_content_setting_values' :  { 'notifications' : 2  }}
	options.add_experimental_option("prefs", prefs)
	user_ag='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
	options.add_argument('--user-agent=%s'%user_ag)
	options.add_argument('--disable-infobars')
	options.add_argument('--disable-gpu') 
	options.add_argument('--incognito')
	#options.add_argument('--headless')
	driver = webdriver.Chrome(chrome_options=options)
	driver.get('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F')
	try:
		result=WebDriverWait(driver,100).until(EC.title_is('京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！'))
	except:
		print("no!!")

	cookies=driver.get_cookies()
	cookies=json.dumps(cookies)
	with open("cookies.json","w") as fbb:
			json.dump(cookies,fbb)

sem_all_html=Semaphore(1)
sem_end=Semaphore(0)
sem_url=Semaphore(0)
sem_cook=Semaphore(1)
class acq_url(Process):
	def __init__(self):
		super(acq_html,self).__init__()
	def run(self):
		options=webdriver.ChromeOptions()
		prefs = {"profile.managed_default_content_settings.images": 2,'profile.default_content_setting_values' :  { 'notifications' : 2  }}
		options.add_experimental_option("prefs", prefs)
		user_ag='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
		options.add_argument('--user-agent=%s'%user_ag)
		options.add_argument('--disable-infobars')
		options.add_argument('--disable-gpu') 
		options.add_argument('--incognito')
		#options.add_argument('--headless')
		page_num=10
		driver = webdriver.Chrome(chrome_options=options)
		sem_cook.acquire()
		with open("cookies.json","r") as f:
			cookies=json.loads(json.load(f))
		sem_cook.release()
		driver.get("https://www.jd.com")
		driver.delete_all_cookies()
		for cookie in cookies:
			driver.add_cookie(cookie)
		sleep(0.5)
		driver.find_element_by_xpath('//*[@id="key"]').send_keys('蓝牙键盘')
		sleep(2)
		driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
		ac=ActionChains(driver)
		for i1 in range(page_num):
			for i in range(4):
				sleep(randint(0,3))
				ac.send_keys(Keys.PAGE_DOWN).perform()
				print(i)
	
			sleep(randint(3,5))

			with open("page_"+str(i1)+'.html','wb') as f:
				f.write(driver.page_source.encode("utf-8","ignore"))
			sem_url.release()
			print("写入成功",i1)
			sleep(randint(5,8))
			ac.send_keys(Keys.RIGHT).perform()

class acq_html(Process):
	def __init__(self):
		super(acq_data,self).__init__()
	
	def run(self):
		options=webdriver.ChromeOptions()
		prefs = {"profile.managed_default_content_settings.images": 2,'profile.default_content_setting_values' :  { 'notifications' : 2  }}
		options.add_experimental_option("prefs", prefs)
		user_ag='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
		options.add_argument('--user-agent=%s'%user_ag)
		options.add_argument('--disable-infobars')
		options.add_argument('--disable-gpu') 
		options.add_argument('--incognito')
		#options.add_argument('--headless')
		driver = webdriver.Chrome(chrome_options=options)
		sem_cook.acquire()
		with open("cookies.json","r") as f:
			cookies=json.loads(json.load(f))
		sem_cook.release()
		driver.get("https://www.jd.com")
		driver.delete_all_cookies()
		for cookie in cookies:
			driver.add_cookie(cookie)
		ac=ActionChains(driver)
		for i in range(10):
			sem_url.acquire()
			with open("page_"+str(i)+".html",'rb') as f:
				text=bs(f.read(),'html.parser')
			lianjie=[]
			for link in text.find_all('strong'):
				for lin in link.find_all('a'):
					try:
						lianjie.append("https:"+lin.get("href"))
					except:
						print("null")
			for ind,t in enumerate(lianjie):
				print(t)
				driver.get(t)
				page_all=-1
				for index in range(2,7):
					sleep(randint(0,2))
					for n in range (randint(2,4)):
						ac.send_keys(Keys.PAGE_DOWN).perform()
						sleep(randint(0,3))
					#if page_all==-1:
						#cc=driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[3]/div[2]/div[2]/div[1]/ul/li[1]/a/em').text
						#cc=driver.find_elements_by_css_selector("[data-anchor='#comment']")
						#cc=driver.find_elements_by_link_text('商品评价')
						#all_num=cc.text
					sem_all_html.acquire()
					with open("all.html",'ab') as f:
						f.write(driver.page_source.encode("utf-8","ignore"))
					sem_all_html.release()
					if sem_end.get_value()<0:
						sem_end.release()
					print("save!!")
					sleep(randint(5,8))
					flag=-1
					for indx,ele in enumerate(driver.find_elements_by_link_text(str(index))):
				
						tx = ele.get_attribute("rel")
			
				
						try:
							if tx==str(index):
								print("ins")
								flag=1
								ele.click()
						except:
							print("ee",indx)
				
					if flag==-1:
						break
		sem_end.release()
		sem_end.release()
		sem_end.release()
class acq_data(Process):
	def __init__(self):
		super(acq_data,self).__init__()
	
	def run(self):
		commit=[]
		while sem_end.get_value()==0:
			if os.path.exists("all.html"):
				print("存在")
				sem_all_html.acquire()
				with open("all.html",'rb') as f:
					gg=f.read().split(b'<html')
				print("删除")
				os.remove("all.html")
				sem_all_html.release()
				print(len(gg),"gg")
				for ins in gg:
					soup=bs(ins)
					for i in soup.find_all('p',class_='comment-con'):
						tx=i.get_text()
						print(tx)
						commit.append(tx)
				print("评论数量:",len(commit))
			else:
				sem_end.acquire()
		print("完成")
		with open("all_commit.json",'a',encoding="utf-8") as f2:
			json.dump(json.dumps(commit),f2)


if __name__=="__main__":
	get_cookie()
	p1=acq_url()
	p1.start()
	p2=acq_html()
	p2.start()
	p3=acq_data()
	p3.start()