import scrapy


class WhiskeyshopSpider(scrapy.Spider):
    name = 'whiskeyshop'
    allowed_domains = ['whiskeyshop.com.ua']
    start_urls = ['https://whiskeyshop.com.ua/en/']

    def parse(self, response):
        list_category = response.css('#top-menu').css('a::attr(href)').getall()
        for x in list_category:
            yield response.follow(response.urljoin(x), callback=self.parse_category)

    def parse_category(self, response):
        for prod in response.xpath('//*[@id="js-product-list"]/div/article/div//div//div/h3'):
            yield response.follow(response.urljoin(prod.css('a::attr(href)').get()), callback=self.parse_product_page)
        next_page_partial_url = response.xpath('//*[@id="js-product-list-top"]/div/nav/ul').css(
            'a.next.js-search-link::attr(href)').get()
        if next_page_partial_url is not None:
            yield response.follow(next_page_partial_url, callback=self.parse_category)

    def parse_product_page(self, response):
        yield {
            'category_text': response.xpath('//*[@id="wrapper"]/nav/ol').css('span::text').getall(),
            'url': response.url,
            'img': response.xpath('//*[@id="content"]/div/div[1]').css('img::attr(src)').get(),
            'title': response.xpath('//*[@id="main"]/div[1]/div[2]/h1/text()').get(),
            'in_stock': response.xpath('//*[@id="product-availability"]/text()').get(),
            'price': response.css('div.current-price').css('span::text').get(),
        }


