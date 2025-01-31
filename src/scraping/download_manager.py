import logging
import os
import aiohttp

from src.utils.file_manager import FileManager
from src.utils.async_manager import AsyncManager


class DownloadManager:
    def __init__(self, download_dir="media"):
        self.async_manager = AsyncManager()
        self.file_manager = FileManager()
        self.download_dir = download_dir

        os.makedirs(self.download_dir, exist_ok=True)

    async def safe_download(self, video, word):
        """
        Safely downloads a video with retries.
        """
        return await self.async_manager.retry_with_backoff(
            self.manage_download, video, word
        )

    async def download_file(self, url, file_path, word):
        """
        Downloads a file asynchronously using aiohttp.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(file_path, "wb") as file:
                            file.write(await response.read())
                        logging.info(f"Downloaded: {word} -> {file_path}")
                        return file_path
                    else:
                        raise Exception(f"HTTP error {response.status} for {url}")
        except Exception as e:
            logging.error(f"Error downloading video for word '{word}': {e}")
            return None

    def manage_download(self, url, word):
        """
        Downloads a video by determining the file extension and constructing the file path.
        :param url: The URL to download.
        :param word: The associated word for the file.
        :return: The file path if successful, None otherwise.
        """
        self.file_extension = self.file_manager.get_file_extension(url)
        self.file_path = self.file_manager.construct_file_path(
            self.download_dir, word, self.file_extension
        )
        return self.download_file(url, self.file_path, word)
