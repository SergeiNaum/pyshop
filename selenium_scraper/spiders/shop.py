import time

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["www.ozon.ru"]
    start_urls = [
        f"https://www.ozon.ru/category/smartfony-15502/?page={i}&sorting=rating" for i in range(1, 2)
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        product_links = []
        previous_links_count = 0

        while True:

            # wait = WebDriverWait(driver, timeout=10)
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".vi6")))
            time.sleep(3)

            new_links = [
                link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR, "a.tile-hover-target")
            ]

            product_links.extend(new_links)

            # if no new links found, break the loop
            if len(set(new_links)) == 0 or len(set(product_links)) == previous_links_count:
                break

            previous_links_count = len(set(product_links))

        # iterate over product links
        for link in list(set(product_links)):
            driver.get(link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # scrape the desired data from the product page
            name = driver.find_element(By.CSS_SELECTOR, "h1").text
            price = driver.find_element(By.CSS_SELECTOR, ".l3o").text
            os = driver.find_element(By.CSS_SELECTOR, "dd.uj2 a").text


            # add the data to the list of scraped items
            yield {
                "url": link,
                "name": name,
                "price": price,
                "Operation System": os
            }

            # navigate back to the list page
            driver.back()
