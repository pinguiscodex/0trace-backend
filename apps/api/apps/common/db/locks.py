from django.db.models import QuerySet


def for_update(queryset: QuerySet, **kwargs) -> QuerySet:
    return queryset.select_for_update(**kwargs)

