from django.urls import path

from .views import CrackJobCancelView, CrackJobDetailView, CrackJobListCreateView, MachineSecurityEventsView, TerminalExecuteView, TerminalHistoryView

urlpatterns = [
    path("crack-jobs/", CrackJobListCreateView.as_view(), name="crack-jobs"),
    path("crack-jobs/<uuid:crack_job_id>/", CrackJobDetailView.as_view(), name="crack-job-detail"),
    path("crack-jobs/<uuid:crack_job_id>/cancel/", CrackJobCancelView.as_view(), name="crack-job-cancel"),
    path("machines/<uuid:machine_id>/security-events/", MachineSecurityEventsView.as_view(), name="machine-security-events"),
    path("machines/<uuid:machine_id>/terminal/execute/", TerminalExecuteView.as_view(), name="terminal-execute"),
    path("machines/<uuid:machine_id>/terminal/history/", TerminalHistoryView.as_view(), name="terminal-history"),
]

