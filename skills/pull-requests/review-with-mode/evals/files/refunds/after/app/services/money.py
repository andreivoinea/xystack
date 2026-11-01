from decimal import ROUND_HALF_UP, Decimal


def to_cents(amount):
    """Convert an amount in the main currency unit to whole cents."""
    return int((Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
