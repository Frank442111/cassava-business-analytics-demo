"""Wholly invented portfolio scenario: no file access, parameters or real-data inputs."""
from datetime import date, timedelta
from decimal import Decimal

FICTIONAL_OPENING_KG = Decimal('12000')
FICTIONAL_PURCHASE_RWF_PER_KG = Decimal('460')


def fictional_transactions():
    """112 new fictional transactions across 56 days; arithmetic, not a ledger transform."""
    rows = []
    start = date(2032, 4, 1)
    for day in range(56):
        current = start + timedelta(days=day)
        weekly = [0, 5, 12, 18, 9, 3, 0][current.weekday()]
        for sale in range(2):
            quantity = Decimal(32 + (day * 7 + sale * 11) % 19 + weekly)
            price = Decimal(720 + ((day + sale * 2) % 5) * 15)
            rows.append({'date': current, 'quantity_kg': quantity,
                         'selling_price_per_kg': price, 'revenue': quantity * price})
    return rows
