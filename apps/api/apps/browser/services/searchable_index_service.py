from apps.browser.models import SearchIndexEntry


def search(query: str):
    return SearchIndexEntry.objects.filter(title__icontains=query) | SearchIndexEntry.objects.filter(body__icontains=query)

