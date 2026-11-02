"""Pure calculations and in-memory CSV for fictional records only."""
import csv
import io
from decimal import Decimal

from demo_data import FICTIONAL_OPENING_KG, FICTIONAL_PURCHASE_RWF_PER_KG


def scenario_summary(rows, selected, zero_expenses=False):
    quantity = sum((r['quantity_kg'] for r in selected), Decimal(0))
    revenue = sum((r['revenue'] for r in selected), Decimal(0))
    cogs = quantity * FICTIONAL_PURCHASE_RWF_PER_KG
    return {'quantity_kg': quantity, 'revenue_rwf': revenue, 'cogs_rwf': cogs,
            'gross_profit_rwf': revenue - cogs,
            'transaction_profit_rwf': revenue - cogs if zero_expenses else None,
            'weighted_price_rwf': revenue / quantity if quantity else None,
            'remaining_kg': FICTIONAL_OPENING_KG - sum((r['quantity_kg'] for r in rows), Decimal(0)),
            'transactions': len(selected)}


def daily_quantities(rows):
    totals = {}
    for row in rows:
        totals[row['date']] = totals.get(row['date'], Decimal(0)) + row['quantity_kg']
    return [{'date': day, 'quantity_kg': float(kg)} for day, kg in sorted(totals.items())]


def fictional_csv(rows):
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(['data_status', 'date', 'quantity_kg', 'selling_price_rwf_per_kg', 'revenue_rwf'])
    for row in rows:
        writer.writerow(['SIMULATED_FICTIONAL', row['date'].isoformat(), row['quantity_kg'],
                         row['selling_price_per_kg'], row['revenue']])
    return output.getvalue().encode('utf-8-sig')
