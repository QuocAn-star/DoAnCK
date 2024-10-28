import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.ebay.com/b/Rolex/bn_21834331']

    def parse(self, response):
        self.logger.info("Parsing page: %s", response.url)

        # Trích xuất tất cả các sản phẩm
        
        products = response.xpath("//ul[contains(@class, 'b-list__items_nofooter')]/li[contains(@class, 's-item')]")

        for product in products:
            product_link = product.xpath(".//a[@target='_blank']/@href").get()  # Lấy liên kết đến sản phẩm
            price = product.xpath(".//span[@class= 's-item__price']/text()").get()# Lấy giá sản phẩm
            shipping_info = product.xpath(".//span[@class='s-item__shipping s-item__logisticsCost']/text()").get()  # Lấy thông tin vận chuyển
            quantity = product.xpath(".//span[@class='s-item__hotness s-item__authorized-seller']/span/text()").get()  # Lấy quantity
            bids = product.xpath(".//span[@class='s-item__bids s-item__bidCount']/text()").get()  # Lấy bids
            time_remaining = product.xpath(".//span[@class='s-item__time-left']/text()").get()  # Lấy time remaining

            # In thông tin đã lấy được
            self.logger.info("Found product link: %s", product_link)
            self.logger.info("Price: %s, Shipping: %s, Quantity: %s, Bids: %s, Time Remaining: %s", 
                             price, shipping_info, quantity, bids, time_remaining)

            if product_link:
                full_link = response.urljoin(product_link)  # Đảm bảo đường dẫn đầy đủ
                yield scrapy.Request(url=full_link, callback=self.parse_product_details, meta={
                    'price': price,  # Lưu giá vào meta
                    'shipping_info': shipping_info,
                    'quantity': quantity,
                    'bids': bids,
                    'time_remaining': time_remaining
                })

        # Truy xuất liên kết đến trang tiếp theo
        next_page = response.xpath("//a[contains(@class, 'pagination__next')]/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info("Following to next page: %s", next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info("No next page link found.")


    def parse_product_details(self, response):
        # Trích xuất các thông tin cần thiết từ trang chi tiết sản phẩm
        product_name = response.xpath("//h1[@class='x-item-title__mainTitle']/span/text()").get()
        price = response.meta.get('price')  # Lấy giá từ meta
        shipping_info = response.meta.get('shipping_info')  # Lấy thông tin vận chuyển từ meta
        quantity = response.meta.get('quantity')  # Lấy quantity từ meta
        bids = response.meta.get('bids')  # Lấy bids từ meta
        time_remaining = response.meta.get('time_remaining')  # Lấy time remaining từ meta

        # Logging cho từng thông tin
        self.logger.info("Parsed product: %s, Price: %s, Quantity: %s, Bids: %s, Time Remaining: %s, Shipping: %s",
                         product_name, price, quantity, bids, time_remaining, shipping_info)

        yield {
            'name': product_name,
            'price': price,
            'quantity': quantity,
            'bids': bids,
            'time_remaining': time_remaining,
            'shipping_info': shipping_info,
            'link': response.url
        }
