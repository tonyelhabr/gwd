from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode, urlunparse
import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class ScrapingService:
    def __init__(self):
        self.base_url = "www.geekswhodrink.com"
        logger.info("Creating driver")
        self.driver = self.create_driver()

    def _set_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        options = [
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        for option in options:
            chrome_options.add_argument(option)
            
        logger.info("Setting options")
        return chrome_options

    def create_driver(self):
        return webdriver.Chrome(self._set_chrome_options())

    def _create_venues_url(self):
        path = "venues"
        query_params = {"search": "", "location": ""}
        encoded_params = urlencode(query_params)
        return urlunparse(("https", self.base_url, path, "", encoded_params, ""))

    def _handle_venues_popup(self):
        try:
            popup_button = WebDriverWait(self.driver, 7).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//button[@class="pum-close popmake-close" and @type="button"]',
                    )
                )
            )
            logger.info("Popup button found")
            popup_button.click()
            logger.info("Popup button clicked.")
        except NoSuchElementException:
            logger.error("Popup button not found. Exiting early.")
            self.driver.quit()
            raise Exception("Popup button not found")

    def _extract_venues_data(self):
        logger.info("Waiting for all venues to load on the source page.")
        WebDriverWait(self.driver, 10).until(lambda driver: True)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        logger.info("All venues have loaded on the source page.")
        results = soup.find_all("div", class_="find__col find__col--list")
        data = []
        for i, result in enumerate(results):
            logger.info(f"Parsing result {i}")
            quiz_blocks = result.find_all("a", class_="quizBlock-returned")
            for j, quiz_block in enumerate(quiz_blocks):
                logger.info(f"Parsing quiz block {j}")
                data.append(
                    {
                        "source_id": str(quiz_block["data-podio"]),
                        "url": quiz_block["href"],
                        "lat": quiz_block["data-lat"],
                        "lon": quiz_block["data-lon"],
                        "name": quiz_block["data-title"],
                        "address": quiz_block["data-address"],
                    }
                )
        return data

    def scrape_venues(self):
        try:
            url = self._create_venues_url()
            logger.info(f"Venues URL: {url}")
            self.driver.get(url)
            self._handle_venues_popup()
            scraped_data = self._extract_venues_data()
            return scraped_data
        finally:
            self.driver.quit()
