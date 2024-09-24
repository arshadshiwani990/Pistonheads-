import scrapy
import json

class PistonheadsSpiderSpider(scrapy.Spider):
    name = 'pistonheads_spider'

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.pistonheads.com/buy/search?sort-order=Date',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        for i in range(1, 20):
            
            offset=i

            url='https://www.pistonheads.com/api/graphql?operationName=SearchPage&variables=%7B%22categoryName%22%3A%22used-cars%22%2C%22distance%22%3A%222147483647%22%2C%22sortOption%22%3A%22Date%22%2C%22limit%22%3A18%2C%22offset%22%3A'+str(offset)+'%2C%22numberOfFeaturedAdverts%22%3A0%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229e3c40b5f359003efffcbd77466d299b533400e53fd9656ec47a81ecc584f92a%22%7D%7D'
            yield scrapy.Request(url=url, method="GET", callback=self.scrape_results,headers=self.headers)

    def scrape_results(self, response):
    
        adverts = json.loads(response.text).get('data').get('searchPage').get('adverts')
        for ads in adverts:
            id=ads.get('id')
            url = 'https://www.pistonheads.com/buy/listing/'+str(id)
            yield scrapy.Request(url=url, method="GET", callback=self.parse_page,headers=self.headers)
            
            
    def parse_page(self,response):
        
        phoneNumber=response.xpath('//a[@data-gtm-event-action="form seller phone number click"]/text()').get()
        title=response.xpath('//h1[@class="Heading_root__i6sCL Heading_noMargin__BzMFT Heading_h3__vCOni"]/text()').get()
        
        
        
        print(phoneNumber)
        print(title)
        
        
        item={}
        item['title']=title
        item['phoneNumber']=phoneNumber
        
        yield item