from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class RegularResultsSetPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = 'page_size'
    max_page_size = 10000


class TinyResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000
