import asyncio
import logging
import aiohttp

from src.scraping.extract_data import ExtractData
from src.data.data_processor import DataProcessor
from src.utils.data_manager import DataManager
from utils.async_manager import AsyncManager


class WebScraper:
    def __init__(self, base_url):
        """
        Initializes the scraper with a base URL and a data manager.
        :param base_url: The URL to scrape.
        :param data_manager: An instance of the DataManager class.
        """
        self.base_url = base_url
        self.data_manager = DataManager.get_instance()
        self.extract_data = ExtractData()
        self.data_processor = DataProcessor(self.data_manager, self.extract_data)
        self.async_manager = AsyncManager()

    async def scrape(self):
        """
        Scrapes the base URL for links and processes them asynchronously.
        """
        async with aiohttp.ClientSession() as session:
            try:
                # Fetch the base page and parse links
                base_soup = await self.extract_data.fetch_with_retry(
                    session, self.base_url
                )

                links = self.extract_data.extract_links(base_soup)

                # Process links concurrently
                await self.async_manager.process_tasks(
                    [self.data_processor.process_link(session, link) for link in links]
                )

                # Log results
                data = self.data_processor.data_manager.get_data()
                logging.info(f"Scraping complete. Total entries: {len(data)}")
            except Exception as e:
                logging.error(f"Scraping failed for {self.base_url}: {e}")
