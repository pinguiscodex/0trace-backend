from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.common.api.errors import GameAPIException
from apps.economy.models import CoinDefinition, MiningJob, Wallet, WalletBalance, WalletTransaction
from apps.jobs.models import PersistedJob
from apps.jobs.services.job_completion_service import succeed_job
from apps.jobs.services.persisted_job_service import create_job
from apps.machines.services.machine_stats_service import calculate_machine_stats
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def create_mining_job(*, user, machine, wallet_id, coin_slug: str, miner_software=None, mode: str = "cpu", request=None):
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    wallet = Wallet.objects.get(id=wallet_id, owner=user, active=True)
    coin = CoinDefinition.objects.get(slug=coin_slug)
    mining_job = MiningJob.objects.create(user=user, machine=machine, wallet=wallet, coin=coin, miner_software=miner_software, mode=mode)
    job = create_job(kind=PersistedJob.Kind.MINING, actor_user=user, machine=machine, domain_object=mining_job)
    mining_job.persisted_job = job
    mining_job.save(update_fields=["persisted_job", "updated_at"])
    audit(actor=user, event_type="mining_job_start", request=request, metadata={"mining_job": str(mining_job.id)})
    return mining_job


@transaction.atomic
def settle_mining_job(mining_job: MiningJob):
    mining_job = MiningJob.objects.select_for_update().get(id=mining_job.id)
    if mining_job.status in {MiningJob.Status.COMPLETED, MiningJob.Status.CANCELLED}:
        return mining_job
    stats = calculate_machine_stats(mining_job.machine)
    payout = (Decimal(stats["mining_efficiency"]) / mining_job.coin.difficulty).quantize(Decimal("0.00000001"))
    balance, _ = WalletBalance.objects.select_for_update().get_or_create(wallet=mining_job.wallet, coin=mining_job.coin, defaults={"amount": Decimal("0")})
    balance.amount += payout
    balance.save(update_fields=["amount", "updated_at"])
    mining_job.total_payout += payout
    mining_job.status = MiningJob.Status.COMPLETED
    mining_job.completed_at = timezone.now()
    mining_job.payout_settled_until = timezone.now()
    mining_job.save()
    WalletTransaction.objects.create(kind="mining_payout", to_wallet=mining_job.wallet, coin=mining_job.coin, amount=payout, metadata={"mining_job": str(mining_job.id)})
    if mining_job.persisted_job:
        succeed_job(mining_job.persisted_job, result={"payout": str(payout)})
    return mining_job


@transaction.atomic
def cancel_mining_job(*, user, mining_job: MiningJob):
    mining_job = MiningJob.objects.select_for_update().get(id=mining_job.id, user=user)
    if mining_job.status in {MiningJob.Status.COMPLETED, MiningJob.Status.CANCELLED}:
        return mining_job
    mining_job.status = MiningJob.Status.CANCELLED
    mining_job.completed_at = timezone.now()
    mining_job.save()
    if mining_job.persisted_job:
        mining_job.persisted_job.status = PersistedJob.Status.CANCELLED
        mining_job.persisted_job.completed_at = timezone.now()
        mining_job.persisted_job.save()
    return mining_job

