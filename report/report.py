import json


class Report:
    def __init__(self, path_file) -> None:
        self.path_file = path_file

    def write_all_links(self, links: list[str]) -> None:
        """
        :param links: Список ссылок, которые нужно записать в отчёт
        :return:
        """
        # Читаем предыдущие данные
        data = self.read_file()
        # Добавляем ссылки в данные
        data['links'] = links

        # Записываем новые данные
        with open(self.path_file, 'w') as file:
            json.dump(data, file, indent=2)

    def add_count_page_by_link(self, link: str, count: int) -> None:
        """
        :param link: Ссылка, где было найдено какое-то кол-во изображений
        :param count: Кол-во изображений по ссылке
        :return:
        """
        # Читаем предыдущие данные
        data = self.read_file()

        # Добавляем кол-во изображений по ссылке в данные
        data[link] = count

        # Записываем новые данные
        with open(self.path_file, 'w') as file:
            json.dump(data, file, indent=2)

    def read_file(self) -> dict:
        """
        Считываем данные из файла, если такого файла нет, то вернётся пустой словарь
        :return: Словарь с данными из файла
        """
        try:
            with open(self.path_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return {}
        return data
