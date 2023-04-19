import platform

from parser import Parser
from report import Report
import aiohttp
import asyncio

# Ссылка, на которой будем искать ссылки
PARSING_URL = 'https://www.kinoafisha.info/rating/movies/'


async def get_count_images(session: aiohttp.ClientSession, link: str, count_links_report: Report):
    page = await Parser.get_page(session, link)
    if page is None:
        return

    # Получаем кол-во изображений по ссылке
    count = Parser.get_count_images(page)
    # Записываем кол-во изображений в отчёт
    count_links_report.add_count_page_by_link(link, count)

    print(f'На странице {link} было найдено {count} изображений')


async def main():
    # Инициализируем парсер и отчёт
    all_links_report = Report('links.json')
    count_links_report = Report('count.json')

    async with aiohttp.ClientSession() as session:
        # Получаем разметку страницы
        page = await Parser.get_page(session, PARSING_URL)

        if page is None:
            return

        # Получаем все ссылки на странице
        links = Parser.get_links(page)
        # Записываем все ссылки в отчёт
        all_links_report.write_all_links(links)

        tasks = []

        for link in links:
            task = asyncio.create_task(get_count_images(session, link, count_links_report))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(main())
