from rest_framework import serializers

from .models import AchievementDefinition, TutorialMissionDefinition, UserAchievement, UserTutorialProgress


class TutorialMissionDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialMissionDefinition
        fields = "__all__"


class UserTutorialProgressSerializer(serializers.ModelSerializer):
    mission = TutorialMissionDefinitionSerializer()

    class Meta:
        model = UserTutorialProgress
        fields = "__all__"


class TutorialCompleteStepSerializer(serializers.Serializer):
    step_key = serializers.CharField(max_length=120)


class AchievementDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementDefinition
        fields = "__all__"


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementDefinitionSerializer()

    class Meta:
        model = UserAchievement
        fields = "__all__"

