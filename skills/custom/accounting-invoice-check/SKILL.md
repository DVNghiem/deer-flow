---
name: accounting-invoice-check
description: Review invoices for completeness and risk flags per Decree 123/2020/ND-CP
version: 1.0.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - invoice-validation
  - tax-compliance
  - decree-123
  - decree-174
author: DeerFlow Community
created: 2025-07-06
legal_basis:
  - Decree 123/2020/ND-CP
  - Law 48/2024/QH15
  - Decree 174/2025/ND-CP
  - Circular 219/2013/TT-BTC
  - Circular 78/2021/TT-BTC
  - Circular 32/2025/TT-BTC
---

# Accounting Invoice Check Skill

## Purpose

Review Vietnamese commercial invoices for regulatory compliance, completeness, and tax risk flags. This skill validates invoices against Decree 123/2020/ND-CP mandatory field requirements, tax rate regulations per Article 9 of Law 48/2024/QH15, and identifies common defects that may trigger audit findings or tax authority challenges.

## When to Use

- **Deductible expense review**: Before approving expense claims involving invoices ≥ 20M VND requiring bank transfer proof
- **Quarterly/annual tax reconciliation**: During tax filing preparation to flag incomplete or risky invoices
- **Invoice processing automation**: As a checkpoint in accounting workflow systems
- **Vendor onboarding**: To validate invoice quality before vendor approval
- **Audit preparation**: To proactively identify and remediate invoice deficiencies

## When Not to Use

- **Final legal determination**: This skill provides guidance only; consult a licensed tax advisor for definitive legal conclusions
- **Pre-2015 invoices**: Different regulations apply; specialized review required
- **E-invoices**: Different validation rules apply; use accounting-invoice-check-einvoice skill
- **Import/customs declarations**: Not an invoice validation task

---

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `invoice_data` | object | Yes | Core invoice fields |
| `invoice_date` | string | Yes | Invoice issue date (YYYY-MM-DD) |
| `seller_info` | object | Yes | Seller/issuer company details |
| `buyer_info` | object | Yes | Buyer/recipient company details |
| `line_items` | array | Yes | Line item breakdown |
| `tax_breakdown` | object | Yes | Tax rate and amount breakdown |
| `total_amount` | number | Yes | Total invoice amount in VND |

### Input Schema

```typescript
interface InvoiceCheckInput {
  invoice_data: {
    invoice_number?: string;      // Serial + invoice number
    invoice_series?: string;       // Required for companies using series
    payment_method?: string;       // cash|bank_transfer|combined
    adjustment_type?: string;       // For adjusted invoices only
  };
  invoice_date: string;            // ISO date string
  seller_info: {
    tax_code: string;              // 10 or 13 digit tax code
    company_name: string;
    address: string;
    bank_account?: string;
    bank_name?: string;
  };
  buyer_info: {
    tax_code: string;
    company_name: string;
    address: string;
  };
  line_items: Array<{
    description: string;
    quantity: number;
    unit: string;
    unit_price: number;
    total: number;
    tax_rate?: number;             // 0, 5, or 10 (percent)
  }>;
  tax_breakdown: {
    subtotal_ex_vat: number;
    total_vat: number;
    total_inclusive: number;
    vat_rates_applied: number[];
  };
  total_amount: number;
  // Optional supporting evidence
  supporting_docs?: {
    has_bank_transfer_proof?: boolean;
    has_contract?: boolean;
    has_delivery_note?: boolean;
    has_import_declaration?: boolean;
  };
}
```

---

## Step-by-Step Workflow

### Step 1: Invoice Type Verification

**Objective**: Confirm the invoice type matches the transaction nature.

1. Identify if this is a standard sale/service invoice or an adjusted invoice
2. For adjusted invoices, verify:
   - Links to original invoice number and date
   - Adjustment type is one of: correction, replacement, refund
   - Adjusted amounts are consistent with correction type

**Risk flag**: Missing original invoice reference for adjustment invoices.

### Step 2: Mandatory Field Check (Article 10, Decree 123/2020/ND-CP)

**Reference**: [Invoice Requirements Reference](references/invoice-requirements.md)

Verify ALL mandatory fields per Article 10:

| Field | Validation |
|-------|------------|
| Invoice serial + number | Required, proper format |
| Issue date | Required, valid date |
| Seller name | Required, matches tax registration |
| Seller tax code | Required, 10 or 13 digits |
| Seller address | Required |
| Buyer name | Required |
| Buyer tax code | Required |
| Buyer address | Required |
| Line items | At least one item |
| Unit price | Required, > 0 |
| Total amount | Required, matches line sum |
| Tax breakdown | Required if VAT applied |
| Payment method | Required for amounts ≥ 20M VND |

**Risk flag**: Any missing mandatory field is flagged with `severity: high`.

### Step 3: Tax Rate Verification (Article 9, Law 48/2024/QH15)

**Applicable VAT rates per current law**:

| Rate | Applicability |
|------|---------------|
| 0% | Essential goods/services (export, healthcare, education, agriculture) |
| 5% | Essential goods/services (water, medical, education, transportation, etc.) |
| 8% | Standard rate (10% reduced to 8% per Decree 174/2025/ND-CP through 31 Dec 2026) |

**Validation checks**:
1. Verify tax rate is one of: 0%, 5%, or 8% (post Decree 174/2025)
2. Verify rate matches product/service category
3. Verify tax calculation: `tax_amount = taxable_amount × rate`
4. Verify VAT declaration matches invoice amount

**Hypothetical example**:
```
Input: Subtotal = 1,000,000 VND, Rate = 8%, VAT = 80,000 VND
Calculation check: 1,000,000 × 0.08 = 80,000 ✓
```

### Step 4: Timing Verification (Article 9, Decree 123/2020/ND-CP)

**Timing rules**:

| Transaction Type | Deadline |
|-----------------|----------|
| Goods delivery | Issue on delivery or within end of delivery day |
| Service provision | Issue when service completed or payment received |
| Construction/installation | Issue when acceptance occurs |
| Goods sale with immediate payment | Issue at point of sale |
| Goods sale on credit | Issue when payment received |

**Validation**:
1. Check invoice date is not future-dated
2. Check invoice date is not excessive (> 30 days late without justification)
3. For adjustments: check adjusted invoice dated after original

**Risk flag**: Future-dated invoices are `severity: critical`. Late invoices (> 90 days) are `severity: high`.

### Step 5: Supporting Evidence Verification (Article 14, Circular 219/2013/TT-BTC)

**Bank transfer requirement**: For input VAT deduction on invoices ≥ 20,000,000 VND, proof of bank transfer is MANDATORY.

| Amount | Required Documentation |
|--------|----------------------|
| < 20M VND | Invoice + any supporting docs |
| ≥ 20M VND | Invoice + bank transfer proof |
| Combined payment | Cash portion documented, bank portion proven |

**Validation**:
1. If total ≥ 20M VND, verify `has_bank_transfer_proof: true`
2. If partial payment by bank, verify proportional documentation
3. Verify bank account on invoice matches actual transfer record

**Risk flag**: Missing bank proof for ≥ 20M VND invoices is `severity: critical` for input VAT deduction.

### Step 6: Risk Flag Assessment

**Common risk flags**:

| Flag | Severity | Description |
|------|----------|-------------|
| `missing_mandatory_field` | High | Required field absent |
| `tax_rate_mismatch` | High | Applied rate doesn't match product category |
| `calculation_error` | Critical | Math verification failed |
| `missing_bank_proof` | Critical | ≥ 20M VND without transfer proof |
| `future_dated` | Critical | Invoice date is in the future |
| `late_invoice` | Medium | Invoice > 30 days late |
| `tax_code_invalid` | High | Tax code format incorrect |
| `unusual_amount` | Low | Amount significantly outside normal range |
| `round_number` | Low | Suspiciously round total (requires human judgment) |
| `seller_buyer_same` | High | Seller and buyer tax codes identical |

### Step 7: Output Generation

Generate structured output with findings and risk assessment.

---

## Data Validation Rules

| Rule | Description | Action if Failed |
|------|-------------|------------------|
| `invoice_number_format` | Must contain serial prefix + number | Flag `format_warning` |
| `tax_code_length` | 10 or 13 digits | Flag `invalid_tax_code` |
| `amount_positive` | All amounts > 0 | Flag `invalid_amount` |
| `tax_rate_valid` | Must be 0, 5, or 8 | Flag `invalid_tax_rate` |
| `line_sum_matches` | Line total = declared subtotal | Flag `calculation_error` |
| `vat_calculation` | VAT = subtotal × rate | Flag `calculation_error` |
| `total_matches` | Subtotal + VAT = total | Flag `calculation_error` |
| `date_valid` | ISO date format, not future | Flag `date_invalid` or `future_dated` |

---

## Vietnam Legal Verification Checklist

### Decree 123/2020/ND-CP Article 10 - Mandatory Fields

- [ ] Invoice serial number and sequential number
- [ ] Full name, address, tax code of seller
- [ ] Full name, address, tax code of buyer
- [ ] Date of invoice issuance
- [ ] Name, quantity, unit, unit price, total of goods/services
- [ ] Total amount before VAT
- [ ] VAT rate and VAT amount (if applicable)
- [ ] Total amount payable

### Decree 123/2020/ND-CP Article 9 - Timing

- [ ] Invoice issued at time of delivery/service completion
- [ ] No future dating
- [ ] No unreasonable delays (> 90 days)

### Article 14, Circular 219/2013/TT-BTC - Input VAT

- [ ] Bank transfer proof present for invoices ≥ 20,000,000 VND
- [ ] Bank account details on invoice match transfer records

### Decree 174/2025/ND-CP - VAT Rate Reduction

- [ ] Invoice dated 2025-2026 applies 8% standard rate (not 10%)
- [ ] Transitional treatment correct for invoices straddling effective date

---

## Output Format

```json
{
  "review_status": "pass" | "pass_with_warnings" | "fail",
  "summary": {
    "total_checks": 12,
    "passed": 10,
    "warnings": 1,
    "failures": 1
  },
  "mandatory_field_check": {
    "status": "complete" | "incomplete",
    "missing_fields": [],
    "present_fields": ["invoice_number", "invoice_date", "seller_name", "seller_tax_code", "seller_address", "buyer_name", "buyer_tax_code", "buyer_address", "line_items", "unit_price", "total", "vat_breakdown"]
  },
  "tax_calculation_check": {
    "status": "correct" | "incorrect" | "cannot_verify",
    "subtotal": 1000000,
    "declared_vat": 80000,
    "calculated_vat": 80000,
    "total": 1080000,
    "errors": []
  },
  "timing_check": {
    "status": "valid" | "late" | "future_dated" | "cannot_verify",
    "invoice_date": "2025-06-15",
    "issues": []
  },
  "supporting_docs_check": {
    "status": "complete" | "incomplete" | "not_required",
    "required_for_amount": true,
    "has_bank_proof": true,
    "missing_docs": []
  },
  "risk_flags": [
    {
      "flag": "missing_bank_proof",
      "severity": "critical",
      "description": "Invoice amount exceeds 20M VND but no bank transfer proof provided",
      "impact": "Input VAT may not be deductible for this invoice",
      "recommendation": "Request bank transfer record or document alternative payment proof"
    }
  ],
  "recommendations": [
    "Request seller to reissue with complete mandatory fields",
    "Obtain bank transfer proof for input VAT deduction"
  ],
  "legal_disclaimer": "This review is for guidance only. Consult a licensed Vietnamese tax advisor for official tax advice and deductible expense determination."
}
```

---

## Missing Data Handling

| Missing Field | Severity | Handling |
|---------------|----------|----------|
| Invoice number | High | Flag, cannot complete review |
| Invoice date | Critical | Flag, cannot complete review |
| Seller tax code | High | Flag, cannot verify against tax records |
| Line items | High | Flag, cannot verify tax calculation |
| Tax breakdown | Medium | Flag if VAT should be present |
| Buyer info | High | Flag, required for B2B invoices |

**Protocol**:
1. If any `Critical` field missing → output `review_status: fail`, stop further checks
2. If any `High` field missing → output `review_status: fail`, note which checks incomplete
3. If only `Medium` fields missing → output `review_status: pass_with_warnings`
4. If low-priority fields missing → include as informational notes

---

## Error Handling

### Data Validation Errors

| Error | Response |
|-------|----------|
| Invalid date format | Flag `date_invalid`, request clarification |
| Non-numeric amount | Flag `invalid_amount`, reject invoice |
| Negative values | Flag `invalid_amount`, reject invoice |
| Amount exceeds reasonable bounds | Flag `unusual_amount`, escalate for human review |

### Processing Errors

| Error | Response |
|-------|----------|
| Missing required input | Output `review_status: fail`, list missing fields |
| Calculation overflow | Flag `calculation_error`, escalate |
| Unexpected input format | Flag `format_warning`, attempt best-effort parsing |

---

## Anti-Hallucination Rules (CRITICAL)

These rules MUST be followed without exception:

### Rule 1: Never Conclude Validity

**WRONG**: "This invoice is valid and compliant."
**RIGHT**: "This invoice appears complete based on provided data. Official validity requires verification through tax authority systems."

### Rule 2: Never Assume Deductibility

**WRONG**: "The VAT on this invoice is deductible."
**RIGHT**: "The VAT amount is stated. Deductibility depends on business purpose, proper documentation, and tax authority acceptance."

### Rule 3: Never Fabricate Legal Citations

**WRONG**: "Per Article 5, Circular 123..." (if Circular 123 doesn't exist)
**RIGHT**: Use ONLY verified citations from known legal instruments. If uncertain, state "based on general understanding of Decree 123/2020/ND-CP" rather than citing specific articles.

### Rule 4: Always Include Disclaimer

**WRONG**: Ending a review without disclaimer
**RIGHT**: Every output MUST include the legal disclaimer

### Rule 5: Never Override Human Judgment

**WRONG**: "This invoice passes the check, no action needed."
**RIGHT**: "This invoice passes the automated checks. Final determination should be made by authorized accounting personnel."

### Rule 6: Cite Sources Precisely

**WRONG**: "Per recent changes in VAT law..."
**RIGHT**: "Per Decree 174/2025/ND-CP, which reduced the standard VAT rate from 10% to 8% effective [date], the applied rate appears correct for this invoice dated [date]."

---

## Escalation Rules

Escalate to human review when:

| Condition | Reason | Priority |
|-----------|--------|----------|
| Calculation error detected | May indicate fraud or data entry error | High |
| Future-dated invoice | Potential compliance issue | Critical |
| Missing bank proof for ≥ 20M | Tax deduction at risk | Critical |
| Tax code validation fails | Seller may not exist | High |
| Amount > 1B VND | High-value transaction review | High |
| Pattern of late invoices | Systemic process issue | Medium |
| All mandatory fields missing | Cannot perform review | Critical |
| Suspicious patterns detected | Potential fraud | Critical |

---

## Legal Disclaimer

**IMPORTANT**: This skill provides automated review based on document analysis and publicly known Vietnamese tax regulations. This skill does NOT constitute legal advice and should NOT be relied upon as the sole basis for tax decisions.

**Limitations**:
- Automated checks cannot verify authenticity against tax authority databases
- This skill cannot confirm business purpose validity
- Tax deductibility final determination requires authorized tax professional review
- Regulations may change; verify current law before making final decisions

**For official guidance**, consult:
- General Department of Taxation (Tổng cục Thuế)
- Licensed tax advisors registered in Vietnam
- Official tax authority publications

**Reference laws** (as of skill creation date):
- Decree 123/2020/ND-CP dated 19 October 2020
- Law 48/2024/QH15 (Tax Management Law) passed 21 November 2024
- Decree 174/2025/ND-CP dated 1 January 2025
- Circular 219/2013/TT-BTC dated 31 December 2013
- Circular 78/2021/TT-BTC dated 17 August 2021
- Circular 32/2025/TT-BTC dated 20 March 2025

---

*Last updated: 2026-07-06*
*Skill version: 1.0.0*
