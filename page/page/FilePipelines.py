# encoding: utf-8
import sys
import traceback
import datetime
sys.path.append("../../../")

class PagePipeline(object):
    
    #把解析后的内容放入文件中
    def process_item(self, item, spider):
        #fname =  '/home/feigu/liepin-demo/output/page_output/' + item['file_id'] + '.txt'
        fname =  'd:/neituiwang/output/page_output/' + item['file_id'] + '.txt'
        try:
            outfile = open(fname, 'wb')
            outfile.write(item['web_id']+self.getJobFieldSpt()+'03'+self.getJobFieldSpt()+item['job_url']+self.getJobFieldSpt()+item['job_name']+self.getJobFieldSpt()+item['job_location']+self.getJobFieldSpt()+item['job_desc']+self.getJobFieldSpt()+item['edu']+self.getJobFieldSpt()+item['gender']+self.getJobFieldSpt()+item['language']+self.getJobFieldSpt()+item['major']+self.getJobFieldSpt()+item['work_years']+self.getJobFieldSpt()+item['salary']+self.getJobFieldSpt()+item['company_name']+self.getJobFieldSpt()+item['company_desc']+self.getJobFieldSpt()+item['company_address']+self.getJobFieldSpt()+item['company_worktype']+self.getJobFieldSpt()+item['company_scale']+self.getJobFieldSpt()+item['company_prop']+self.getJobFieldSpt()+item['company_website']+self.getJobFieldSpt()+self.getCurrentTimestamp())
        except Exception as e:
            print "ERROR GEN FILE!! >>> " + fname
            print traceback.format_exc()

    def getCurrentTimestamp(self):
	# 得到时间戳
	    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getJobFieldSpt(self):
	#得到生成的职位文件字段间的分隔符。使用ascii码1，和hive中默认的分隔符相同        
	    return chr(1)
