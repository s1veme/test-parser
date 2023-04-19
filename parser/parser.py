import logging

import aiohttp
import validators

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    async def get_page(session: aiohttp.ClientSession, url: str) -> BeautifulSoup | None:
        try:
            async with session.get(url) as response:
                text = await response.text()
                return BeautifulSoup(text, 'lxml')
        except (aiohttp.ClientConnectionError, aiohttp.ServerDisconnectedError, aiohttp.ClientOSError):
            logger.info(f'{url} not parsed')

    @staticmethod
    def get_links(page: BeautifulSoup) -> list[str]:
        """
        :param page: Страница, в которой нужно получить все ссылки
        :return:
        """

        # Собираем все атрибуты "href" из ссылок
        links = []
        for link in page.find_all('a'):
            # Если у ссылки есть атрибут "href" и ссылка имеет валидный формат, то добавляем "href" в список
            if (href := link.get('href')) and validators.url(link['href']):
                links.append(href)

        return links

    @staticmethod
    def get_count_images(page: BeautifulSoup) -> int:
        """
        :param page: Страница, на которой нужно посчитать кол-во изображений
        :return: Кол-во изображений
        """

        return len(page.find_all('img'))

