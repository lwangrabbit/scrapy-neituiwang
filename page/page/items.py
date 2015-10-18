# encoding: utf-8

from scrapy.item import Item, Field

#定义存放帖子内容的类
class PageItem(Item):
    #网站标识
    web_id = Field()	#www.neitui.me
    #生成的文件名
    file_id = Field()	#409321
    #职位来源网址
    job_url = Field()	#www.neitui.me/j/409321
    #工作名称
    job_name = Field()	#Hadoop/Spark开发工程师
    #工作地点    
    job_location = Field()	#北京市海淀区上地
    #职位描述 
    job_desc = Field()		#。。。。。。。
    #学历要求   
    edu = Field()			#“”
    #性别要求      
    gender = Field()		#“”
    #语言要求       
    language = Field()		#“”
    #专业要求        
    major = Field()			#“”
    #工作年限    
    work_years = Field()	#3-5年经验
    #薪水范围         
    salary = Field()		#10-20k
    #职位发布时间
    job_datetime = Field()	#10月18日
    #公司名称      
    company_name = Field()	#北京升鑫网络科技有限公司
    #企业介绍
    company_desc = Field()	#最懂互联网企业的安全伙伴
    #公司地址
    company_address = Field() 	#北京市海淀区上地
    #行业
    company_worktype = Field()	#业务领域：企业服务
    #规模
    company_scale = Field()		#公司规模：15-50人
    #性质
    company_prop = Field()		#“”
    #网址
    company_website = Field()	#主页：
