from apps.economy.models import CoinPricePoint


def latest_price(coin):
    return coin.price_points.order_by("-price_at").first()


def chart_data(coin, limit: int = 100):
    return CoinPricePoint.objects.filter(coin=coin).order_by("-price_at")[:limit]

