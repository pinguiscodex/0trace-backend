from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.api.responses import accepted, no_content, ok
from apps.machines.models import Machine
from apps.software.models import SoftwareFile

from .models import CoinDefinition, MiningJob, Wallet
from .serializers import (
    CoinDefinitionSerializer,
    CoinBuySerializer,
    CoinPricePointSerializer,
    CoinSellSerializer,
    MiningJobCreateSerializer,
    MiningJobSerializer,
    WalletCreateSerializer,
    WalletSerializer,
    WalletTransactionSerializer,
    WalletTransferSerializer,
)
from .services.coin_price_service import chart_data
from .services.mining_service import cancel_mining_job, create_mining_job
from .services.transfer_service import buy_coin, sell_coin, transfer
from .services.wallet_service import create_wallet, delete_wallet


@extend_schema(tags=["economy"])
class CoinListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CoinDefinitionSerializer

    def get(self, request):
        return ok(CoinDefinitionSerializer(CoinDefinition.objects.all(), many=True).data)


@extend_schema(tags=["economy"])
class CoinPricesView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CoinPricePointSerializer

    def get(self, request, slug):
        coin = CoinDefinition.objects.get(slug=slug)
        return ok(CoinPricePointSerializer(chart_data(coin), many=True).data)


@extend_schema(tags=["economy"])
class CoinBuyView(APIView):
    serializer_class = CoinBuySerializer

    @extend_schema(request=CoinBuySerializer, responses={200: WalletTransactionSerializer})
    def post(self, request, slug):
        serializer = CoinBuySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = Wallet.objects.get(id=serializer.validated_data["wallet_id"], owner=request.user)
        tx = buy_coin(user=request.user, wallet=wallet, coin_slug=slug, credit_amount=serializer.validated_data["credit_amount"], request=request)
        return ok(WalletTransactionSerializer(tx).data)


@extend_schema(tags=["economy"])
class CoinSellView(APIView):
    serializer_class = CoinSellSerializer

    @extend_schema(request=CoinSellSerializer, responses={200: WalletTransactionSerializer})
    def post(self, request, slug):
        serializer = CoinSellSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = Wallet.objects.get(id=serializer.validated_data["wallet_id"], owner=request.user)
        tx = sell_coin(user=request.user, wallet=wallet, coin_slug=slug, coin_amount=serializer.validated_data["coin_amount"], request=request)
        return ok(WalletTransactionSerializer(tx).data)


@extend_schema(tags=["economy"])
class WalletListCreateView(APIView):
    serializer_class = WalletCreateSerializer

    @extend_schema(operation_id="wallets_list", responses={200: WalletSerializer(many=True)})
    def get(self, request):
        return ok(WalletSerializer(Wallet.objects.filter(owner=request.user), many=True).data)

    @extend_schema(request=WalletCreateSerializer, responses={201: WalletSerializer})
    def post(self, request):
        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok(WalletSerializer(create_wallet(user=request.user, **serializer.validated_data)).data, status_code=201)


@extend_schema(tags=["economy"])
class WalletDetailView(APIView):
    serializer_class = WalletSerializer

    @extend_schema(operation_id="wallets_retrieve", responses={200: WalletSerializer})
    def get(self, request, wallet_id):
        return ok(WalletSerializer(Wallet.objects.get(id=wallet_id, owner=request.user)).data)

    def delete(self, request, wallet_id):
        delete_wallet(user=request.user, wallet=Wallet.objects.get(id=wallet_id, owner=request.user))
        return no_content()


@extend_schema(tags=["economy"])
class WalletTransferView(APIView):
    serializer_class = WalletTransferSerializer

    @extend_schema(request=WalletTransferSerializer, responses={200: WalletTransactionSerializer})
    def post(self, request, wallet_id):
        serializer = WalletTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx = transfer(user=request.user, from_wallet=Wallet.objects.get(id=wallet_id, owner=request.user), request=request, **serializer.validated_data)
        return ok(WalletTransactionSerializer(tx).data)


@extend_schema(tags=["economy"])
class MiningJobListCreateView(APIView):
    serializer_class = MiningJobCreateSerializer

    @extend_schema(operation_id="mining_jobs_list", responses={200: MiningJobSerializer(many=True)})
    def get(self, request):
        return ok(MiningJobSerializer(MiningJob.objects.filter(user=request.user), many=True).data)

    @extend_schema(request=MiningJobCreateSerializer, responses={202: MiningJobSerializer})
    def post(self, request):
        serializer = MiningJobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        machine = Machine.objects.get(id=data["machine_id"], owner=request.user)
        miner = None
        if data.get("miner_software_id"):
            miner = SoftwareFile.objects.get(id=data["miner_software_id"], owner=request.user, machine=machine)
        mining_job = create_mining_job(user=request.user, machine=machine, wallet_id=data["wallet_id"], coin_slug=data["coin_slug"], miner_software=miner, mode=data["mode"], request=request)
        return accepted(MiningJobSerializer(mining_job).data, request_id=getattr(request, "request_id", ""))


@extend_schema(tags=["economy"])
class MiningJobDetailView(APIView):
    serializer_class = MiningJobSerializer

    @extend_schema(operation_id="mining_jobs_retrieve", responses={200: MiningJobSerializer})
    def get(self, request, mining_job_id):
        return ok(MiningJobSerializer(MiningJob.objects.get(id=mining_job_id, user=request.user)).data)


@extend_schema(tags=["economy"])
class MiningJobCancelView(APIView):
    serializer_class = MiningJobSerializer

    def post(self, request, mining_job_id):
        return ok(MiningJobSerializer(cancel_mining_job(user=request.user, mining_job=MiningJob.objects.get(id=mining_job_id, user=request.user))).data)
