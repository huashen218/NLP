import re
import scrapy
import pandas as pd

class NLPSpider(scrapy.Spider):
    name = 'nlpspider'
    start_urls = ['https://aclweb.org/anthology/events/acl-2018/']    # set crawled url

    def parse(self, response):
        for link in response.css('a.align-middle::attr(href)').extract():
            if re.match(r'/anthology(.*?)\.bib',link):
                yield scrapy.Request('https://aclweb.org'+link, callback = self.parse2)
            
    def parse2(self, response):
        outname = "./nlpspider_acl2018.csv"    # set output file
        
        try:
            title = re.findall(r'title = "(.*?)",', response.body.decode("utf-8"))[0]
            title = title.replace("{","").replace("}","")
            
            abstract = re.findall(r'abstract = "(.*?)",', response.body.decode("utf-8"))[0]
            abstract = abstract.replace("{","").replace("}","")
            
            index = re.findall(r'url = "https://www.aclweb.org/anthology/P18-(.*?)",', response.body.decode("utf-8"))[0]
            columns = ['title','abstract','index']
            data = pd.DataFrame({"title": [title], "abstract": [abstract], "index": [index]})
            data.to_csv(outname,mode='a',columns=columns,header=False,index=False)
        except:
            pass