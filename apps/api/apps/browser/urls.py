from django.urls import path

from .views import (
    BrowserResolveView,
    CertificateListView,
    CertificatePurchaseView,
    DomainListView,
    DomainPurchaseView,
    SearchableSearchView,
    WebsiteDetailView,
    WebsiteFileDetailView,
    WebsiteFilesView,
    WebsiteListCreateView,
    WebsitePublishView,
)

urlpatterns = [
    path("browser/resolve/", BrowserResolveView.as_view(), name="browser-resolve"),
    path("websites/", WebsiteListCreateView.as_view(), name="websites"),
    path("websites/<uuid:website_id>/", WebsiteDetailView.as_view(), name="website-detail"),
    path("websites/<uuid:website_id>/publish/", WebsitePublishView.as_view(), name="website-publish"),
    path("websites/<uuid:website_id>/files/", WebsiteFilesView.as_view(), name="website-files"),
    path("website-files/<uuid:file_id>/", WebsiteFileDetailView.as_view(), name="website-file-detail"),
    path("domains/", DomainListView.as_view(), name="domains"),
    path("domains/purchase/", DomainPurchaseView.as_view(), name="domain-purchase"),
    path("certificates/", CertificateListView.as_view(), name="certificates"),
    path("certificates/purchase/", CertificatePurchaseView.as_view(), name="certificate-purchase"),
    path("searchable/search/", SearchableSearchView.as_view(), name="searchable-search"),
]

