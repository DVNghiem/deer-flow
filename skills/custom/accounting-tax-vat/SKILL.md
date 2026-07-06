---
name: accounting-tax-vat
description: VAT compliance checklist and evidence review per Law 48/2024/QH15
version: 1.0.0
domain: vietnam-accounting
---

# Accounting Tax VAT Skill

## Purpose

This skill provides a structured compliance checklist and evidence review framework for Value Added Tax (VAT) under Vietnam's Law 48/2024/QH15. It verifies VAT rates, validates input VAT deduction conditions, and checks VAT refund eligibility.

**Scope:** Evidence review and compliance checklist ONLY. This skill does NOT provide tax advice, tax planning recommendations, or tax calculation services.

## When to Use

- Reviewing VAT invoices for compliance with Law 48/2024/QH15
- Verifying input VAT deduction eligibility for business expenses
- Checking VAT refund application completeness
- Auditing VAT returns before submission
- Validating that VAT rates applied match legal requirements
- Reviewing payment evidence for input VAT claims (transactions ≥20,000,000 VND)

## When NOT to Use

- Calculating VAT amounts or tax liability
- Providing tax planning advice or optimization strategies
- Filing VAT returns or submitting refund applications
- Interpreting ambiguous tax situations requiring professional judgment
- Replacing consultation with a qualified tax advisor

## Required Inputs

The following inputs must be provided to execute this skill:

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `vat_method` | string | Yes | "credit" (input-output method) or "direct" (percentage on revenue) |
| `output_vat` | array | Yes | List of output VAT transactions (sales) |
| `output_vat[].invoice_number` | string | Yes | Invoice identifier |
| `output_vat[].date` | string | Yes | Invoice date (YYYY-MM-DD) |
| `output_vat[].amount_vnd` | number | Yes | Total invoice amount in VND |
| `output_vat[].vat_rate` | number | Yes | VAT rate applied (0, 5, 8, or 10 percent) |
| `output_vat[].service_type` | string | Yes | Description of goods/services |
| `input_vat` | array | Yes | List of input VAT transactions (purchases) |
| `input_vat[].invoice_number` | string | Yes | Invoice identifier |
| `input_vat[].date` | string | Yes | Invoice date (YYYY-MM-DD) |
| `input_vat[].amount_vnd` | number | Yes | Total invoice amount in VND |
| `input_vat[].vat_amount` | number | Yes | VAT amount claimed in VND |
| `input_vat[].vat_rate` | number | Yes | VAT rate on invoice |
| `input_vat[].service_type` | string | Yes | Description of goods/services |
| `invoices` | array | Yes | Supporting VAT invoices for review |
| `payment_evidence` | array | Yes | Bank transfer records for transactions ≥20M VND |

## Step-by-Step Workflow

### Step 1: Identify VAT Method

Determine the applicable VAT method based on business type and characteristics:

| Method | Applicable To | Key Characteristic |
|--------|---------------|-------------------|
| Credit Method | General businesses with proper accounting | Deduct input VAT against output VAT |
| Direct Method | Small businesses, specific industries | Applied as percentage of revenue |

**Action:** Verify method consistency throughout the review period.

### Step 2: Verify Output VAT

For each output VAT transaction, verify:

1. VAT rate matches the service/good type per Article 9, Law 48/2024/QH15
2. Invoice contains all required fields per Decree 209/2013/ND-CP
3. Tax period correctly reported

**Reference:** See VAT Rate Verification Checklist below.

### Step 3: Verify Input VAT Credits

For each input VAT transaction, verify:

1. Invoice is a legitimate VAT invoice with valid serial number
2. Goods/services are for business purposes
3. Payment evidence exists for transactions ≥20,000,000 VND per Article 14, Circular 219/2013/TT-BTC
4. Invoice date falls within the review period

**Reference:** See Input VAT Deduction Conditions Checklist below.

### Step 4: Check Deduction Conditions

Verify all four conditions per Article 14, Law 48/2024/QH15:

1. **Condition 1:** Payment made via bank transfer (for amounts ≥20,000,000 VND)
2. **Condition 2:** Goods/services used for VAT-taxable production/business activities
3. **Condition 3:** Valid VAT invoice or equivalent supporting document
4. **Condition 4:** Goods/services actually received and verified

**Reference:** See Input VAT Deduction Conditions Checklist below.

### Step 5: Check VAT Refund Eligibility

If VAT refund is claimed, verify eligibility per Article 15, Law 48/2024/QH15:

1. Excess input VAT carried forward from previous periods
2. Export transactions with 0% VAT
3. Foreign diplomatic missions and international organizations
4. Compliance with minimum documentation requirements

**Reference:** See VAT Refund Conditions Checklist below.

### Step 6: Flag Issues

Compile all identified discrepancies and compliance gaps:

- Missing payment evidence for high-value transactions
- Incorrect VAT rate applications
- Missing or invalid invoice fields
- Incomplete supporting documentation
- Timing mismatches between invoice and payment

---

## VAT Rate Verification Checklist

Per **Article 9, Law 48/2024/QH15** (effective 01/07/2025):

### 0% VAT Rate

Applies to exports and international transport:

- [ ] Goods exported outside Vietnam
- [ ] Services consumed outside Vietnam
- [ ] International transportation services
- [ ] Goods and services for diplomatic missions
- [ ] Goods and services for aid and humanitarian purposes

**Legal Reference:** Article 9(1), Law 48/2024/QH15

### 5% VAT Rate

Applies to essential goods and services:

- [ ] Clean water for production and daily use
- [ ] Fertilizers, pesticides, agricultural tools
- [ ] Teaching equipment, scientific equipment
- [ ] Medical equipment and assistive devices
- [ ] News, press, and official publications
- [ ] Art performances and cultural events (domestic)
- [ ] Children's toys and books
- [ ] Food products in their natural state or basic processing
- [ ] Protective equipment for production safety

**Legal Reference:** Article 9(2), Law 48/2024/QH15

### 8% VAT Rate

**Temporary reduction** per Decree 174/2025/ND-CP (until 31/12/2026):

- [ ] Goods and services currently subject to 10% rate
- [ ] Applicable to domestic transactions during reduction period

**Legal Reference:** Article 1, Decree 174/2025/ND-CP

**Note:** This is a temporary reduction. Rate reverts to 10% from 01/01/2027 unless extended.

### 10% VAT Rate

**Default rate** applies when no other rate applies:

- [ ] All other goods and services not covered by 0%, 5%, or 8% rates

**Legal Reference:** Article 9(4), Law 48/2024/QH15

---

## Input VAT Deduction Conditions Checklist

Per **Article 14, Law 48/2024/QH15** (effective 01/07/2025):

### Condition 1: Payment Method (Article 14(1))

For transactions **≥20,000,000 VND**:

- [ ] Payment made via bank transfer
- [ ] Bank transfer record matches invoice details
- [ ] Transfer date is on or after invoice date
- [ ] Transfer amount covers full invoice or documented installment

**Legal Reference:** Article 14(1), Law 48/2024/QH15; Article 14, Circular 219/2013/TT-BTC

**Exception:** Cash payment permitted when:
- Paying taxes and state fees to state treasury
- Paying for goods/services in remote areas without banking services
- Other exceptions per current regulations

### Condition 2: Business Purpose (Article 14(2))

- [ ] Goods/services used for VAT-taxable production activities
- [ ] Goods/services used for VAT-taxable business operations
- [ ] Clear nexus between purchased goods/services and taxable output
- [ ] No personal or non-business use included

**Legal Reference:** Article 14(2), Law 48/2024/QH15

### Condition 3: Valid Documentation (Article 14(3))

- [ ] VAT invoice with proper serial number and format
- [ ] All required invoice fields completed (seller, buyer, description, amount, VAT)
- [ ] Invoice not from cancelled or suspended taxpayer
- [ ] Invoice not from businesses without proper tax registration
- [ ] Electronic invoice submitted to tax authority (if applicable)

**Legal Reference:** Article 14(3), Law 48/2024/QH15

### Condition 4: Goods/Services Received (Article 14(4))

- [ ] Goods physically received or documented completion for services
- [ ] No fictitious or incomplete transactions
- [ ] Actual delivery supported by receiving documentation
- [ ] Warehouse receipts, service completion reports, or equivalent

**Legal Reference:** Article 14(4), Law 48/2024/QH15

---

## VAT Refund Conditions Checklist

Per **Article 15, Law 48/2024/QH15** (effective 01/07/2025):

### Eligible for Refund (Article 15(1))

- [ ] Input VAT exceeds output VAT in the tax period
- [ ] Excess carried forward from previous period
- [ ] Export of goods/services with 0% VAT
- [ ] Goods/services supplied to diplomatic missions and international organizations
- [ ] Newly established investment projects (under specific conditions)
- [ ] Organizations with VAT-exempt activities generating excess input VAT

### Documentation Requirements (Article 15(2))

- [ ] Completed VAT refund application form
- [ ] VAT return for the claimed period
- [ ] List of VAT invoices (input)
- [ ] List of VAT invoices (output)
- [ ] Bank transfer records for transactions ≥20M VND
- [ ] Export documentation (for export-related refunds)
- [ ] Contract or agreement for long-term projects
- [ ] Minutes of goods receipt or service completion

### Ineligible Situations

- [ ] Tax evasion or fraud suspected
- [ ] Missing documentation as outlined above
- [ ] Non-compliance with other tax regulations
- [ ] Tax debt outstanding
- [ ] Recently established businesses under scrutiny period

---

## Output Format

The skill returns results in JSON format:

```json
{
  "skill": "accounting-tax-vat",
  "version": "1.0.0",
  "review_date": "YYYY-MM-DD",
  "vat_method": "credit",
  "summary": {
    "total_output_vat_transactions": 0,
    "total_output_vat_amount": 0,
    "total_input_vat_transactions": 0,
    "total_input_vat_claimed": 0,
    "total_input_vat_verified": 0,
    "issues_count": 0,
    "compliance_status": "PASS|FAIL|WARNING"
  },
  "output_vat_review": [
    {
      "invoice_number": "string",
      "vat_rate_applied": 0,
      "vat_rate_correct": true|false,
      "correct_rate": 0,
      "legal_reference": "string",
      "issue": "string|null"
    }
  ],
  "input_vat_review": [
    {
      "invoice_number": "string",
      "vat_amount_claimed": 0,
      "deductibility": "VERIFIED|CONDITIONAL|FLAGGED",
      "conditions_met": {
        "payment_method": true|false,
        "business_purpose": true|false,
        "valid_documentation": true|false,
        "goods_services_received": true|false
      },
      "missing_evidence": ["string"],
      "legal_reference": "string",
      "issue": "string|null"
    }
  ],
  "vat_refund_eligibility": {
    "eligible": true|false,
    "conditions_met": true|false,
    "documentation_complete": true|false,
    "missing_documents": ["string"],
    "legal_reference": "string"
  },
  "flagged_issues": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "category": "string",
      "description": "string",
      "invoice_numbers": ["string"],
      "legal_reference": "string",
      "recommendation": "string"
    }
  ],
  "references_used": [
    "Law 48/2024/QH15",
    "Decree 209/2013/ND-CP",
    "Decree 174/2025/ND-CP",
    "Circular 219/2013/TT-BTC"
  ],
  "disclaimer": "This skill provides compliance checklist review only. It does not constitute tax advice."
}
```

---

## Anti-Hallucination Rules

**CRITICAL: Follow these rules strictly to prevent incorrect conclusions.**

### Rule 1: Never State a Rate Without Legal Citation

**WRONG:** "The VAT rate for this service is 10%."
**CORRECT:** "Based on Article 9(4), Law 48/2024/QH15, the default 10% rate applies to this service category."

### Rule 2: Never Conclude Deductibility Without Verifying All Conditions

**WRONG:** "Input VAT of X VND is deductible."
**CORRECT:** "Input VAT of X VND is VERIFIED when all four conditions per Article 14, Law 48/2024/QH15 are met: (1) payment via bank transfer, (2) business purpose, (3) valid documentation, (4) goods/services received."

### Rule 3: Label All Examples as Hypothetical

**WRONG:** "A construction company purchasing 50M VND of materials can deduct VAT."
**CORRECT:** "Hypothetical example only: A construction company purchasing 50,000,000 VND of materials with proper bank transfer evidence may claim input VAT deduction if all Article 14 conditions are met."

### Rule 4: Distinguish Between Rate Application and Deduction Eligibility

**WRONG:** "The 10% VAT rate means input VAT is deductible."
**CORRECT:** "Rate verification (Article 9) and deduction eligibility (Article 14) are separate determinations. A correctly applied VAT rate does not guarantee deductibility."

### Rule 5: Flag Ambiguous Situations

When encountering unclear cases:
- State the ambiguity explicitly
- List possible interpretations with legal references
- Recommend escalation to qualified tax professional
- Do NOT guess or assume a resolution

---

## Escalation Rules

**Escalate to qualified tax professional when:**

1. Transaction involves mixed VAT rates that require allocation
2. Business activities span multiple VAT treatment categories
3. Legal interpretation is ambiguous or contested
4. Cross-border transactions with international tax implications
5. Transactions with related parties requiring transfer pricing analysis
6. Refund amount exceeds defined thresholds requiring tax authority review
7. Suspected non-compliance requires voluntary disclosure consideration
8. Industry-specific VAT treatments are unclear
9. Temporal applicability of different legal provisions is unclear
10. Tax authority has issued case-specific guidance

**Escalation Template:**

```
ESCALATION REQUIRED
Category: [Category]
Issue: [Description of ambiguous or complex situation]
Legal References Considered: [List applicable laws/decrees/circulars]
Ambiguity: [Specific question or unclear element]
Recommendation: [Escalate to tax advisor/tax authority consultation]
```

---

## Legal Disclaimer

**This skill provides compliance checklist review only.**

It is designed to assist with reviewing VAT compliance and verifying evidence against legal requirements. However, this skill:

- **Does NOT** constitute professional tax advice
- **Does NOT** replace consultation with a qualified tax advisor
- **Does NOT** guarantee tax authority acceptance of claimed deductions
- **Does NOT** cover all possible VAT scenarios or industry-specific rules
- **Does NOT** represent opinions or interpretations of tax authorities

Tax laws are subject to change and may have industry-specific provisions not covered by this skill. For any tax decisions, compliance determinations, or situations with legal ambiguity, consult a qualified Vietnamese tax professional or obtain direct guidance from the General Department of Taxation.

**Legal References:**

- Law 48/2024/QH15 (VAT Law, effective 01/07/2025)
- Decree 209/2013/ND-CP (VAT Implementation)
- Decree 174/2025/ND-CP (VAT Reduction)
- Circular 219/2013/TT-BTC (VAT Deduction Conditions)
- Circular 93/2017/TT-BTC (Electronic VAT Invoices)
