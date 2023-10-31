from rest_framework.pagination import PageNumberPagination

from core.constants.settings import PAGINATION_PAGE_SIZE


class CustomPagination(PageNumberPagination):
    """
    Пользовательская пагинация для API.

    Опции пагинации:
        - page_size_query_param (str): Параметр запроса для указания
        количества элементов на странице.
        - page_size (int): Количество элементов на странице по умолчанию.

    Константы:
        - PAGINATION_PAGE_SIZE (int): Количество элементов на странице
        по умолчанию.

    Методы:
        - get_page_size(self, request): Возвращает количество элементов
        на странице.
        - get_paginated_response(self, data): Возвращает ответ с данными,
        пагинацией и метаданными.
    """
    page_size_query_param = 'limit'
    page_size = PAGINATION_PAGE_SIZE
