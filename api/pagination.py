from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class VerbosePageNumberPagination(PageNumberPagination):
    """
    Add some additional information to pagination.
    """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('start', self.page.start_index()),
            ('end', self.page.end_index()),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
