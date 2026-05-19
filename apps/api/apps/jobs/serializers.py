from rest_framework import serializers

from .models import PersistedJob


class PersistedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersistedJob
        fields = "__all__"
