---
name: accounting-reconciliation
description: Reconcile ledger entries, bank statements, receivables, payables per Vietnamese accounting regime
version: 1.0.0
domain: vietnam-accounting
---

# Accounting Reconciliation Skill

## Purpose

This skill performs accounting reconciliation following Vietnamese accounting standards and regulations. It matches source documents against ledger entries, identifies discrepancies, classifies differences according to Vietnamese accounting taxonomy, and generates audit-ready reconciliation reports.

**Legal Framework:**
- Law 88/2015/QH13 (Accounting Law) — governing principles for accounting records
- Circular 99/2025/TT-BTC (Enterprise Accounting Regime) — effective 01/01/2026, replaces Circular 200/2014/TT-BTC
- Decree 123/2020/ND-CP — invoices and supporting documentation requirements

## When to Use

- Month-end or quarter-end closing reconciliations
- Year-end financial statement preparation
- Bank statement reconciliation for cash management
- Accounts payable aging analysis and vendor payment reconciliation
- Accounts receivable confirmation and collection tracking
- Inventory count verification against perpetual records
- Fixed asset register validation against depreciation schedules
- Intercompany transaction elimination for consolidated statements
- Audit preparation and supporting documentation assembly

## When Not to Use

- Tax calculation or tax filing (use tax-specialist skill instead)
- Financial statement interpretation or analysis (use financial-analysis skill)
- Budget variance analysis (use budgeting skill)
- Currency translation (use fx-reconciliation skill)
- Consolidation of subsidiaries with complex equity structures (use consolidation-skill)
- Real-time transaction posting (use transaction-entry skill)

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `ledger_data` | JSON/CSV | Yes | General ledger entries with account codes, dates, amounts, descriptions |
| `source_documents` | JSON/Array | Yes | Invoices, receipts, payment vouchers per Decree 123/2020/ND-CP |
| `bank_statements` | JSON/CSV | No | Bank statement transactions (required for bank reconciliation) |
| `reconciliation_type` | Enum | Yes | One of: `bank`, `accounts_payable`, `accounts_receivable`, `inventory`, `fixed_assets`, `intercompany` |
| `accounting_period` | Object | Yes | `{ start_date, end_date }` in DD/MM/YYYY format |
| `company_info` | Object | No | Company details for report header (name, tax_code, address) |

### Input Validation

Before processing, validate:

1. **Date format** — All dates must be DD/MM/YYYY. Reject MM/DD/YYYY or YYYY-MM-DD inputs.
2. **Currency** — Amounts must be in VND. Foreign currency transactions require separate handling.
3. **Account codes** — Must conform to Circular 99/2025/TT-BTC chart of accounts.
4. **Document references** — Source documents must include invoice numbers per Decree 123/2020/ND-CP Article 4.

**Hypothetical example only:**
```json
{
  "ledger_data": [
    {
      "entry_id": "LE-2026-0001",
      "date": "15/01/2026",
      "account_code": "1121",
      "account_name": "Tiền gửi ngân hàng VND",
      "description": "Thu tiền bán hàng",
      "debit": 50000000,
      "credit": 0,
      "counterparty": "Công ty TNHH ABC"
    }
  ],
  "reconciliation_type": "bank",
  "accounting_period": {
    "start_date": "01/01/2026",
    "end_date": "31/01/2026"
  }
}
```

## Step-by-Step Workflow

### Step 1: Identify Reconciliation Type

Based on `reconciliation_type`, select the appropriate procedure:

| Type | Primary Matching Key | Secondary Key |
|------|---------------------|--------------|
| `bank` | Transaction date + amount | Reference number |
| `accounts_payable` | Vendor invoice number | Vendor tax code + date |
| `accounts_receivable` | Customer invoice number | Customer tax code + date |
| `inventory` | Item code + quantity | Batch/lot number |
| `fixed_assets` | Asset code | Serial number |
| `intercompany` | Transaction ID | Counterparty entity code |

### Step 2: Gather Supporting Documents

Collect per Decree 123/2020/ND-CP:

- **For revenue/receipts:** Sales invoices (Hóa đơn GTGT), collection receipts (Phiếu thu)
- **For payments:** Purchase invoices, payment vouchers (Phiếu chi), bank transfer slips
- **For adjustments:** Adjustment vouchers (Chứng từ điều chỉnh) with written justification

Flag any missing required documents per Article 4 of Decree 123/2020/ND-CP.

### Step 3: Match Entries

Apply matching algorithm:

```
For each ledger entry:
  1. Search source documents for exact match on primary key
  2. If no exact match, search with tolerance on date (±3 days) + exact amount
  3. If still unmatched, search for partial amount matches
  4. Flag as: MATCHED | PARTIAL_MATCH | UNMATCHED_LEDGER | UNMATCHED_SOURCE
```

### Step 4: Identify Differences

Calculate discrepancies:

| Type | Calculation | Threshold |
|------|-------------|-----------|
| Timing difference | Entry exists in one source but not other | Always flag |
| Amount difference | |ledger_amount - source_amount| | > 0 VND |
| Rounding difference | Amount differs by ≤ 100 VND | Accept if documented |
| Classification difference | Entry exists but in wrong account | Always flag |

### Step 5: Classify Discrepancies

Per Circular 99/2025/TT-BTC, classify discrepancies:

```
CLASSIFICATION_HIERARCHY:
├── TEMPORARY_TIMING_DIFFERENCE
│   ├── Bank not yet credited
│   ├── Cheque issued but not presented
│   └── Invoice issued but not recorded
├── AMOUNT_VARIANCE
│   ├── Rounding (≤ 100 VND)
│   ├── Pricing error (invoice vs contract)
│   └── Calculation error
├── DOCUMENTATION_GAP
│   ├── Missing source document
│   ├── Missing approval
│   └── Incorrect account coding
└── UNCLASSIFIED
    └── Requires investigation
```

### Step 6: Investigate (Flag for Manual Review)

**CRITICAL — ANTI-HALLUCINATION RULE:**

> **Never infer fraud, embezzlement, or intentional misconduct from discrepancies.**
> Flag ALL unexplained differences as `UNCLASSIFIED` for human investigation.
> The reconciliation skill identifies and classifies; humans determine cause.

Investigate each `UNCLASSIFIED` discrepancy by:

1. Checking for data entry errors
2. Verifying document authenticity (noting this requires specialized expertise)
3. Confirming authorization
4. Checking for timing of transactions near period-end

Do NOT conclude: "This appears to be fraud." Instead: "This discrepancy of X VND on date Y is unclassified and requires investigation."

### Step 7: Document Reconciliation Work

Per Law 88/2015/QH13 Article 15, maintain documentation:

- Reconciliation preparer name and signature
- Reconciliation reviewer name and signature
- Date of preparation and review
- Evidence of investigation of discrepancies
- Management approval for write-offs or adjustments

### Step 8: Generate Report

Output structured JSON report (see Output Format below).

## Reconciliation Types

### Bank Reconciliation

Matches: Bank statement vs. cash/bank ledger account (TK 112)

**Key documents:**
- Bank statement (Sao kê tài khoản)
- Cash book (Sổ quỹ tiền mặt) or bank book (Sổ tiền gửi ngân hàng)

**Common discrepancies:**
- Outstanding cheques (Séc đang lưu hành)
- Bank fees not yet recorded
- Direct transfers not yet notified
- Deposits in transit (Tiền gửi chuyển khoản đang xử lý)

### Accounts Payable Reconciliation

Matches: Vendor invoices vs. AP subledger vs. GL

**Key documents:**
- Purchase invoices (Hóa đơn mua hàng)
- Goods received notes (Phiếu nhập kho)
- Payment vouchers (Phiếu chi)

**Common discrepancies:**
- Invoice received but goods not yet received (hàng chưa về)
- Payment made but invoice not yet received
- Goods returned but credit note not processed
- Early payment discounts (chiết khấu thanh toán)

### Accounts Receivable Reconciliation

Matches: Customer invoices vs. AR subledger vs. GL

**Key documents:**
- Sales invoices (Hóa đơn GTGT)
- Collection receipts (Phiếu thu)
- Credit notes (Phiếu ghi giảm)

**Common discrepancies:**
- Invoice issued but delivery not confirmed
- Collection recorded in cash book but not yet deposited
- Credit notes not yet matched
- Bad debt write-off pending approval

### Inventory Reconciliation

Matches: Physical count vs. perpetual inventory vs. GL

**Key documents:**
- Physical count sheets (Biên bản kiểm kê)
- Inventory movement reports
- Valuation calculations

**Common discrepancies:**
- Count errors
- Goods in transit
- Consignment inventory
- Damaged/spoiled goods
- Valuation method differences (FIFO vs. weighted average)

### Fixed Assets Reconciliation

Matches: Asset register vs. GL accumulated depreciation vs. physical assets

**Key documents:**
- Asset register (Bảng theo dõi TSCĐ)
- Depreciation schedule
- Asset acquisition/disposal documents

**Common discrepancies:**
- Fully depreciated assets still in use (no issue)
- Assets under construction not yet capitalized
- Disposals not recorded
- Useful life misestimation

### Intercompany Reconciliation

Matches: Parent and subsidiary books for elimination entries

**Key documents:**
- Intercompany invoices
- Transfer pricing documentation
- Elimination entries

**Common discrepancies:**
- Timing differences in intercompany billing
- Unrealized profit in inventory
- Different cutoff dates
- Currency translation differences

## Output Format

```json
{
  "reconciliation_report": {
    "report_id": "REC-{YYYYMMDD}-{SEQUENCE}",
    "prepared_by": "{name}",
    "reviewed_by": "{name}",
    "preparation_date": "DD/MM/YYYY",
    "review_date": "DD/MM/YYYY",
    "accounting_period": {
      "start_date": "DD/MM/YYYY",
      "end_date": "DD/MM/YYYY"
    },
    "reconciliation_type": "{type}",
    "scope": {
      "total_ledger_entries": 0,
      "total_source_documents": 0,
      "total_bank_transactions": 0
    },
    "matched_entries": [
      {
        "match_id": "MATCH-001",
        "ledger_entry_id": "LE-XXX",
        "source_document_id": "DOC-XXX",
        "match_type": "EXACT",
        "amount": 0,
        "date": "DD/MM/YYYY",
        "match_confidence": "HIGH"
      }
    ],
    "partial_matches": [
      {
        "match_id": "PARTIAL-001",
        "ledger_entry_id": "LE-XXX",
        "source_document_id": "DOC-XXX",
        "ledger_amount": 0,
        "document_amount": 0,
        "difference": 0,
        "difference_type": "ROUNDING"
      }
    ],
    "unmatched_entries": {
      "unmatched_ledger": [
        {
          "entry_id": "LE-XXX",
          "date": "DD/MM/YYYY",
          "account_code": "XXXX",
          "description": "...",
          "amount": 0,
          "debit_credit": "DEBIT|CREDIT",
          "reason": "SOURCE_NOT_FOUND"
        }
      ],
      "unmatched_source": [
        {
          "document_id": "DOC-XXX",
          "date": "DD/MM/YYYY",
          "invoice_number": "XXX",
          "amount": 0,
          "counterparty": "...",
          "reason": "LEDGER_NOT_FOUND"
        }
      ]
    },
    "discrepancies": [
      {
        "discrepancy_id": "DISC-001",
        "entry_id": "LE-XXX",
        "discrepancy_type": "CLASSIFICATION",
        "classification": "DOCUMENTATION_GAP",
        "subclassification": "MISSING_SOURCE_DOCUMENT",
        "amount": 0,
        "description": "...",
        "investigation_status": "PENDING",
        "investigation_notes": "...",
        "resolution": null,
        "escalation_required": false
      }
    ],
    "summary": {
      "total_ledger_amount": 0,
      "total_source_amount": 0,
      "total_matched_amount": 0,
      "total_unmatched_amount": 0,
      "total_discrepancy_amount": 0,
      "match_rate_percentage": 0.0,
      "items_requiring_investigation": 0,
      "items_escalated": 0
    },
    "status": "DRAFT|IN_REVIEW|APPROVED|COMPLETED",
    "approval": {
      "approver_name": "...",
      "approval_date": "DD/MM/YYYY",
      "comments": "..."
    },
    "legal_references": [
      "Law 88/2015/QH13 Article 15",
      "Circular 99/2025/TT-BTC Chapter III",
      "Decree 123/2020/ND-CP Article 4"
    ]
  }
}
```

## Missing Data Handling

| Scenario | Handling |
|----------|----------|
| Missing bank statement | Cannot complete bank reconciliation. Flag as `BLOCKED` and request data. |
| Missing source document | Classify as `DOCUMENTATION_GAP`, flag for manual retrieval |
| Missing GL entry | Add to `unmatched_source`, do not create GL entry automatically |
| Partial period data | Complete reconciliation for available period, document coverage gap |
| Missing approval | Hold report in `DRAFT` status until approval obtained |

## Error Handling

| Error | Response |
|-------|----------|
| Invalid date format | Reject with clear error message specifying expected format (DD/MM/YYYY) |
| Invalid account code | Flag non-conforming codes, suggest alternatives per Circular 99/2025 |
| Duplicate entries detected | Report duplicates, do not auto-deduplicate |
| Negative amounts in source | Flag for review (debits/credits should be explicit) |
| Currency mismatch | Flag all foreign currency items for separate handling |

## Anti-Hallucination Rules (CRITICAL)

**These rules must NEVER be bypassed:**

1. **Never infer fraud** — A discrepancy is a discrepancy. It could be a data entry error, timing issue, system limitation, or legitimate difference. Do not conclude otherwise.

2. **Never infer embezzlement** — Missing amounts or unexplained differences require investigation. Do not speculate about cause.

3. **Never infer intentional misconduct** — The skill identifies patterns and flags anomalies. Humans investigate and conclude.

4. **Use neutral language** — Say "unclassified discrepancy" not "suspicious activity". Say "requires investigation" not "potential fraud indicator".

5. **Escalate unexplained items** — Any discrepancy that cannot be classified must be escalated per escalation rules.

6. **Document the investigation process** — Note what was checked, what was not found, and that no conclusion was drawn.

**Correct output:**
> "Unmatched credit entry of 50,000,000 VND on 15/01/2026. Source document not found. Classified as UNCLASSIFIED. Investigation status: PENDING. Escalation required: YES."

**Prohibited output:**
> "This appears to be fraud as the amount was recorded but no supporting document exists."

## Escalation Rules

Escalate to human review when:

| Condition | Escalation Level | Recipient |
|-----------|------------------|----------|
| Unclassified discrepancy > 10,000,000 VND | HIGH | Finance Manager |
| Unclassified discrepancy > 100,000,000 VND | URGENT | CFO |
| > 5% of entries unmatched | HIGH | Finance Manager |
| Pattern of timing differences | MEDIUM | Finance Manager |
| Missing audit trail documentation | MEDIUM | Finance Manager |
| Recurring discrepancies same account | MEDIUM | Finance Manager |
| Suspected duplicate entries | HIGH | Finance Manager |
| Amounts that could affect tax liability | HIGH | Finance Manager + Tax |

**Escalation format:**
```json
{
  "escalation": {
    "escalation_id": "ESC-001",
    "timestamp": "DD/MM/YYYY HH:MM",
    "level": "HIGH|URGENT",
    "recipient": "Finance Manager",
    "reason": "...",
    "affected_items": ["DISC-001", "DISC-002"],
    "total_amount_at_risk": 0,
    "recommended_action": "...",
    "supporting_evidence": ["..."]
  }
}
```

## Legal Disclaimer

**IMPORTANT LEGAL NOTICE:**

This skill performs mechanical reconciliation based on input data. It does not:

- Provide legal, tax, or audit advice
- Guarantee compliance with Vietnamese accounting standards
- Substitute for professional judgment in complex situations
- Detect fraud, misrepresentation, or intentional misstatement
- Replace the need for qualified accounting professionals

**User Responsibility:**

- Verify input data accuracy before reconciliation
- Review all flagged discrepancies with appropriate personnel
- Ensure reconciliations comply with your organization's internal policies
- Consult qualified accountants for complex or unusual transactions
- Obtain appropriate approvals before making adjustments

**Regulatory Compliance:**

This skill references:
- Law 88/2015/QH13 (Accounting Law)
- Circular 99/2025/TT-BTC (Enterprise Accounting Regime, effective 01/01/2026)
- Decree 123/2020/ND-CP (Invoices and Documents)

Users are responsible for ensuring their reconciliation practices comply with the most current version of applicable laws and regulations. Regulations may change after this skill's publication date.

**Limitation of Liability:**

The operators of this system and the skill developers accept no liability for:
- Decisions made based on reconciliation output
- Errors in input data
- Failure to obtain appropriate approvals
- Non-compliance with applicable regulations
- Indirect, incidental, or consequential damages

*Hypothetical example only: Any resemblance to real companies, accounts, or transactions is coincidental.*
