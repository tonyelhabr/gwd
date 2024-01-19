import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode, urlunparse
import time
import sys


class ScrapingService:
    def __init__(self):
        self.base_url = "https://www.geekswhodrink.com"
        self.driver = self.create_driver()

    def _set_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        options = [
            "--headless",
        ]
        for option in options:
            chrome_options.add_argument(option)
        return chrome_options

    def create_driver(self):
        return webdriver.Chrome(options=self._set_chrome_options())

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
            popup_button.click()
        except NoSuchElementException:
            print("Popup button not found.")
            self.driver.quit()
            sys.exit("Exiting the script early and not updating venues.csv.")

    def _extract_venues_data(self):
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        results = soup.find_all("div", class_="find__col find__col--list")
        data = []
        for result in results:
            quiz_blocks = result.find_all("a", class_="quizBlock-returned")
            for quiz_block in quiz_blocks:
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
        self.driver.get(self._create_venues_url())
        self._handle_venues_popup()
        self._extract_venues_data()
        self.driver.quit()
