from django.contrib import admin

from .models import ActiveSoftwareSelection, SkillDefinition, SkillProgress, SoftwareFile, SoftwareUpgradeRule, XPEvent


admin.site.register(SoftwareFile)
admin.site.register(ActiveSoftwareSelection)
admin.site.register(SoftwareUpgradeRule)
admin.site.register(SkillDefinition)
admin.site.register(SkillProgress)
admin.site.register(XPEvent)

