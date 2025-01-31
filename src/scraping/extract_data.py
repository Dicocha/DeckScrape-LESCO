from bs4 import BeautifulSoup
from src.utils.async_manager import AsyncManager
from utils.data_manager import DataManager


class ExtractData:
    def __init__(self, retries=3, delay=1):
        self.data_manager = DataManager.get_instance()
        self.reties = retries
        self.delay = delay
        self.async_manager = AsyncManager()

    async def fetch_with_retry(self, session, url):
        return await self.async_manager.retry_with_backoff(
            self.fetch_content, self.retries, 1, session, url
        )

    async def extract_with_retry(self, soup):
        return await self.async_manager.retry_with_backoff(
            self.extract_data, self.retries, self.delay, soup, self.data_manager
        )

    async def extract_data(self, soup):
        """
        Logic for extracting words and URLs.
        """
        self.data_manager.add_word(await self.extract_words(soup))
        self.data_manager.add_url(await self.extract_urls(soup))

        if not self.data_manager.verify_length():
            raise ValueError("Mismatch between the number of words and URLs.")

        return zip(self.words, self.urls)

    @staticmethod
    def extract_links(soup):
        """Extracts all links within <td> elements."""
        return [
            a_tag["href"]
            for td in soup.find_all("td")
            if (a_tag := td.find("a", href=True))
        ]

    @staticmethod
    async def extract_words(soup):
        """Extracts all words from <span> elements with a specific class."""
        return [span.text for span in soup.find_all("span", "elementskit-tab-title")]

    @staticmethod
    async def extract_urls(soup):
        """Extracts all image/video URLs from a BeautifulSoup object."""
        return [
            img["src"]
            for img in soup.find_all("img", "aligncenter")
            if "src" in img.attrs
        ]

    @staticmethod
    async def fetch_content(session, url):
        """
        Fetches the HTML content of a URL asynchronously.
        :param session: The aiohttp client session.
        :param url: The URL to fetch.
        """
        async with session.get(url) as response:
            html = await response.text()
            return BeautifulSoup(html, "lxml")
