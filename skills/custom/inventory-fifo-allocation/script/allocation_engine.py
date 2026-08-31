"""
Generic Inventory Allocation Engine with FIFO and No-Negative-Stock Constraints.

Usage:
    from allocation_engine import allocate_fifo, allocate_proportional, allocate_hybrid

    result = allocate_hybrid(
        supply_df=supply,           # columns: item_col, qty_col, date_col, price_col
        demand_df=demand,           # columns: item_col, qty_col, date_col, id_col
        item_col='Mã NVL',
        qty_col='SL',
        date_col='Ngày',
        price_col='Đơn giá',
        id_col='Số HĐ',
        detailed_ids=None,          # list of demand IDs that have BOM detail
        reduction_rate=None         # auto-computed if None
    )
"""

import pandas as pd


def allocate_proportional(supply_df, demand_df, item_col, qty_col, price_col=None,
                          id_col=None, date_col=None, reduction_rate=None):
    """
    Strategy A: Reduce all demand proportionally so total does not exceed supply.
    Every demand record gets the same percentage of its original request.

    Parameters
    ----------
    supply_df, demand_df : DataFrame
    item_col, qty_col : str
        Column names for item key and quantity
    price_col, id_col, date_col : str or None
    reduction_rate : float or None
        If None, auto-computed as 1 - (total_supply / total_demand)

    Returns
    -------
    dict with keys: 'allocation', 'balance', 'reduction_rate'
    """
    supply_total = supply_df[qty_col].sum()
    demand_total = demand_df[qty_col].sum()

    if reduction_rate is None:
        if supply_total >= demand_total:
            reduction_rate = 0.0
        else:
            reduction_rate = 1.0 - (supply_total / demand_total)

    keep_rate = 1.0 - reduction_rate
    result = demand_df.copy()
    result['allocated_qty'] = (result[qty_col] * keep_rate).round(4)
    if price_col and price_col in result.columns:
        result['allocated_value'] = (result['allocated_qty'] * result[price_col]).round(0)
    else:
        result['allocated_value'] = result['allocated_qty']

    balance = _compute_balance(supply_df, result, item_col, qty_col)

    return {
        'allocation': result,
        'balance': balance,
        'reduction_rate': reduction_rate,
        'keep_rate': keep_rate
    }


def allocate_fifo(supply_df, demand_df, item_col, qty_col, date_col,
                  price_col=None, id_col=None):
    """
    Strategy B: Sequential FIFO allocation. Sort demand by date, consume
    from available stock. Each demand record may get full, partial, or zero.

    Parameters
    ----------
    date_col : str
        Column name for date (used for FIFO ordering)
    Other params same as allocate_proportional

    Returns
    -------
    dict with keys: 'allocation', 'balance'
    """
    result_rows = []

    for item in demand_df[item_col].unique():
        item_supply = supply_df[supply_df[item_col] == item].copy()
        item_demand = demand_df[demand_df[item_col] == item].copy()

        if item_supply.empty:
            for _, d in item_demand.iterrows():
                row = d.to_dict()
                row['allocated_qty'] = 0.0
                row['allocated_value'] = 0.0
                result_rows.append(row)
            continue

        total_stock = item_supply[qty_col].sum()

        item_demand = item_demand.sort_values(date_col)
        for _, d in item_demand.iterrows():
            row = d.to_dict()
            requested = d[qty_col]
            allocated = min(requested, total_stock)
            total_stock -= allocated
            row['allocated_qty'] = round(allocated, 4)
            if price_col and price_col in d:
                row['allocated_value'] = round(allocated * d[price_col], 0)
            else:
                row['allocated_value'] = round(allocated, 0)
            result_rows.append(row)

    result = pd.DataFrame(result_rows)
    balance = _compute_balance(supply_df, result, item_col, qty_col)

    return {'allocation': result, 'balance': balance}


def allocate_hybrid(supply_df, demand_df, item_col, qty_col, date_col,
                    price_col=None, id_col=None, detailed_ids=None,
                    reduction_rate=None):
    """
    Strategy C: Reduce detailed demand proportionally, then use saved stock
    to fulfill undetailed demand via FIFO.

    detailed_ids : list or None
        Demand record IDs that have detailed BOM/specs. These get reduced.
        Others (undetailed) get funded from saved stock.
    """
    if detailed_ids is None or id_col is None:
        return allocate_proportional(supply_df, demand_df, item_col, qty_col,
                                     price_col, id_col, date_col, reduction_rate)

    demand_df = demand_df.copy()
    demand_df['_is_detailed'] = demand_df[id_col].isin(detailed_ids)

    # Compute reduction rate from undetailed demand value
    undetailed = demand_df[~demand_df['_is_detailed']]
    detailed = demand_df[demand_df['_is_detailed']]

    if reduction_rate is None:
        undetailed_total = undetailed[qty_col].sum()
        detailed_total = detailed[qty_col].sum()
        if detailed_total > 0:
            reduction_rate = min(undetailed_total / detailed_total, 0.99)
        else:
            reduction_rate = 0.0

    # Step 1: Reduce detailed demand
    detailed_result = detailed.copy()
    detailed_result['allocated_qty'] = (detailed[qty_col] * (1 - reduction_rate)).round(4)
    if price_col and price_col in detailed.columns:
        detailed_result['allocated_value'] = (detailed_result['allocated_qty'] * detailed[price_col]).round(0)
    else:
        detailed_result['allocated_value'] = detailed_result['allocated_qty']

    # Step 2: Compute remaining stock
    detailed_usage = detailed_result.groupby(item_col)['allocated_qty'].sum()
    all_usage = detailed_usage

    # Step 3: Allocate undetailed demand from remaining stock
    undetailed_rows = []
    for _, d in undetailed.iterrows():
        row = d.to_dict()
        item = d[item_col]

        # Available = original stock - detailed usage for this item
        item_stock = supply_df[supply_df[item_col] == item][qty_col].sum()
        item_used = all_usage.get(item, 0)
        available = max(item_stock - item_used, 0)

        requested = d[qty_col]
        allocated = min(requested, available)
        item_used += allocated  # track for next iteration
        if item in all_usage.index:
            all_usage[item] = item_used
        else:
            all_usage[item] = item_used

        row['allocated_qty'] = round(allocated, 4)
        if price_col and price_col in d:
            row['allocated_value'] = round(allocated * d[price_col], 0)
        else:
            row['allocated_value'] = round(allocated, 0)
        undetailed_rows.append(row)

    undetailed_result = pd.DataFrame(undetailed_rows)

    # Combine
    allocation = pd.concat([detailed_result, undetailed_result], ignore_index=True)
    allocation = allocation.drop(columns=['_is_detailed'], errors='ignore')

    balance = _compute_balance(supply_df, allocation, item_col, qty_col)

    # Verify no negative
    negative = balance[balance['remaining'] < -0.001]
    if not negative.empty:
        print(f"WARNING: {len(negative)} items negative. Retrying with higher reduction...")
        return allocate_hybrid(supply_df, demand_df.drop(columns=['_is_detailed'], errors='ignore'),
                               item_col, qty_col, date_col, price_col, id_col,
                               detailed_ids, reduction_rate + 0.01)

    return {
        'allocation': allocation,
        'balance': balance,
        'reduction_rate': reduction_rate,
        'detailed_count': len(detailed),
        'undetailed_count': len(undetailed)
    }


def _compute_balance(supply_df, allocation_df, item_col, qty_col):
    """Compute per-item balance: opening, issued, remaining."""
    opening = supply_df.groupby(item_col)[qty_col].sum().reset_index()
    opening.columns = [item_col, 'opening_qty']

    issued = allocation_df.groupby(item_col)['allocated_qty'].sum().reset_index()
    issued.columns = [item_col, 'issued_qty']

    balance = opening.merge(issued, on=item_col, how='outer').fillna(0)
    balance['remaining'] = balance['opening_qty'] - balance['issued_qty']
    return balance


def verify_constraints(allocation_df, supply_df, item_col, qty_col,
                       issue_date_col=None, receipt_date_col=None):
    """
    Verify hard constraints. Returns dict with pass/fail per constraint.
    """
    results = {'no_negative_stock': True, 'date_constraint': True, 'errors': []}

    # 1. No negative stock
    opening = supply_df.groupby(item_col)[qty_col].sum()
    issued = allocation_df.groupby(item_col)['allocated_qty'].sum()
    for item in issued.index:
        avail = opening.get(item, 0)
        if issued[item] > avail + 0.01:
            results['no_negative_stock'] = False
            results['errors'].append(f"Item {item}: issued {issued[item]:.2f} > available {avail:.2f}")

    # 2. Issue date >= receipt date
    if issue_date_col and receipt_date_col:
        for _, row in allocation_df.iterrows():
            if pd.notna(row.get(issue_date_col)) and pd.notna(row.get(receipt_date_col)):
                if row[issue_date_col] < row[receipt_date_col]:
                    results['date_constraint'] = False
                    results['errors'].append(
                        f"Date violation: {row.get(item_col, '?')} issue={row[issue_date_col]} < receipt={row[receipt_date_col]}"
                    )

    return results
