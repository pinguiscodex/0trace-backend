from apps.hardware.models import Delivery
from apps.hardware.services.delivery_service import claim_delivery


def run(job):
    return claim_delivery(user=job.actor_user, delivery=Delivery.objects.get(id=job.domain_object_id))
