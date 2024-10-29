import scrapy


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com/b/Audemars-Piguet-Watches/31387/bn_3007141"]

    def parse(self, response):
        # Lấy thông tin sản phẩm
        products = response.css('li.s-item')

        for product in products:
            yield {
                'name': product.css('a h3::text').get(),
                'price': product.css('.s-item__price::text').get(),
                'shipping': product.css('.s-item__shipping::text').get(),
                'img': product.css('img.s-item__image-img::attr(src)').get(),
                'url': product.css('a.s-item__link::attr(href)').get(),
            }



        # Tìm URL của trang tiếp theo
        next_page = response.css("a.pagination__next::attr(href)").get()

        # Nếu có trang tiếp theo, thực hiện yêu cầu đến trang tiếp theo
        if next_page:
            yield response.follow(next_page, callback=self.parse)
