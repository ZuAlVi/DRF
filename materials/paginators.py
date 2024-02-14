from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    page_size = 10
