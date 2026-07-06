# Common Invoice Defects Reference

**Purpose**: Identify, classify, and remediate common invoice defects found during accounting review
**Legal Basis**: Decree 123/2020/ND-CP, Circular 219/2013/TT-BTC
**Last Updated**: 2025-07-06
**Disclaimer**: This document is for reference only. Consult official gazettes and tax advisors for definitive guidance.

---

## Defect Classification Framework

Defects are classified by severity and impact on:
- Input VAT deduction eligibility
- Tax authority audit risk
- Financial statement accuracy

### Severity Levels

| Severity | Impact | Action Required |
|----------|--------|-----------------|
| **Critical** | Input VAT likely non-deductible; high penalty risk | Immediate correction or escalation |
| **High** | Invoice may be rejected; audit flag | Request reissue or provide documentation |
| **Medium** | Minor compliance issue | Document and monitor |
| **Low** | Informational; no immediate action | Include in review notes |

---

## Section 1: Critical Defects

### 1.1 Missing Bank Transfer Proof (≥ 20M VND)

**Legal Basis**: Article 14, Circular 219/2013/TT-BTC

**Description**:
Invoices totaling ≥ 20,000,000 VND without documented bank transfer proof.

**Detection Criteria**:
- `total_amount >= 20000000`
- `payment_method == 'cash'`
- `has_bank_transfer_proof == false`

**Impact**:
- Input VAT non-deductible (per Article 14 Circular 219/2013/TT-BTC)
- May trigger tax authority inquiry
- Expense may be disallowed

**Corrective Actions**:

| Scenario | Action |
|----------|--------|
| Cash payment actually made | Request reissue with bank transfer OR obtain alternative documentation |
| Bank transfer made but not documented | Request bank statement extract |
| Payment < 20M when combining invoices | Ensure invoices separated; each < 20M individually |
| Payment split between cash and bank | Document bank portion separately; cash portion ≤ 20M |

**Hypothetical example**:
```
Invoice: 45,000,000 VND
Payment: Cash
Missing bank proof → Critical defect

Remediation options:
1. Obtain bank transfer record (if originally paid by transfer)
2. Request credit note and reissue with proper payment method
3. Document business reason for cash payment (rare exceptions exist)
```

### 1.2 Future-Dated Invoice

**Legal Basis**: Article 9, Decree 123/2020/ND-CP

**Description**:
Invoice with issue date in the future relative to current date.

**Detection Criteria**:
- `invoice_date > current_date`

**Impact**:
- Non-compliant with Decree 123/2020/ND-CP timing requirements
- May indicate fictitious transaction
- Cannot be used for VAT input deduction until date arrives
- High audit risk

**Corrective Actions**:
- Do not process; return to issuer for correction
- If received with future date, wait until date passes, then re-verify
- Document as "Received early; cannot process until [date]"

### 1.3 Calculation Error in Tax Amount

**Legal Basis**: Article 10, Decree 123/2020/ND-CP

**Description**:
VAT amount does not equal taxable amount × applicable rate.

**Detection Criteria**:
- `calculated_vat != declared_vat`
- Where: `calculated_vat = subtotal × vat_rate`

**Hypothetical example**:
```
Subtotal: 10,000,000 VND
VAT Rate: 8%
Declared VAT: 850,000 VND  ← ERROR
Correct VAT: 800,000 VND

Severity: Critical
Impact: Invoice may be rejected; requests reissue
```

**Corrective Actions**:
- Request corrected invoice with accurate VAT calculation
- If received as-is, escalate for manual review
- Document discrepancy for audit trail

### 1.4 Missing All Mandatory Fields

**Description**:
Invoice lacks sufficient information to identify parties or verify transaction.

**Detection Criteria**:
- Missing seller tax code AND seller name
- Missing buyer information entirely
- Missing date AND invoice number

**Impact**:
- Cannot identify parties to transaction
- Cannot verify against tax records
- Invoice invalid for any tax purpose

**Corrective Actions**:
- Reject invoice; request complete replacement
- Escalate if pattern from vendor identified

---

## Section 2: High Severity Defects

### 2.1 Missing Mandatory Field(s)

**Legal Basis**: Article 10, Decree 123/2020/ND-CP

**Description**:
Invoice missing one or more mandatory fields per Article 10.

**Common Missing Fields**:

| Field | Frequency | Severity |
|-------|-----------|----------|
| Seller tax code | Common | High |
| Buyer tax code | Common | High |
| Invoice date | Less common | High |
| Unit price | Less common | High |
| VAT breakdown | Moderate | Medium |
| Payment method | Common for < 20M | Low-Medium |

**Impact**:
- Depending on field: partial or full non-compliance
- Tax authority may reject during audit
- Input VAT deduction may be challenged

**Corrective Actions**:
- Request seller reissue with complete fields
- If seller unwilling, document reason and escalate
- For internal invoices: implement pre-issuance validation

### 2.2 Invalid Tax Code

**Legal Basis**: Tax Code Registration System (TNCN/TNDN)

**Description**:
Tax code format does not match Vietnamese standards.

**Valid Formats**:

| Entity Type | Format | Example |
|-------------|--------|---------|
| Enterprise | 10 digits | 0123456789 |
| Individual | 13 characters (K + 12 digits) | K123456789012 |
| Foreign | Varies by treaty | Treaty-specific |

**Detection Criteria**:
- Not 10 digits (for organizations)
- Not 13 characters starting with K (for individuals)
- Contains non-numeric characters (except K prefix)
- Checksum validation fails

**Impact**:
- Cannot verify seller/buyer exists
- Cannot cross-reference with tax authority records
- May indicate fictitious entity

**Corrective Actions**:
- Request clarification from issuer
- Verify against business registration documents
- If verification fails, escalate for due diligence

### 2.3 Tax Rate Mismatch

**Legal Basis**: Article 9, Law 48/2024/QH15; Decree 174/2025/ND-CP

**Description**:
Applied VAT rate does not match the product/service category requirements.

**Common Mismatches**:

| Product Category | Correct Rate | Incorrect Rate Applied |
|-----------------|--------------|----------------------|
| Standard goods | 8% | 5% (too low) or 10% (too high) |
| Essential goods | 5% | 8% (too high) |
| Exports | 0% | 8% (too high) |

**Detection Criteria**:
- Product description indicates category with specific rate
- Applied rate differs from standard rate for stated category
- Post-2025: 10% applied (should be 8%)

**Impact**:
- Incorrect tax charged/claimed
- May trigger audit
- Requires correction and potential refund claim

**Corrective Actions**:
- Identify correct rate based on product category
- Request corrected invoice
- If over-collected: issue refund
- If under-collected: pay difference + potential penalties

### 2.4 Late Invoice Issuance

**Legal Basis**: Article 9, Decree 123/2020/ND-CP

**Description**:
Invoice issued significantly after goods delivery or service completion.

**Risk Classification**:

| Delay | Severity | Risk Level |
|-------|----------|------------|
| 1-7 days | Low | Minimal |
| 8-30 days | Medium | Moderate |
| 31-90 days | High | Significant |
| > 90 days | Critical | Very High |

**Impact**:
- May indicate transaction didn't occur when claimed
- Non-compliance with timing requirements
- Tax authority scrutiny

**Corrective Actions**:
- Request written explanation from issuer
- Document business reason for delay
- For > 90 days: escalate for management review
- Consider rejecting and requiring new invoice

### 2.5 Seller and Buyer Same Entity

**Legal Basis**: General tax principles; Circular 219/2013/TT-BTC

**Description**:
Invoice issued where seller tax code equals buyer tax code.

**Detection Criteria**:
- `seller_info.tax_code == buyer_info.tax_code`

**Impact**:
- Intra-company transaction should not generate deductible expense
- May indicate documentation error
- Could indicate fraud if treated as external transaction

**Corrective Actions**:
- Verify if transaction is truly inter-company
- If inter-company: treat as internal transfer, not expense
- If error: request corrected invoice
- Escalate for investigation if unexplained

### 2.6 Invoice Amount Mismatch

**Legal Basis**: Article 10, Decree 123/2020/ND-CP

**Description**:
Declared totals do not equal sum of line items.

**Variations**:
- Line sum ≠ declared subtotal
- Subtotal + VAT ≠ declared total
- Rounding inconsistency

**Detection Criteria**:
- `SUM(line_items.total) != tax_breakdown.subtotal_ex_vat`
- `subtotal + total_vat != total_amount`

**Impact**:
- Indicates calculation error
- Invoice may be rejected
- Requires correction

**Hypothetical example**:
```
Line Items Total: 9,950,000 VND
Declared Subtotal: 10,000,000 VND
Difference: 50,000 VND

Severity: High
Action: Request corrected invoice
```

---

## Section 3: Medium Severity Defects

### 3.1 Missing Payment Method

**Legal Basis**: Article 10, Decree 123/2020/ND-CP; Article 14, Circular 219/2013/TT-BTC

**Description**:
Invoice does not specify payment method, particularly important for amounts ≥ 20M VND.

**Impact**:
- Cannot verify bank transfer requirement compliance
- Minor for small amounts; significant for large

**Corrective Actions**:
- Request clarification
- If ≥ 20M: require confirmation of payment method with proof

### 3.2 Inconsistent Bank Account

**Legal Basis**: Article 14, Circular 219/2013/TT-BTC

**Description**:
Bank account on invoice differs from actual transfer record.

**Impact**:
- May indicate payment to different entity
- Triggers suspicion of legitimacy
- Input VAT deduction challengeable

**Corrective Actions**:
- Verify actual transfer account
- Document if subsidiaries/related parties involved
- Escalate if unexplained

### 3.3 Invoice Series Discontinuity

**Legal Basis**: Decree 123/2020/ND-CP

**Description**:
Gaps in invoice numbering or series irregularities.

**Impact**:
- May indicate missing invoices
- Triggers audit inquiry
- Need to document "voided" invoices

**Corrective Actions**:
- Request voided invoice register
- Document all gaps with explanations
- If unexplained gaps: escalate

### 3.4 Adjustment Invoice Missing Original Reference

**Legal Basis**: Article 11, Decree 123/2020/ND-CP

**Description**:
E-type (adjustment) invoice without reference to original C invoice.

**Impact**:
- Cannot verify adjustment is valid
- May indicate unauthorized adjustment
- Breaks audit trail

**Corrective Actions**:
- Request original invoice reference
- Verify adjustment against original
- If refused: escalate

---

## Section 4: Low Severity Defects

### 4.1 Minor Formatting Issues

**Description**:
Non-critical formatting inconsistencies that don't affect compliance.

**Examples**:
- Phone number format variations
- Address abbreviated differently
- Company name spacing inconsistencies

**Impact**:
- Minimal
- May indicate data entry carelessness

**Corrective Actions**:
- Document if future reference needed
- No immediate action required
- Monitor for pattern

### 4.2 Rounding Discrepancies

**Legal Basis**: Standard accounting practice

**Description**:
Minor rounding differences due to calculation method.

**Hypothetical example**:
```
Price per unit: 33,333.33 VND
Quantity: 3
Line total: 99,999.99 VND

May be rounded to 100,000 VND
Difference: 0.01 VND
```

**Impact**:
- Minimal
- Standard in commercial practice

**Corrective Actions**:
- If < 100 VND total difference: note and proceed
- If > 100 VND: request clarification

### 4.3 Missing Optional Fields

**Description**:
Optional fields (email, phone, contact name) not populated.

**Impact**:
- None for compliance
- May complicate follow-up communications

**Corrective Actions**:
- None required
- Note for future communication purposes

---

## Section 5: Risk Pattern Detection

### 5.1 Volume Risk Patterns

| Pattern | Description | Risk |
|---------|-------------|------|
| Same-day batch | Multiple invoices from same vendor, same date | Low-Medium |
| Round amounts | All invoices are exact round numbers | Medium |
| Weekend/holiday | Invoices dated on holidays | Medium |
| Series clustering | Sequential invoices all flagged | Low |
| Amount clustering | All invoices just under thresholds | Medium-High |

### 5.2 Vendor Risk Patterns

| Pattern | Description | Risk |
|---------|-------------|------|
| New vendor | Vendor recently registered | Medium-High |
| Single transaction | Only one invoice from vendor | Low |
| Related party | Vendor is subsidiary/associate | Medium |
| Tax code anomalies | Multiple tax codes for same name | High |

### 5.3 Timing Risk Patterns

| Pattern | Description | Risk |
|---------|-------------|------|
| Quarter-end spike | Unusual volume at quarter end | Medium |
| Year-end rush | High volume in December | Low |
| Post-deadline | Invoices just before filing deadline | Medium |

---

## Section 6: Remediation Workflow

### Workflow for Critical/High Defects

```
1. IDENTIFY
   └─> Flag defect with severity level
   
2. ASSESS
   ├─> Determine if reissuance possible
   ├─> Evaluate impact on tax position
   └─> Estimate remediation effort
   
3. CONTACT
   ├─> Notify issuer of defect
   ├─> Provide specific correction required
   └─> Set deadline for response
   
4. RESOLVE
   ├─> Receive corrected invoice
   ├─> Verify correction
   └─> Update records
   
5. DOCUMENT
   ├─> Record original defect
   ├─> Record correction
   └─> File for audit trail
   
6. ESCALATE (if unresolved)
   └─> Notify management
   └─> Consider vendor removal
```

### Escalation Triggers

| Trigger | Escalate To |
|---------|-------------|
| Reissuance refused | Finance Manager |
| > 30 days unresolved | Finance Director |
| Pattern of defects from vendor | Procurement + Finance Director |
| Suspected fraud | Finance Director + Legal |
| Amount > 100M VND with defect | Finance Director + CFO |

---

## Section 7: Defect Statistics Reference

### Common Defect Frequency (Hypothetical Data)

Based on accounting review experience:

| Defect Type | Frequency | % of Total |
|-------------|-----------|------------|
| Missing bank proof | 15% | Most common critical |
| Missing mandatory fields | 12% | Common |
| Calculation errors | 5% | Less common |
| Invalid tax code | 3% | Less common |
| Timing issues | 8% | Common |
| Other | 57% | Various |

---

## Summary Checklist

### Before Flagging Defect

- [ ] Verify input data is accurate
- [ ] Check for data entry errors on your end
- [ ] Confirm interpretation of requirement
- [ ] Check for known exceptions

### When Flagging Defect

- [ ] Assign correct severity level
- [ ] Provide specific recommendation
- [ ] Reference applicable regulation
- [ ] Include impact statement
- [ ] Set action required

### When Escalating

- [ ] Document all attempted resolutions
- [ ] Provide complete documentation
- [ ] State business impact
- [ ] Recommend decision criteria

---

## Disclaimer

**This reference document is provided for informational purposes only.**

The defect classifications and severity levels in this document represent general guidance based on publicly available regulations. Actual regulatory interpretation may vary. Always consult official gazettes and qualified tax professionals for definitive guidance on specific situations.

This document does not constitute legal or tax advice. The author and contributors are not responsible for any decisions made based on this information.

**For official guidance**:
- General Department of Taxation: https://gdt.gov.vn
- Ministry of Finance: https://mof.gov.vn
- Licensed tax advisors registered in Vietnam

---

*Last updated: 2025-07-06*
