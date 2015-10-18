# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from page import items
import traceback
import sys
import datetime

#定义要抓取页面的爬虫类
class PageSpider(BaseSpider):
    name = "page"    
    start_urls = []
    
    def __init__(self):        
        self.start_urls = self.set_url()

    #从jobs_task表中读出要抓取的链接列表，放入数组中
    def set_url(self):
        url_list = []
        link_file = open('../output/link_output/link.txt', 'r')
        loops = 0
        for each_link in link_file:
            each_link = each_link.replace('\r','')
            each_link = each_link.replace('\n','')
            url_list.append(each_link)
            loops+=1
            #if (loops == 100):
                #break
        link_file.close()
        url_list = set(url_list)
        return url_list

    def parse(self, response):
        try:            
			#从网址http://www.neitui.me/j/409321中解析出409321作为文件名
            file_id = response.url.split("/")[-1]
            hxs = HtmlXPathSelector(response)
            
            job_name = hxs.select('//div[@class="jobnote"]/strong[@class="padding-r10"]/text()').extract()
            if len(job_name) <= 0:
			    job_name = ""
            else:
                job_name = job_name[0].encode('utf-8')
            
            job_location = hxs.select('//dl[@class="ci_body"]/dd/text()').extract()
            if len(job_location) <= 0:
                job_location = ""
            else:
                job_location = job_location[0].encode('utf-8')
			
            job_desc = hxs.select('//div[@class="jobdetail nooverflow"]').extract()
            if len(job_desc) <= 0:
                job_desc = ""
            else:
                job_desc = job_desc[0].encode('utf-8')
                job_desc = job_desc.split('nooverflow">')[1]
                job_desc = job_desc.split('</div>')[0]
                job_desc = job_desc.strip()
					
            company_name = hxs.select('//div[@class="ci_head clearfix"]/div[@class="c_name"]/a/text()').extract()
            if len(company_name) <= 0:
                company_name = ""
            else:
                company_name = company_name[0].encode('utf-8')
				
            job_datetime = self.getYYYYMMDD()
			
            work_years = hxs.select('//div[@class="jobnote"]/span[@class="padding-r10 experience"]/text()').extract()
            if len(work_years) <= 0:
                work_years = ""			    
            else:
                work_years = work_years[0].encode('utf-8')
				
            edu = ""
            salary = hxs.select('//div[@class="jobnote"]/span[@class="padding-r10 pay"]/text()').extract()
            if len(salary) <= 0:
                salary = ""
            else:
                salary = salary[0].encode('utf-8')

            company_desc = hxs.select('//dl[@class="ci_body"]').extract()
            if len(company_desc) < 3:
                company_desc = ""
            else:
                company_desc = company_desc[2].split('<dd>')[-1].split('</dd>')[0].strip().encode('utf-8')
            			
            company_address = job_location
            company_website = hxs.select('//dl[@class="ci_body"]/dd/a[@href]/text()').extract()[0].encode('utf-8')
			
            language = ""
            
            company_worktype = hxs.select('//dl[@class="ci_body"]').extract()[1]
            company_worktype = company_worktype.split('</dt><dd>')[2].split('</dd><dt>')[0].encode('utf-8')
            
            company_prop = ""
            
            company_scale = hxs.select('//dl[@class="ci_body"]').extract()[1]
            company_scale = company_scale.split('</dt><dd>')[1].split('</dd><dt>')[0].encode('utf-8')
			
            data = items.PageItem()
            data['web_id'] = "www.neitui.me"
            data['file_id'] = file_id
            data['job_url'] = response.url
            data['job_name'] = job_name
            data['job_desc'] = job_desc
            data['gender'] = ""
            data['major'] = ""
            data['company_name'] = company_name
            data['job_datetime'] = job_datetime
            data['job_location'] = job_location
            data['work_years'] = work_years
            data['edu'] = edu
            data['salary'] = salary
            data['company_desc'] = company_desc
            data['company_address'] = company_address
            data['company_website'] = company_website
            data['language'] = language
            data['company_worktype'] = company_worktype
            data['company_prop'] = company_prop
            data['company_scale'] = company_scale
            
            #更新任务表中抓取状态
			#self.jobsTool.updateCrulInfo(ConfigPropObj.liepin_webid, response.url, 1, "")
            return data
        except Exception as e:
            print "ERROR PARSE"
            print response.url
            print traceback.format_exc()
			#self.jobsTool.updateCrulInfo(ConfigPropObj.liepin_webid, response.url, 2, e)

    #得到yyyymmdd格式的当期日期
    def getYYYYMMDD(self):
	    return datetime.datetime.now().strftime('%Y%m%d')
