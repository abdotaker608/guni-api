from rest_framework.filters import BaseFilterBackend
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


class AdvancedProductsFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params.dict()
        search = query_params.pop('search', '')
        allowed_keys = ['price__lte', 'price__gte', 'category', 'on_sale']
        for key in set(query_params.keys()) - set(allowed_keys):
            query_params.pop(key)
        if 'on_sale' in query_params:
            query_params.update({'on_sale': True})
        queryset = queryset.filter(**query_params)
        if search:
            queryset = queryset.\
                annotate(similarity=TrigramSimilarity('name', search)).\
                filter(similarity__gte=.1)
        return queryset
