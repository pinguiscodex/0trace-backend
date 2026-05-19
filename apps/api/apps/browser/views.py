from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.common.api.errors import GameAPIException
from apps.common.api.responses import no_content, ok
from apps.machines.models import Machine

from .models import Certificate, Domain, Website, WebsiteFile
from .serializers import (
    BrowserResolveSerializer,
    CertificatePurchaseSerializer,
    CertificateSerializer,
    DomainPurchaseSerializer,
    DomainSerializer,
    SearchResultSerializer,
    WebsiteFileSerializer,
    WebsiteSerializer,
)
from .services.browser_resolution_service import resolve_url
from .services.certificate_service import purchase_certificate
from .services.domain_service import purchase_domain
from .services.searchable_index_service import search
from .services.website_service import create_website, publish_website


@extend_schema(tags=["browser"])
class BrowserResolveView(APIView):
    serializer_class = BrowserResolveSerializer

    @extend_schema(request=BrowserResolveSerializer, responses={200: dict})
    def post(self, request):
        serializer = BrowserResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = resolve_url(serializer.validated_data["url"])
        if result is None:
            raise GameAPIException("Target not found.", code="target_not_found", status_code=404)
        return ok(result)


@extend_schema(tags=["browser"])
class WebsiteListCreateView(APIView):
    serializer_class = WebsiteSerializer

    @extend_schema(operation_id="websites_list", responses={200: WebsiteSerializer(many=True)})
    def get(self, request):
        return ok(WebsiteSerializer(Website.objects.filter(owner=request.user), many=True).data)

    @extend_schema(request=WebsiteSerializer, responses={201: WebsiteSerializer})
    def post(self, request):
        domain = None
        if request.data.get("domain"):
            domain = Domain.objects.get(id=request.data["domain"], owner=request.user)
        website = create_website(user=request.user, domain=domain, title=request.data.get("title", "Untitled"), html=request.data.get("html", ""), css=request.data.get("css", ""), js=request.data.get("js", ""))
        return ok(WebsiteSerializer(website).data, status_code=201)


@extend_schema(tags=["browser"])
class WebsiteDetailView(APIView):
    serializer_class = WebsiteSerializer

    @extend_schema(operation_id="websites_retrieve", responses={200: WebsiteSerializer})
    def get(self, request, website_id):
        return ok(WebsiteSerializer(Website.objects.get(id=website_id, owner=request.user)).data)

    def patch(self, request, website_id):
        website = Website.objects.get(id=website_id, owner=request.user)
        for field in ["title", "html", "css", "js", "status"]:
            if field in request.data:
                setattr(website, field, request.data[field])
        website.content_version += 1
        website.save()
        return ok(WebsiteSerializer(website).data)

    def delete(self, request, website_id):
        Website.objects.get(id=website_id, owner=request.user).delete()
        return no_content()


@extend_schema(tags=["browser"])
class WebsitePublishView(APIView):
    serializer_class = WebsiteSerializer

    def post(self, request, website_id):
        website = Website.objects.get(id=website_id, owner=request.user)
        machine = Machine.objects.get(id=request.data["machine_id"], owner=request.user)
        deployment = publish_website(user=request.user, website=website, machine=machine)
        return ok({"deployment_id": str(deployment.id), "status": deployment.status})


@extend_schema(tags=["browser"])
class WebsiteFilesView(APIView):
    serializer_class = WebsiteFileSerializer

    def get(self, request, website_id):
        website = Website.objects.get(id=website_id, owner=request.user)
        return ok(WebsiteFileSerializer(website.files.all(), many=True).data)

    def post(self, request, website_id):
        website = Website.objects.get(id=website_id, owner=request.user)
        file = WebsiteFile.objects.create(website=website, path=request.data["path"], content=request.data.get("content", ""), content_type=request.data.get("content_type", "text/html"))
        return ok(WebsiteFileSerializer(file).data, status_code=201)


@extend_schema(tags=["browser"])
class WebsiteFileDetailView(APIView):
    serializer_class = WebsiteFileSerializer

    def patch(self, request, file_id):
        file = WebsiteFile.objects.get(id=file_id, website__owner=request.user)
        for field in ["path", "content", "content_type"]:
            if field in request.data:
                setattr(file, field, request.data[field])
        file.save()
        return ok(WebsiteFileSerializer(file).data)

    def delete(self, request, file_id):
        WebsiteFile.objects.get(id=file_id, website__owner=request.user).delete()
        return no_content()


@extend_schema(tags=["browser"])
class DomainListView(APIView):
    serializer_class = DomainSerializer

    def get(self, request):
        return ok(DomainSerializer(Domain.objects.filter(owner=request.user), many=True).data)


@extend_schema(tags=["browser"])
class DomainPurchaseView(APIView):
    serializer_class = DomainPurchaseSerializer

    @extend_schema(request=DomainPurchaseSerializer, responses={201: DomainSerializer})
    def post(self, request):
        serializer = DomainPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        machine = None
        if serializer.validated_data.get("machine_id"):
            machine = Machine.objects.get(id=serializer.validated_data["machine_id"], owner=request.user)
        return ok(DomainSerializer(purchase_domain(user=request.user, name=serializer.validated_data["name"], machine=machine)).data, status_code=201)


@extend_schema(tags=["browser"])
class CertificateListView(APIView):
    serializer_class = CertificateSerializer

    def get(self, request):
        return ok(CertificateSerializer(Certificate.objects.filter(owner=request.user), many=True).data)


@extend_schema(tags=["browser"])
class CertificatePurchaseView(APIView):
    serializer_class = CertificatePurchaseSerializer

    @extend_schema(request=CertificatePurchaseSerializer, responses={201: CertificateSerializer})
    def post(self, request):
        serializer = CertificatePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = Domain.objects.get(id=serializer.validated_data["domain_id"], owner=request.user)
        return ok(CertificateSerializer(purchase_certificate(user=request.user, domain=domain)).data, status_code=201)


@extend_schema(tags=["browser"])
class SearchableSearchView(APIView):
    serializer_class = SearchResultSerializer

    def get(self, request):
        return ok(SearchResultSerializer(search(request.GET.get("q", "")), many=True).data)
