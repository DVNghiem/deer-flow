# Detailed Reconciliation Type Procedures

Reference guide for accounting reconciliation procedures under Vietnamese accounting standards. This document supplements the main SKILL.md and provides step-by-step procedures for each reconciliation type.

**Legal References:**
- Law 88/2015/QH13 (Accounting Law)
- Circular 99/2025/TT-BTC (Enterprise Accounting Regime, effective 01/01/2026)
- Decree 123/2020/ND-CP (Invoices and Documents)
- Decision 48/2006/QD-BTC (Chart of Accounts)

---

## Table of Contents

1. [Bank Reconciliation](#1-bank-reconciliation)
2. [Accounts Payable Reconciliation](#2-accounts-payable-reconciliation)
3. [Accounts Receivable Reconciliation](#3-accounts-receivable-reconciliation)
4. [Inventory Reconciliation](#4-inventory-reconciliation)
5. [Fixed Assets Reconciliation](#5-fixed-assets-reconciliation)
6. [Intercompany Reconciliation](#6-intercompany-reconciliation)

---

## 1. Bank Reconciliation

### Applicable Accounts (per Circular 99/2025)
- TK 1121 — Tiền gửi ngân hàng VND (Cash in bank accounts - VND)
- TK 1122 — Tiền gửi ngân hàng ngoại tệ (Cash in bank accounts - Foreign currency)

### Required Documents

| Document | Source | Per Decree 123/2020/ND-CP |
|----------|--------|---------------------------|
| Bank statement (Sao kê tài khoản) | Bank | Article 4, Section 2 |
| Cash book / Bank book (Sổ tiền gửi) | Company | Law 88/2015/QH13 Article 16 |
| Payment vouchers (Phiếu chi) | Company | Article 4, Section 3 |
| Collection vouchers (Phiếu thu) | Company | Article 4, Section 3 |
| Bank transfer slips (UNC, Lệnh chuyển tiền) | Bank | — |

### Step-by-Step Procedure

**Step 1: Obtain Bank Statement**
```
1. Request bank statement from bank for the accounting period
2. Verify bank statement covers the exact period required
3. Note opening and closing balances
4. Record all transaction dates, descriptions, and amounts
```

**Step 2: Obtain Cash/Bank Book**
```
1. Extract all entries from TK 1121 and/or TK 1122 for the period
2. Verify book balance at period start and end
3. Note all transaction references (cheque numbers, transfer IDs)
```

**Step 3: Compare Opening Balances**
```
1. Verify book opening balance = bank opening balance
2. If different, carry forward prior period's unreconciled items
3. Document any adjustments from prior period
```

**Step 4: Match Transactions**

| Match Type | Criteria | Action |
|------------|----------|--------|
| Exact match | Date + Amount + Reference | Mark as RECONCILED |
| Date tolerance | ±3 days + Exact amount | Accept with note |
| Partial match | Amount partially matches | Flag for investigation |
| No match | Cannot match | Add to unreconciled list |

**Step 5: Identify Timing Differences**

Common timing differences per Circular 99/2025 guidance:

| Item | In Book | Not Yet in Bank | In Bank | Not Yet in Book |
|------|---------|-----------------|---------|----------------|
| Cheques issued (Séc đã phát hành) | Yes | Yes | No | — |
| Cheques deposited (Séc gửi ngân hàng) | Yes | — | No | Yes |
| Bank transfers sent (Chuyển khoản đi) | Yes | Yes | No | — |
| Bank transfers received (Chuyển khoản đến) | Yes | — | No | Yes |
| Bank fees (Phí ngân hàng) | No | — | Yes | Yes |
| Interest earned (Lãi tiền gửi) | No | — | Yes | Yes |

**Step 6: Calculate Reconciliation**

```
Bank Statement Closing Balance
± Outstanding cheques (not yet presented)
± Deposits in transit (not yet credited)
± Bank errors (if any)
= Adjusted Bank Balance

Book Cash/Bank Account Closing Balance
± Adjustments required
= Adjusted Book Balance

Adjusted Bank Balance = Adjusted Book Balance ✓
```

**Step 7: Document Discrepancies**

| Discrepancy Type | Classification | Action |
|------------------|----------------|--------|
| Outstanding cheque > 90 days | TIMING_DIFFERENCE | Review with Finance Manager |
| Deposit in transit > 30 days | TIMING_DIFFERENCE | Follow up with bank |
| Bank fee not recorded | DOCUMENTATION_GAP | Record immediately |
| Unrecorded interest | DOCUMENTATION_GAP | Record immediately |
| Amount mismatch | AMOUNT_VARIANCE | Investigate |
| Unknown transaction | UNCLASSIFIED | Escalate |

**Hypothetical example only:**

```
Bank Statement Closing: 500,000,000 VND
- Outstanding cheque #12345: (50,000,000 VND)
+ Deposit in transit: 25,000,000 VND
= Adjusted Bank Balance: 475,000,000 VND

Book Balance: 475,000,000 VND
+ Unrecorded bank fee: 0 VND (already recorded)
= Adjusted Book Balance: 475,000,000 VND

RECONCILIATION COMPLETE ✓
```

---

## 2. Accounts Payable Reconciliation

### Applicable Accounts (per Circular 99/2025)
- TK 331 — Phải trả cho người bán (Accounts payable - Suppliers)
  - TK 3311 — TK 331 (VND suppliers)
  - TK 3312 — TK 331 (Foreign currency suppliers)

### Required Documents

| Document | Source | Per Decree 123/2020/ND-CP |
|----------|--------|---------------------------|
| Purchase invoices (Hóa đơn GTGT / Hóa đơn bán hàng) | Supplier | Article 4, Section 1 |
| Goods received notes (Phiếu nhập kho) | Company | Article 4, Section 3 |
| Payment vouchers (Phiếu chi) | Company | Article 4, Section 3 |
| Vendor statements (Bảng đối chiếu công nợ) | Supplier | — |
| Purchase orders (Đơn đặt hàng) | Company | — |
| Contracts (Hợp đồng mua hàng) | Company | — |

### Step-by-Step Procedure

**Step 1: Prepare AP Aging Report**
```
1. Generate AP aging by vendor from subledger
2. Group by aging buckets:
   - Current (0-30 days)
   - 31-60 days overdue
   - 61-90 days overdue
   - Over 90 days overdue
3. Calculate total AP balance per vendor
4. Verify total matches GL (TK 331) balance
```

**Step 2: Request Vendor Statements**
```
1. Send statement requests to all vendors with balances
2. Request confirmation of:
   - Invoice numbers and dates
   - Payment references
   - Credit notes
   - Outstanding balance
3. Track responses received
```

**Step 3: Match by Vendor**

For each vendor with statement:

```
1. Start with vendor's stated balance
2. Match company records against vendor statement
3. Match payments made (by payment reference, date, amount)
4. Match invoices received (by invoice number, date, amount)
5. Identify discrepancies at each step
```

**Step 4: Match by Invoice**

| Match Type | Criteria | Action |
|------------|----------|--------|
| Exact | Invoice number + Amount | Confirm both sides |
| Date variance | Invoice date ±5 days + Amount | Accept with note |
| Partial payment | Payment < Invoice amount | Calculate remaining balance |
| Credit note | Credit note number + Amount | Match to original invoice |
| Payment without invoice | Payment recorded, no invoice | Flag for investigation |
| Invoice without payment | Invoice recorded, no payment | Add to aging |

**Step 5: Common Discrepancies**

| Discrepancy | Classification | Action |
|-------------|----------------|--------|
| Invoice on statement not in books | UNMATCHED_SOURCE | Record AP immediately |
| Payment made but not credited | TIMING_DIFFERENCE | Follow up with vendor |
| Credit note not recorded | DOCUMENTATION_GAP | Request credit note documentation |
| Early payment discount taken | AMOUNT_VARIANCE | Verify against contract terms |
| Price difference on invoice | AMOUNT_VARIANCE | Resolve with vendor |
| Wrong vendor charged | CLASSIFICATION_ERROR | Reclassify to correct vendor |
| Invoice in local currency vs FCY | CURRENCY_DIFFERENCE | Verify exchange rate used |

**Step 6: Resolve Discrepancies**

For each discrepancy:

```
1. Obtain supporting documentation
2. Contact vendor if required
3. Prepare adjusting entry if approved
4. Document resolution with evidence
5. For items over 90 days: review for write-off consideration
```

**Step 7: Reconcile to GL**

```
Vendor Stated Balances (per statements received):
  Total: XXX VND

Company Records (per subledger):
  Total: XXX VND

Differences:
  - Items in transit / processing: XXX VND
  - Statements not yet received: XXX VND
  - Unresolved discrepancies: XXX VND

Reconciling Amount: XXX VND
```

**Hypothetical example only:**

```
Vendor: Công ty TNHH XYZ (Tax Code: 0123456789)

Company Books:
  - Invoice #INV-001: 100,000,000 VND (15/01/2026)
  - Payment #PAY-001: 100,000,000 VND (20/01/2026) ✓ MATCHED
  - Invoice #INV-002: 50,000,000 VND (25/01/2026)
  Outstanding balance: 50,000,000 VND

Vendor Statement:
  - Invoice #INV-001: 100,000,000 VND (15/01/2026) ✓ PAID
  - Invoice #INV-002: 50,000,000 VND (25/01/2026) ✓ CONFIRMED
  Outstanding balance: 50,000,000 VND

RECONCILIATION COMPLETE ✓
```

---

## 3. Accounts Receivable Reconciliation

### Applicable Accounts (per Circular 99/2025)
- TK 131 — Phải thu khách hàng (Accounts receivable - Customers)
  - TK 1311 — TK 131 (VND customers)
  - TK 1312 — TK 131 (Foreign currency customers)

### Required Documents

| Document | Source | Per Decree 123/2020/ND-CP |
|----------|--------|---------------------------|
| Sales invoices (Hóa đơn GTGT) | Company | Article 4, Section 1 |
| Collection receipts (Phiếu thu) | Company | Article 4, Section 3 |
| Credit notes (Phiếu ghi giảm) | Company | Article 4, Section 3 |
| Customer confirmations (Xác nhận công nợ) | Customer | — |
| Delivery notes (Biên bản giao hàng) | Company | — |
| Collection follow-up records | Company | — |

### Step-by-Step Procedure

**Step 1: Prepare AR Aging Report**
```
1. Generate AR aging by customer from subledger
2. Group by aging buckets:
   - Current (0-30 days from due date)
   - 31-60 days overdue
   - 61-90 days overdue
   - Over 90 days overdue
3. Calculate total AR balance per customer
4. Verify total matches GL (TK 131) balance
```

**Step 2: Send Confirmation Requests**
```
1. Send confirmation requests to customers with significant balances
   - Priority: balances > 50,000,000 VND
   - All customers with balances > 30 days overdue
2. Request confirmation of:
   - Invoice numbers and dates
   - Payment references
   - Credit notes received
   - Outstanding balance
3. Track responses received
```

**Step 3: Match by Customer**

For each customer with confirmation:

```
1. Start with customer's stated balance
2. Match company records against confirmation
3. Match collections received (by receipt number, date, amount)
4. Match invoices issued (by invoice number, date, amount)
5. Identify discrepancies at each step
```

**Step 4: Match by Invoice**

| Match Type | Criteria | Action |
|------------|----------|--------|
| Exact | Invoice number + Amount | Confirm both sides |
| Date variance | Invoice date ±3 days + Amount | Accept with note |
| Partial payment | Payment < Invoice amount | Calculate remaining balance |
| Credit note | Credit note number + Amount | Match to original invoice |
| Collection not deposited | Payment recorded, not in bank | Investigate cash handling |
| Invoice not in customer records | Invoice issued, not confirmed | Contact customer |

**Step 5: Common Discrepancies**

| Discrepancy | Classification | Action |
|-------------|----------------|--------|
| Invoice issued not recorded by customer | TIMING_DIFFERENCE | Contact customer |
| Payment made not received by company | TIMING_DIFFERENCE | Check bank, follow up |
| Goods returned not processed as credit note | DOCUMENTATION_GAP | Issue credit note |
| Collection receipt not matched | TIMING_DIFFERENCE | Match to invoice |
| Early payment discount not recorded | AMOUNT_VARIANCE | Adjust if documented |
| Wrong customer charged | CLASSIFICATION_ERROR | Transfer to correct account |
| Uncollectible receivable | UNCLASSIFIED | Review for bad debt provision |

**Step 6: Bad Debt Assessment**

Per Circular 99/2025/TT-BTC on provision for doubtful debts:

| Criteria | Provision Level |
|----------|-----------------|
| Over 90 days overdue | 30% of balance |
| Over 180 days overdue | 50% of balance |
| Over 360 days overdue | 100% of balance |
| Customer in bankruptcy/ dissolution | 100% of balance |

**Step 7: Reconcile to GL**

```
Customer Confirmed Balances (per confirmations received):
  Total: XXX VND

Company Records (per subledger):
  Total: XXX VND

Differences:
  - Customers not responding: XXX VND
  - Unresolved discrepancies: XXX VND
  - Bad debt provisions: XXX VND

Reconciling Amount: XXX VND
```

**Hypothetical example only:**

```
Customer: Công ty Cổ phần ABC (Tax Code: 9876543210)

Company Books:
  - Invoice #SI-001: 200,000,000 VND (10/01/2026) due 10/02/2026
  - Payment #CR-001: 200,000,000 VND (25/01/2026) ✓ MATCHED
  Outstanding balance: 0 VND

Customer Confirmation:
  - Invoice #SI-001: 200,000,000 VND (10/01/2026) ✓ PAID
  Outstanding balance: 0 VND

RECONCILIATION COMPLETE ✓
```

---

## 4. Inventory Reconciliation

### Applicable Accounts (per Circular 99/2025)
- TK 151 — Hàng mua đang đi đường (Goods in transit)
- TK 152 — Nguyên liệu, vật liệu (Raw materials)
- TK 153 — Công cụ, dụng cụ (Tools, instruments)
- TK 154 — Chi phí sản xuất kinh doanh dở dang (Work in progress)
- TK 155 — Thành phẩm (Finished goods)
- TK 156 — Hàng hóa (Merchandise)

### Required Documents

| Document | Source | Per Decree 123/2020/ND-CP |
|----------|--------|---------------------------|
| Physical count sheets (Biên bản kiểm kê) | Count team | Article 4, Section 3 |
| Inventory movement report (Báo cáo biến động tồn kho) | System | — |
| Perpetual inventory records (Sổ tồn kho) | System | — |
| Goods received notes (Phiếu nhập kho) | Warehouse | — |
| Goods issue notes (Phiếu xuất kho) | Warehouse | — |
| Inventory valuation working papers | Accounting | — |

### Step-by-Step Procedure

**Step 1: Plan Physical Count**

```
1. Determine count date (ideally period-end or nearby)
2. Organize counting teams
3. Prepare count sheets with:
   - Item codes
   - Item descriptions
   - Unit of measure
   - Location/sublocation
4. Freeze movements during count (where possible)
5. Assign counting and supervisory roles
```

**Step 2: Conduct Physical Count**
```
1. Count each item in each location
2. Record on count sheets:
   - Item code
   - Counted quantity
   - Condition notes (damaged, expired, etc.)
3. Second count for high-value items
4. Supervisor verification
5. Record all count sheets with signatures
```

**Step 3: Obtain Perpetual Inventory Records**
```
1. Extract perpetual inventory as of count date
2. Include:
   - Opening balance
   - Receipts (purchases, returns in)
   - Issues (sales, usage, returns out)
   - Closing balance
3. Reconcile movements to source documents
```

**Step 4: Compare Physical to Perpetual**

| Variance Type | Calculation | Threshold |
|---------------|-------------|-----------|
| Quantity variance | |Physical Qty - Book Qty| | > 0 |
| Value variance | |Physical Value - Book Value| | > 0 |
| Unit cost difference | Different cost used | — |

**Step 5: Investigate Variances**

| Possible Cause | Investigation Steps |
|----------------|---------------------|
| Count error | Re-count; verify items in wrong location |
| Goods in transit | Check shipping/receiving dates |
| Consignment inventory | Verify ownership documentation |
| Damaged goods | Confirm quantity and condition |
| Theft/loss | Review access logs; escalate if material |
| Recording error | Recheck calculations and postings |
| Valuation error | Verify unit cost and method |

**Step 6: Common Discrepancies**

| Discrepancy | Classification | Action |
|-------------|----------------|--------|
| Quantity difference small | ROUNDING/COUNT_ERROR | Accept if < 0.1% |
| Damaged goods | INVENTORY_IMPAIRMENT | Record provision |
| Obsolete items | INVENTORY_IMPAIRMENT | Record provision |
| Consignment inventory | CLASSIFICATION | Verify ownership |
| Goods in transit | TIMING_DIFFERENCE | Document cut-off |
| Valuation method difference | VALUATION_VARIANCE | Review costing method |

**Step 7: Reconcile to GL**

```
Physical Count Value: XXX VND
± Goods in transit (not counted): XXX VND
± Consignment adjustments: XXX VND
± Valuation adjustments: XXX VND
= Adjusted Physical Value: XXX VND

Book Value (Perpetual): XXX VND
± Adjustments required: XXX VND
= Adjusted Book Value: XXX VND

Variance: XXX VND (0.XX%)
```

**Hypothetical example only:**

```
Item: Nguyên liệu A (Code: NLA-001)
Unit: KG
Unit Cost Method: Bình quân gia quyền

Perpetual Record:
  Opening: 1,000 KG @ 10,000 VND = 10,000,000 VND
  Receipts: 500 KG @ 11,000 VND = 5,500,000 VND
  Issues: 800 KG @ 10,625 VND = 8,500,000 VND
  Closing: 700 KG @ 10,625 VND = 7,437,500 VND

Physical Count:
  Counted: 695 KG
  Variance: 5 KG (0.71%)

Investigation: Count variance attributed to moisture loss (acceptable for raw materials)

RECONCILIATION COMPLETE with 5 KG variance documented
```

---

## 5. Fixed Assets Reconciliation

### Applicable Accounts (per Circular 99/2025)
- TK 211 — Tài sản cố định hữu hình (Tangible fixed assets)
- TK 213 — Tài sản cố định vô hình (Intangible fixed assets)
- TK 214 — Hao mòn tài sản cố định (Accumulated depreciation)
- TK 241 — Xây dựng cơ bản dở dang (Construction in progress)

### Required Documents

| Document | Source | Per Decree 123/2020/ND-CP |
|----------|--------|---------------------------|
| Asset register (Bảng theo dõi TSCĐ) | Company | Law 88/2015/QH13 |
| Asset acquisition documents | Company | — |
| Depreciation schedule | Company | — |
| Asset disposal documents | Company | — |
| Physical asset verification report | Count team | — |
| Asset improvement/repair records | Company | — |

### Step-by-Step Procedure

**Step 1: Obtain Asset Register**
```
1. Extract complete fixed asset register
2. Include for each asset:
   - Asset code
   - Asset description
   - Acquisition date
   - Original cost
   - Useful life
   - Depreciation method
   - Accumulated depreciation to date
   - Net book value
   - Location
   - Custodian
```

**Step 2: Obtain Depreciation Schedule**
```
1. Extract depreciation schedule for the period
2. Verify:
   - Opening accumulated depreciation
   - Depreciation charged this period
   - Disposals
   - Closing accumulated depreciation
3. Cross-check to GL (TK 214)
```

**Step 3: Verify to Source Documents**

For each major asset (cost > 10,000,000 VND):

```
1. Acquisition:
   - Purchase invoice
   - Goods received note
   - Capitalization approval
2. Subsequent expenditure:
   - Improvement vs. repair classification
   - Approval documentation
3. Disposal:
   - Disposal approval
   - Sale invoice (if sold)
   - Write-off approval (if scrapped)
```

**Step 4: Physical Verification**

For tangible fixed assets:

```
1. Plan physical verification schedule
2. For each asset in register:
   - Locate asset
   - Verify existence
   - Note condition
   - Note any location changes
3. Identify:
   - Assets not found
   - Unrecorded assets
   - Asset modifications
```

**Step 5: Common Discrepancies**

| Discrepancy | Classification | Action |
|-------------|----------------|--------|
| Asset not found | UNCLASSIFIED | Investigate; may require write-off |
| Useful life misestimate | VALUATION_VARIANCE | Review depreciation policy |
| Not yet capitalized | DOCUMENTATION_GAP | Capitalize if criteria met |
| Disposal not recorded | DOCUMENTATION_GAP | Record disposal entry |
| Wrong depreciation method | CLASSIFICATION_ERROR | Correct if material |
| Double depreciation | AMOUNT_VARIANCE | Correct immediately |
| Asset improvement capitalized vs. expensed | CLASSIFICATION | Review capitalization policy |

**Step 6: Reconcile to GL**

```
Asset Register Summary:
  TK 211 Opening: XXX VND
  + Acquisitions: XXX VND
  - Disposals: XXX VND
  ± Adjustments: XXX VND
  = TK 211 Closing: XXX VND

TK 211 in GL: XXX VND
Variance: XXX VND

Accumulated Depreciation (TK 214):
  Register Closing: XXX VND
  GL Balance: XXX VND
  Variance: XXX VND

Net Book Value:
  Register: XXX VND
  GL: XXX VND
  Variance: XXX VND
```

**Step 7: Review Depreciation Rates**

Per Circular 99/2025/TT-BTC standard rates:

| Asset Type | Minimum Useful Life |
|------------|--------------------|
| Buildings | 5-50 years |
| Machinery & equipment | 3-15 years |
| Motor vehicles | 6-10 years |
| Office equipment | 3-10 years |
| Intangible assets | Per legal useful life |
| Software | 2-5 years |

**Hypothetical example only:**

```
Asset: Máy photocopy Canon IR 6570
Code: TS-001
Acquisition: 01/03/2023
Cost: 150,000,000 VND
Useful life: 8 years
Depreciation method: Straight-line

Asset Register:
  Cost: 150,000,000 VND
  Accumulated depreciation (Jan 2026): 54,687,500 VND
  Net book value: 95,312,500 VND

GL (TK 211 / TK 214):
  TK 211: 150,000,000 VND ✓
  TK 214: 54,687,500 VND ✓

Physical Verification:
  Asset found at location: Phòng Kế toán
  Condition: Good
  Tag present: TS-001

RECONCILIATION COMPLETE ✓
```

---

## 6. Intercompany Reconciliation

### Applicable Context
- Parent-subsidiary relationships
- Sister-sister relationships
- Related party transactions within groups

### Required Documents

| Document | Source | Notes |
|----------|--------|-------|
| Intercompany invoice | Originating entity | Per Decree 123/2020/ND-CP |
| Intercompany agreement | All entities | Transfer pricing documentation |
| Confirmation from counterpart | Counterparty entity | |
| Elimination entries | Consolidation team | |
| Transfer pricing documentation | All entities | Required for transactions > threshold |

### Step-by-Step Procedure

**Step 1: Identify Intercompany Transactions**
```
1. From each entity's books:
   - List all transactions with related entities
   - Include sales, purchases, loans, services, dividends
   - Note amounts, dates, and descriptions
2. Build intercompany transaction matrix
```

**Step 2: Match Between Entities**

For each intercompany transaction:

```
1. Match transaction from Entity A to Entity B
2. Verify:
   - Amount matches (accounting currency)
   - Date matches (within tolerance)
   - Description matches
   - No duplication
```

**Step 3: Common Discrepancies**

| Discrepancy | Classification | Action |
|-------------|----------------|--------|
| Transaction in one entity not in other | TIMING_DIFFERENCE | Identify cutoff timing |
| Different amounts recorded | AMOUNT_VARIANCE | Check exchange rates, rounding |
| Wrong entity recorded | CLASSIFICATION_ERROR | Correct in appropriate entity |
| Revenue recognition timing | TIMING_DIFFERENCE | Align cutoff policies |
| Unrealized profit in inventory | ELIMINATION_REQUIRED | Calculate and eliminate |
| Loan interest rate difference | AMOUNT_VARIANCE | Verify against agreement |

**Step 4: Transfer Pricing Verification**

Per regulations on related party transactions:

```
1. Verify transaction is at arm's length
2. Document transfer pricing method used
3. Ensure within arm's length range
4. Flag if documentation insufficient
```

**Step 5: Calculate Elimination Entries**

For consolidated reporting:

```
1. Unrealized profit elimination:
   - Identify upstream sales with unsold inventory
   - Calculate profit margin
   - Eliminate to extent of unsold inventory

2. Intercompany balance elimination:
   - Match payable and receivable
   - Eliminate to zero

3. Intercompany transaction elimination:
   - Match revenue and expense
   - Eliminate to zero
```

**Step 6: Reconcile to Consolidation**

```
Entity A Books:
  Intercompany receivable from B: XXX VND

Entity B Books:
  Intercompany payable to A: XXX VND

Variance: XXX VND
Reason: [Timing difference / Classification error / etc.]

Elimination Entry Required:
  DR: Intercompany payable XXX
  CR: Intercompany receivable XXX
```

**Hypothetical example only:**

```
Transaction: Management fee
Period: January 2026
Entities: Parent (A) → Subsidiary (B)

Entity A (Parent):
  - Invoice #IC-2026-001: 30,000,000 VND
  - Revenue recognized: 30,000,000 VND
  - Receivable from B: 30,000,000 VND

Entity B (Subsidiary):
  - Invoice received: 30,000,000 VND
  - Expense recognized: 30,000,000 VND
  - Payable to A: 30,000,000 VND

RECONCILIATION COMPLETE ✓
Intercompany balance eliminated in consolidation
```

---

## Quick Reference: Classification Codes

| Code | Classification | Description |
|------|----------------|-------------|
| TEMPORARY_TIMING | Timing Difference | Transaction recorded in one period, not another |
| AMOUNT_VARIANCE | Amount Variance | Amounts differ between sources |
| ROUNDING | Rounding | Difference within acceptable rounding threshold |
| DOCUMENTATION_GAP | Documentation Gap | Missing or incomplete documentation |
| CLASSIFICATION_ERROR | Classification Error | Wrong account or category |
| UNCLASSIFIED | Unclassified | Cannot be classified; requires investigation |

---

## Document Retention

Per Law 88/2015/QH13 Article 15:

| Document Type | Retention Period |
|---------------|------------------|
| Accounting documents | 10 years minimum |
| Asset registers | Life of asset + 5 years |
| Bank reconciliations | 10 years |
| Vendor/customer statements | 10 years |
| Physical count reports | 10 years |

---

*This document is a reference guide only. Consult with qualified accounting professionals for complex situations. All examples are hypothetical and for illustrative purposes only.*
