from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    pass


class DataEnvelopeSerializer(serializers.Serializer):
    data = serializers.DictField()


class ErrorEnvelopeSerializer(serializers.Serializer):
    error = serializers.DictField()

