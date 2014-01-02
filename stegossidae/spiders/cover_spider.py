#from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
#from scrapy.selector import HtmlXPathSelector

from stegossidae.items import StegossidaeItem


class CoverSpider(CrawlSpider):
    name = "stego_cover"
    allowed_domains = ["mit.edu"]
    start_urls = ["http://mit.edu"]
    #cover_list_file = "equalit.ie"
    supported_extension = ["js", "pdf", "swf", "htm", "html", "jpg", "png", "gif"]
    tag_to_dig = [("img", "src"), ("script", "src"), ("a","href")]

    rules = (Rule (SgmlLinkExtractor(),callback="parse_items", follow= True),)
             #allow=("index\d00\.html", ),restrict_xpaths=('//p[@class="nextpage"]',))

    def parse_items(self, response):
        # import pdb
        # pdb.set_trace()
        #filename = response.url.split("/")[-2]
        #open(filename, 'w').write(response.body)
        #with open(self.cover_list_file, 'a+') as cover_list:
            #cover_list.write(response.url)

            #we are interested in images as well
        cur_page = StegossidaeItem()
        cur_page["url"] = response.url
        items = [cur_page]

        sel = Selector(response)
        for cur_tag in self.tag_to_dig:
            taggers = sel.xpath('//'+cur_tag[0])
            for cur_tagger in taggers:
                url = cur_tagger.xpath('@src').extract()
                if (url): #ignoring embeded scripts
                    url = url[0] #assuming there is one url
                    # we don't really need to check for the type as payload scraper will do it
                    #cur_type = url.split(".")[-1]
                    #if cur_type.lower in self.supported_extension or url.find(".") == -1: 
                    #turn relative url to absolute url
                    if url[0] == '/' or url.find(':') == -1:
                        url_sep = (url[0] != '/') and "/" or ""
                        url = cur_page["url"][:cur_page["url"].rfind('/')]+url_sep + url

                    cur_item = StegossidaeItem()
                    cur_item["url"] = url.split('?')[0]
                    items.append(cur_item)

        return (items)
                
