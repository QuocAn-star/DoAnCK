import scrapy


class RuouSpider(scrapy.Spider):
    name = "ruou"
    allowed_domains = ["grandcru.vn"]
    start_urls = ["https://grandcru.vn/ruou-vang-nhap-khau/"]

    # Danh sách để lưu các URL sản phẩm đã thu thập
    urls = set()
            #Sử dụng set để lưu trữ các URL duy nhất

    def parse(self, response):
        products = response.css('div.product-small')

        for product in products:
            #Lấy url của sản phảm
            url = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()

            #Kiểm tra xem url đã được thu thập chưa
            if url not in self.urls:
                self.urls.add(url) #Nếu chưa thì thêm vào

                price = product.css('div bdi::text').get()
                if price:
                    price = price.replace('.', '').replace('\xa0', '').strip()  # Loại bỏ ký tự \xa0 và dấu chấm


                yield {
                    'name': product.css('p a::text').get(),
                    'price': price,
                    'img': product.css('div.box-image-inner img::attr(src)').get(),
                    'url': product.css('a.woocommerce-LoopProduct-link::attr(href)').get(),
                    'wine_type': product.css('li.product-attribute__item.pa_loai-vang .pa-info__value p::text').get(),
                    'grape_variety':  product.css('li.product-attribute__item.pa_giong-nho .pa-info__value p::text').get(),
                    'alcohol_concentration':  product.css('li.product-attribute__item.pa_nong-do .pa-info__value p::text').get(),
                    'volume': product.css('li.product-attribute__item.pa_dung-tich .pa-info__value p::text').get(),
                    'vintage': product.css('li.product-attribute__item.pa_nien-vu .pa-info__value p::text').get(),
                }

        #Qua trang tiếp theo để lấy sản phẩm
        next_page = response.css('a.next.page-number::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)



