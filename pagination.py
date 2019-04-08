from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination



class CSLimitOffestpagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10

class CSPageNumberPagination(PageNumberPagination):
    page_size = 10