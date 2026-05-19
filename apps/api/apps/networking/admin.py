from django.contrib import admin

from .models import CrackJob, SimulatedLoginAttempt, SimulatedRemoteSession


admin.site.register(CrackJob)
admin.site.register(SimulatedRemoteSession)
admin.site.register(SimulatedLoginAttempt)

