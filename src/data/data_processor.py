import asyncio
import logging

from extract_data import ExtractData
from src.scraping.download_manager import DownloadManager
from utils.data_manager import DataManager


class DataProcessor:
    def __init__(self):
        self.data_manager = DataManager.get_instance()
        self.extract_data = ExtractData()
        self.download_manager = DownloadManager()
        self.semaphore = asyncio.Semaphore(5)

    async def process_link(self, session, url):
        """
        Processes a link by extracting words and URLs, downloading videos,
        and updating the data manager.
        """
        try:
            # Extract data with retries
            self.soup = await self.extract_data.fetch_with_retry(session, url)

            # Extract words and URLs
            self.word_url_pairs = await self.extract_data.extract_with_retry(
                self.soup, self.data_manager
            )

            # Process each word and URL pair
            for self.word, self.video_url in self.word_url_pairs:
                try:
                    self.file_path = await self.download_manager.safe_download(
                        self.video_url, self.word
                    )

                    self.data_manager.add_data(self.word, self.file_path)

                    logging.info(f"Processed: {self.word} -> {self.file_path}")
                except Exception as e:
                    logging.warning(f"Download failed for {self.word}: {e}")

        except Exception as e:
            logging.error(f"Error processing link {url}: {e}")
