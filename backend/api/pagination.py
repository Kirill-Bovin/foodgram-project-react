from rest_framework.pagination import PageNumberPagination


class PageFieldPagination(PageNumberPagination):
    page_size_query_param = 'limit'
