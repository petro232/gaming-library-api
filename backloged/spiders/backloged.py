import scrapy
from scrapy_playwright.page import PageMethod
import random 
import os 


base_url=os.path.dirname(os.path.abspath(__file__))




def convert_count(value):
    if not value or value == "NONE":
        return 0
    value = str(value).strip()
    if 'K' in value:
        return int(float(value.replace('K', '')) * 1000)
    try:
        return int(value)
    except:
        return 0


def get_last_page():
    try:
        with open(f"{base_url}/last_page.txt","r") as file:
            return int(file.read().strip())
    except :
        return 0
    
def save_page(page_num):
    with open (f"{base_url}/last_page.txt","w") as file:
        file.write(str(page_num))




class BacklogedSpider(scrapy.Spider):
    name = "backloged"
    allowed_domains = ["backloggd.com"]
    start_urls = ["https://backloggd.com/games/lib/popular/popular?page=1"]
    
    def start_requests(self):
        start_page=get_last_page() + 1
        yield   scrapy.Request(f"https://backloggd.com/games/lib/popular?page={start_page}",meta={"playwright":True,
                                                                 "page_count":start_page,
                                                                  "start_page": start_page,
                                                                 "playwright_page_methods":[PageMethod("wait_for_timeout",random.randint(100,300))
                                                                                            ,PageMethod("evaluate","window.scrollBy(0,1200);")]}
                                                                                           , dont_filter=False,callback=self.parse)


    def parse(self, response):
        page_count=response.meta.get("page_count",1)
        start_page = response.meta.get("start_page", 1)
        elements=response.css("div.card.mx-auto.game-cover.quick-access")
        for x in elements:
            title=x.css("div.game-text-centered::text").get()
            href_title=x.css("a.cover-link::attr(href)").get()
            if href_title:
                yield response.follow(href_title,callback=self.entering_fetsh,meta={"playwright":True,"playwright_context":"default",
                                                                                    "title":title,
                                                                                    "href_title":response.urljoin(href_title),
                                                                                    "start_page": start_page,
                                                                                    "playwright_page_methods":[PageMethod("wait_for_timeout",random.randint(100,250))
                                                                                                               ,PageMethod("evaluate",f"window.scrollBy(0,{random.randint(200,1200)})")]}
                                      )
        save_page(page_count)
        if page_count <  start_page + 4 :
            pagination_link=response.css('nav.pagy.nav a[aria-label="Next"]::attr(href)').get()
            if pagination_link :
                yield response.follow(pagination_link,callback=self.parse,meta={"playwright":True,"playwright_context":"default","page_count":page_count+1,"start_page": start_page,"playwright_page_methods":[PageMethod("evaluate",f"window.scrollBy(0,{random.randint(200,700)})")
                                                                                                                                                    ,PageMethod("wait_for_timeout",random.randint(100,400))]})
    def entering_fetsh(self,response):
        title=response.meta["title"]
        href_title=response.meta["href_title"]


        year=response.xpath("//div[contains(@class, 'col-auto')]//text()[contains(., ', 20')]").get().strip() or "NONE"
        rating=response.css("div.row div.col.mx-auto.game-rating h1::text").get() or "NONE"
        played = response.xpath("normalize-space(//p[contains(@class,'log-counter-stat')])").get()
        playing=response.xpath("//p[contains(., 'Playing')]/ancestor::div[1]/following-sibling::div//p/text()").get() or "NONE"
        backlog=response.xpath("//a[contains(@href, '/backlogs/')]//p[@class='mb-0 log-counter-stat']/text()").get() or "NONE"
        wishlist=wishlist_count = response.xpath("//a[contains(@href, '/wishlists/')]//p[contains(@class, 'log-counter-stat')]/text()").get() or "NONE"
        likes=response.xpath("//a[contains(@href, '/likes/')]//h3/text()").get() or "NONE"
        released = [x.strip() for x in response.css("div.row div.col a[href*='/release_platform']::text").getall()] or []
        post_image=response.css("div.overflow-wrapper img.card-img::attr(src)").get() or "NONE"
        studio_llss=response.xpath("//div[contains(@class,'col-auto')]/a[contains(@href,'/company/')]/text()").getall() or []
        studio = list(dict.fromkeys(studio_llss))
        genres_lss=response.xpath("//span[contains(@class,'game-detail')]/a[contains(@class,'game-details-value')]/text()").getall()
        genres=list(dict.fromkeys(genres_lss))
        story=response.xpath("//div[contains(@id,'collapseSummary')]/p/text()").get()

        yield {
            "title":title,
            "year":year,
            "rating":rating,
            "played":convert_count(played),
            "playing":convert_count(playing),
            "backlog":convert_count(backlog),
            "wishlist":convert_count(wishlist),
            "likes":convert_count(likes),
            "released":released ,
             "url": response.url,
             "post_image":post_image,
             "studio":studio,
             "genres":genres,
             "story":story

        }



