from decimal import Decimal, ROUND_HALF_UP


MONEY_QUANT = Decimal("0.00000001")


def money(value) -> Decimal:
    return Decimal(value).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)


def require_non_negative(value: Decimal) -> None:
    if value < 0:
        raise ValueError("Money values cannot be negative.")

