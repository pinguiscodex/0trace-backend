import random
from decimal import Decimal


def suggested_price(base_price, condition="good", market_trend=0.0):
    """Calculate a suggested marketplace price based on base price, condition, and market trend.
    
    Args:
        base_price: The base retail price of the item.
        condition: Item condition - "new", "good", "fair", "poor".
        market_trend: Market trend multiplier (-0.3 to 0.3 range typical).
    
    Returns:
        Suggested price as Decimal.
    """
    condition_multipliers = {
        "new": Decimal("1.0"),
        "good": Decimal("0.85"),
        "fair": Decimal("0.65"),
        "poor": Decimal("0.45"),
    }
    
    multiplier = condition_multipliers.get(condition, Decimal("0.75"))
    trend_factor = Decimal(str(1.0 + max(-0.3, min(0.3, market_trend))))
    
    suggested = base_price * multiplier * trend_factor
    return suggested.quantize(Decimal("0.01"))
