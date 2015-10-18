# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import os
import sys
import datetime

#定义爬虫的业务逻辑实现类
class LinkSpider(BaseSpider):
    name = "link"
    start_urls = []
    neitui_urlpattern = "http://www.neitui.me/?name=neitui&handle=lists&keyword={KEYWORD}&page={CURR_PAGE}"
	#liepin_urlpatten = "http://www.liepin.com/zhaopin/?searchField=1&key={KEYWORD}&pubTime=3curPage={CURR_PAGE}"
		
    def __init__(self):
        self.start_urls = self.set_url()        
        
    #set_url方法动态设定要抓取的链接列表
    def set_url(self):
        url_list = []
        #从配置文件中取出所有的关键字列表，逐个去liepin做检索
        keys = '大数据,hadoop,hive,hbase,spark,storm,sqoop,pig'
        for keyword in keys.split(','):
            #url = self.liepin_urlpatten
			url = self.neitui_urlpattern
			url = url.format(KEYWORD=keyword, CURR_PAGE=1)
			url_list.append(url)
        return url_list
    
    #parse方法从html源代码中解析要抓取的内容
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        pgNum = -1
        position_one_page = 28
        all_position_count = hxs.select('//div[@class="search_results_bar clearfix"]/p/strong/text()').extract()
        #print "all_position_count:" + all_position_count[0]
        pgNum = (int(all_position_count[0]) / position_one_page) + 1
		
        keyword = hxs.select('//input[@name="keyword"]/@value').extract()[0]
        keyword = keyword.encode('utf-8')
		
        #pg_info = hxs.select('//a[@class="last"]/@href').extract()
        #keyword = hxs.select('//input[@name="key"]/@value').extract()[0]
        #keyword = keyword.encode('utf-8')
        # 如果没有找到末页的连接，说明只有一页
        #if (len(pg_info)==0):
        #    pgNum = 1
        #else:
        #    pg_info = pg_info[0]
        #    if (pg_info.find("curPage=")>-1):
        #        pg_info = pg_info.split("curPage=")[1]
        #        pgNum = int(pg_info)

        #根据总页数，拼成分页时使用的url
        i = 1
        #url = self.liepin_urlpatten
        url = self.neitui_urlpattern
        for i in range(pgNum):
            each_url = url.format(KEYWORD=keyword, CURR_PAGE=i)
            #调用分页后的页面
            yield Request(each_url,callback=self.get_joburls_bypage)

    #解析职位检索结果页面上的所有职位的链接，插入表中            
    def get_joburls_bypage(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//div[@class="jobnote clearfix"]/div[@class="jobnote-l"]/a/@href').extract()
        links_jobdate = hxs.select('//div[@class="jobmore display"]/span/text()').extract()
        today = self.getMMDD()
        res_links = []
        for idx,link in enumerate(links):
            if (links_jobdate[idx].find(today) > -1):
                open('../output/link_output/link.txt', 'ab').write('http://www.neitui.me' + link + '\n')

		#links = hxs.select('//ul[@class="sojob-result-list"]/li/a/@href').extract()
        #links_jobdate = hxs.select('//ul[@class="sojob-result-list"]/li/a/dl/dt[@class="date"]/span/text()').extract()
        #today = self.getYYYYMMDD()
        #today2 = self.getYYYYMMDD2()
        # 找到每个职位的发布日期，如果发布日期是当天的，就入库
        #for idx,link in enumerate(links):
            #if (links_jobdate[idx].find(today2)>-1):				
                #open('../output/link_output/link.txt', 'ab').write(link+'\n')

    #得到yyyymmdd格式的当期日期
    def getYYYYMMDD(self):
        return datetime.datetime.now().strftime('%Y%m%d')
						
    #得到yyyy-mm-dd格式的当期日期
    def getYYYYMMDD2(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')
	
    def getMMDD(self):
        return datetime.datetime.now().strftime('%m-%d')
