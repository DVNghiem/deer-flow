---
name: inventory-fifo-allocation
description: >
  Inventory allocation and stock distribution with FIFO constraints. Use when the
  user needs to allocate stock, raw materials, finished goods, or any inventory
  items to orders, invoices, production batches, or consumption records while
  enforcing hard constraints: no negative stock and issue date must be on or
  after receipt date. Handles Excel files with arbitrary sheet structures and
  column names. Triggers on: phan bo ton kho, xuat kho, nhap xuat ton, FIFO
  allocation, stock allocation, inventory balance, cham ton kho, can doi ton
  kho, phan bo NVL, phan bo nguyen vat lieu, ton kho am, or any inventory
  allocation task with date and quantity constraints.
---

# Inventory FIFO Allocation

Generic framework for allocating inventory stock to demand records with FIFO
and no-negative-stock constraints. Works with any Excel structure.

## Core Principle

Inventory is a pool. Demand records consume from the pool. Two rules are sacred:

1. **No negative stock** -- cumulative issued quantity for each item cannot
   exceed available quantity.
2. **Issue date >= receipt date** -- stock can only be issued on or after the
   date it was received (FIFO).

Everything else is flexible: reduction rates, priority rules, proportional
scaling, etc.

## Step 1: Map the Data

Before any allocation, identify three things in the user's Excel:

| Concept | What to look for | Flexible mapping |
|---------|-----------------|------------------|
| **Supply** (stock) | Receipts, opening stock, purchases, nhap kho, ton dau ky | Any row with item code + quantity + date + unit price |
| **Demand** (consumption) | Orders, invoices, BOM lines, xuat kho, production needs | Any row with item code + required quantity + date |
| **Item key** | Material code, SKU, product ID, ma NVL, ma hang | The column that joins supply and demand |

Read the file. Use `pd.ExcelFile` to list sheets. Inspect headers. Ask the user
only if the mapping is ambiguous.

## Step 2: Choose Allocation Strategy

Select based on the problem structure:

### Strategy A: Proportional Reduction (Uniform Scale Down)
**When**: Total demand exceeds total supply. Need to cut all demand by same
percentage so everyone gets something.

```
reduction_rate = 1 - (total_supply / total_demand)
allocated_qty = original_qty * (1 - reduction_rate)
```

**Use for**: Invoice material allocation, budget distribution, quota sharing.

### Strategy B: FIFO Sequential (First-Come-First-Served)
**When**: Each demand record has a date. Earlier records consume first.

```
Sort demand by date ascending
For each demand record:
    Consume from oldest available stock first
    If stock runs out, stop (record gets partial or nothing)
```

**Use for**: Warehouse pick lists, production material issuance, consumable
tracking.

### Strategy C: Hybrid (Proportional + Top-Up)
**When**: Most demand records have BOM/detail, but some lack breakdown.
Reduce the detailed ones proportionally to fund the undetailed ones.

```
1. Reduce all detailed demand by rate R
2. Use saved stock to fulfill undetailed demand via FIFO
3. Verify no negative stock
```

**Use for**: The NVL-by-invoice pattern -- some invoices have material specs,
some only have total value.

## Step 3: Apply Date Constraint

After quantity allocation, verify: **issue_date >= receipt_date** for every
allocation line.

If violation:
- Option 1: Shift issue_date forward to match receipt_date
- Option 2: Reallocate using later-received stock
- Option 3: If no valid stock exists, record gets zero (logged, not dropped)

## Step 4: Verify Hard Constraints

```python
def verify(allocation_df, stock_df):
    # Constraint 1: No negative stock
    for item in items:
        total_issued = allocation_df[allocation_df.item == item].qty.sum()
        total_available = stock_df[stock_df.item == item].qty.sum()
        assert total_issued <= total_available + epsilon

    # Constraint 2: Issue date >= receipt date
    for _, row in allocation_df.iterrows():
        assert row.issue_date >= row.receipt_date
```

If verification fails, increase reduction rate (Strategy A) or re-sort and
re-allocate (Strategy B). Retry with adjusted parameters.

## Step 5: Output

Generate Excel with these sheets (create what the user needs):

| Sheet | Content |
|-------|---------|
| Detail allocation | Per line: item, qty, unit price, amount, issue date |
| Summary by demand | Per demand record: requested, allocated, balance, status |
| Stock balance | Per item: opening, issued, remaining, remaining value |
| Shortage / exceptions | Records that could not be fully fulfilled |

## Python Template

See `scripts/allocation_engine.py` -- a generic allocation engine that
accepts supply and demand DataFrames and applies the chosen strategy. Adapt
column names and strategy parameters for each use case.

## Common Pitfalls

- **Do not drop records** -- every demand record must appear in output, even
  with zero allocation. Mark status clearly.
- **Do not hardcode column names** -- read actual headers from the file.
- **Watch for NaN in numeric columns** -- use `fillna(0)` before math.
- **Date format ambiguity** -- use `pd.to_datetime` with `dayfirst=True` for
  dd/mm/yyyy formats common in Vietnam.
- **Unit mismatch** -- supply and demand must use the same unit per item.
