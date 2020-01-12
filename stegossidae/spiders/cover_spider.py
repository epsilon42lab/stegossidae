from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from stegossidae.items import StegossidaeItem
import re

class CoverSpider(CrawlSpider):
    name = "stego_cover"
    #allowed_domains = ["www.utoronto.ca"]
    #start_urls = ["http://www.utoronto.ca/"]
    # cover_list_file = "equalit.ie"
    # supported_extension = ["js", "pdf", "swf", "htm", "html", "jpg", "png", "gif"]
    #allowed_domains = ["funnycatpix.com"]
    #start_urls = ["http://www.funnycatpix.com/"]
    #allowed_domains = ["www.puppiesden.com"]
    #start_urls = ["http://www.puppiesden.com/"]
    allowed_domains = ["www.puppiesden.com"]
    start_urls = ["http://www.puppiesden.com/"]

    supported_extension = ["js", "htm", "html", "jpg", "png", "shtml"]
    
    tag_to_dig = [("img", "src"), ("script", "src"), ("a","href")]

    rules = (Rule (SgmlLinkExtractor(),callback="parse_items", follow= True),)
             #allow=("index\d00\.html", ),restrict_xpaths=('//p[@class="nextpage"]',))
    url_disector_regex = re.compile("^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$")
    HOST_FIELD = 3
        
    def parse_items(self, response):
        # import pdb
        # pdb.set_trace()
        #filename = response.url.split("/")[-2]
        #open(filename, 'w').write(response.body)
        #with open(self.cover_list_file, 'a+') as cover_list:
            #cover_list.write(response.url)

            #we are interested in images as well
        cur_page = StegossidaeItem()
        if not self.url_disector_regex.match(response.url).group(self.HOST_FIELD) in self.allowed_domains:
            return [] #we have to ignore cause we don't know what to do with local links

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

                    #if there is no host then we add the host
                    if url[0] == '/' or url.find(':') == -1:
                        url_sep = (url[0] != '/') and "/" or ""
                        url = cur_page["url"][:cur_page["url"].rfind('/')]+url_sep + url
                    else:
                        #we check the if the host is in the allowed domain
                        disected_url = self.url_disector_regex.match(url)
                        if disected_url and not str(disected_url.group(self.HOST_FIELD)) in self.allowed_domains:
                            continue

                    cur_item = StegossidaeItem()
                    cur_item["url"] = url.split('?')[0]
                    items.append(cur_item)

        return (items)
                
