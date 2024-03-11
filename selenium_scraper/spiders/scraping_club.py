import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"

    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):


        driver = response.request.meta["driver"]
        product_links = []
        previous_links_count = 0

        while True:
            # scroll down by 10000 pixels
            ActionChains(driver) \
                .scroll_by_amount(0, 10000) \
                .perform()

            # waiting 2 seconds for the products to load
            wait = WebDriverWait(driver, timeout=10)
            wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, ".post:nth-child(60)").is_displayed())

            # select all product links and add them to the list
            new_links = [link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR, ".post a")]
            product_links.extend(new_links)

            # if no new links found, break the loop
            if len(set(new_links)) == 0 or len(set(product_links)) == previous_links_count:
                break

            previous_links_count = len(set(product_links))

        # iterate over product links
        for link in set(product_links):
            driver.get(link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card-img-top")))

            # scrape the desired data from the product page
            name = driver.find_element(By.CSS_SELECTOR, "h3").text
            image = driver.find_element(By.CSS_SELECTOR, ".card-img-top").get_attribute("src")
            price = driver.find_element(By.CSS_SELECTOR, ".card-price").text
            description = driver.find_element(By.CSS_SELECTOR, ".card-description").text

            # add the data to the list of scraped items
            yield {
                "url": link,
                "image": image,
                "name": name,
                "price": price,
                "description": description
            }

            # navigate back to the list page
            driver.back()
