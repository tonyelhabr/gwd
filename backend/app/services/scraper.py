from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from app.extensions.logger import LOGGER_NAME
import time
import random
import pandas as pd
from io import StringIO

logger = logging.getLogger(LOGGER_NAME)
MAX_RESULTS_PAGE_TO_SCRAPE = 2


class ScrapingService:
    def __init__(self):
        self.base_url = "https://www.geekswhodrink.com"
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

    def _handle_popup(self):
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
            try:
                popup_button.click()
                logger.info("Popup button clicked.")
            except Exception as e:
                logger.info("Popup button hidden on page. No button to click.")
        except NoSuchElementException:
            msg = "Popup button not found. Exiting early."
            logger.error(msg)
            self.driver.quit()
            raise Exception(msg)

    def create_driver(self):
        return webdriver.Chrome(self._set_chrome_options())


class VenueScrapingService(ScrapingService):
    def __init__(self):
        super().__init__()

    def _create_venues_url(self):
        return f"{self.base_url}/venues"

    def _extract_venues_data(self):
        logger.info("Waiting for all venues to load on the source page.")
        # WebDriverWait(self.driver, 10).until(lambda driver: True)
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        logger.info("All venues have loaded on the source page.")
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
        try:
            url = self._create_venues_url()
            self.driver.get(url)
            self._handle_venues_popup()
            scraped_data = self._extract_venues_data()
            return scraped_data
        finally:
            self.driver.quit()


class ResultsScrapingService(ScrapingService):
    def __init__(self, source_id):
        super().__init__()
        self.source_id = source_id

    def _create_results_page_url(self, page):
        url = f"{self.base_url}/venues/{self.source_id}/?pag={page}"
        return url

    def _clean_results_df(self, df):
        df["Place Ranking"] = pd.to_numeric(
            df["Place Ranking"], errors="coerce"
        ).astype("Int64")
        df["Team Name"] = df["Team Name"].astype(str)
        df["Score"] = pd.to_numeric(df["Score"], errors="coerce").astype("Int64")
        df.columns = [col.replace(" ", "_").lower() for col in df.columns]
        return df

    def _scrape_tables_from_venue_page(self, page):
        time.sleep(random.uniform(1, 2))
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz__title"))
            )
        except NoSuchElementException:
            msg = (
                f"No quiz dates found for venue_id = {self.venue_id} on page = {page}."
            )
            logger.error(msg)
            self.driver.quit()
            return Exception(msg)

        quiz_dates = [
            element.text
            for element in self.driver.find_elements(By.CSS_SELECTOR, ".quiz__title")
        ]
        n_quiz_dates = len(quiz_dates)
        time.sleep(random.uniform(1, 2))

        tables = self.driver.find_elements(By.CSS_SELECTOR, "table")
        data_frames = []
        for table in tables:
            df = pd.read_html(StringIO(table.get_attribute("outerHTML")))[0]
            if all(
                col in df.columns for col in ["Place Ranking", "Team Name", "Score"]
            ):
                df = self._clean_results_df(df)
                data_frames.append(df)

        n_tbs = len(data_frames)
        if n_tbs == 0:
            print(f"No tables found for venue_id = {self.venue_id} on page = {page}.")
        elif n_tbs != n_quiz_dates:
            print(
                f"Number of tables ({n_tbs}) is different from number of quiz dates ({n_quiz_dates})."
            )
            if n_tbs < n_quiz_dates:
                quiz_dates = quiz_dates[:n_tbs]

        res = pd.concat(data_frames, keys=quiz_dates, names=["quiz_date"]).reset_index(
            level=0
        )
        res["quiz_date"] = pd.to_datetime(res["quiz_date"], format="%a, %b %d, %Y")
        return res

    def scrape_results(self):
        try:
            page = 1
            all_tables = []
            while page <= MAX_RESULTS_PAGE_TO_SCRAPE:
                print(f"Scraping page {page} for venue ID {self.source_id}.")
                url = self._create_results_page_url(page)
                self.driver.get(url)
                self._handle_popup()
                tables = self._scrape_tables_from_venue_page(page)
                page += 1
                all_tables.append(tables)

            all_results = pd.concat(all_tables)
            return all_results
        finally:
            self.driver.quit()
