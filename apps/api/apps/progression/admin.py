from django.contrib import admin

from .models import AchievementDefinition, TutorialMissionDefinition, UserAchievement, UserTutorialProgress


admin.site.register(TutorialMissionDefinition)
admin.site.register(UserTutorialProgress)
admin.site.register(AchievementDefinition)
admin.site.register(UserAchievement)

