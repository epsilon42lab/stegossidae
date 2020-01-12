stegossidae
===========

Crawler for aquiring covers for HTTP steganographic transport of Stegotorus 

Edit stegossidae/spiders/cover_spider.py and add the name of the website and domain:

allowed_domains = ["website.com"]
start_urls = ["https://www.website.com/"]

then run 

scrapy crawl stego_cover -o /tmp/website.csv -t csv

Then the cover file /tmp/website.csv can be given as an input for cover-list for Stegotorus.
