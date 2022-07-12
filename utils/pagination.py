from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "per_page"
    page_size = 12
    max_page_size = 60
