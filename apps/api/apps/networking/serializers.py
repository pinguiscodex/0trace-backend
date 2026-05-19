from rest_framework import serializers

from .models import CrackJob, SimulatedRemoteSession


class CrackJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrackJob
        fields = "__all__"


class CrackJobCreateSerializer(serializers.Serializer):
    attacker_machine_id = serializers.UUIDField()
    target_ip = serializers.CharField(max_length=45)
    cracker_software_id = serializers.UUIDField(required=False)


class TerminalExecuteSerializer(serializers.Serializer):
    command = serializers.CharField(max_length=500)


class SimulatedRemoteSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatedRemoteSession
        fields = "__all__"

