import scrapy


class RuouSpider(scrapy.Spider):
    name = "ruou"
    allowed_domains = ["grandcru.vn"]
    start_urls = ["https://grandcru.vn/ruou-vang-nhap-khau/"]

    def parse(self, response):
        products = response.css('div.product-small')

        for product in products:
            yield {
                'name': product.css('p a::text').get(),
                'price': product.css('div bdi::text').get(),
                'img': product.css('div.box-image-inner img::attr(src)').get(),
                'url': product.css('a.woocommerce-LoopProduct-link::attr(href)').get(),
                'loai_vang': product.css('li.product-attribute__item.pa_loai-vang .pa-info__value p::text').get(),
                'giong nho':  product.css('li.product-attribute__item.pa_giong-nho .pa-info__value p::text').get(),
                'nong do':  product.css('li.product-attribute__item.pa_nong-do .pa-info__value p::text').get(),
                'dung tich': product.css('li.product-attribute__item.pa_dung-tich .pa-info__value p::text').get(),
                'nien vu': product.css('li.product-attribute__item.pa_nien-vu .pa-info__value p::text').get()
            }
        pass
