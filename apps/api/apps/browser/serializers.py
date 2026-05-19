from rest_framework import serializers

from .models import Certificate, Domain, SearchIndexEntry, Website, WebsiteFile


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class DomainPurchaseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=253)
    machine_id = serializers.UUIDField(required=False)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


class CertificatePurchaseSerializer(serializers.Serializer):
    domain_id = serializers.UUIDField()


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"
        read_only_fields = ["owner", "trust_level", "site_type", "sandbox_policy", "content_version"]


class WebsiteFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteFile
        fields = "__all__"


class BrowserResolveSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=500)


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchIndexEntry
        fields = "__all__"

