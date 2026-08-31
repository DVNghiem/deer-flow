# Vietnam Invoice Requirements Reference

**Legal Basis**: Decree 123/2020/ND-CP, Law 48/2024/QH15, Decree 174/2025/ND-CP
**Last Updated**: 2025-07-06
**Disclaimer**: This document is for reference only. Always verify against official gazettes.

---

## Decree 123/2020/ND-CP Overview

Decree 123/2020/ND-CP governs the issuance and management of electronic invoices in Vietnam, replacing earlier regulations on sales invoices, value-added invoices, and service invoice guidelines.

### Scope

Applies to:
- Organizations and individuals producing and trading goods/services in Vietnam
- Foreign entities with permanent establishments in Vietnam
- Goods and services consumed in Vietnam

---

## Article 10 - Mandatory Invoice Fields

Per Article 10 of Decree 123/2020/ND-CP, every invoice must contain the following mandatory fields:

### Invoice Header

| Field | Requirement | Notes |
|-------|------------|-------|
| Invoice serial number | Mandatory | Assigned by tax authority or self-generated |
| Invoice number | Mandatory | Sequential, continuous numbering |
| Invoice type code | Mandatory | C (sale), E (adjustment), H (replacement) |
| Issue date | Mandatory | Date invoice is issued |
| Issue time | Recommended | For e-invoices |

### Seller Information

| Field | Requirement | Notes |
|-------|------------|-------|
| Seller name | Mandatory | Legal name as registered |
| Seller tax code | Mandatory | 10 digits (organizations) or 13 digits (individuals) |
| Seller address | Mandatory | Full registered address |
| Seller phone | Optional | Contact number |
| Seller email | Optional | For e-invoice delivery |

### Buyer Information

| Field | Requirement | Notes |
|-------|------------|-------|
| Buyer name | Mandatory | Legal name as registered |
| Buyer tax code | Mandatory | 10 digits (organizations) or 13 digits (individuals) |
| Buyer address | Mandatory | Full registered address |
| Buyer email | Optional | For e-invoice delivery |

### Line Items

| Field | Requirement | Notes |
|-------|------------|-------|
| Product/service name | Mandatory | Clear description |
| Quantity | Mandatory | Numeric value with unit |
| Unit | Mandatory | e.g., piece, kg, hour, service |
| Unit price | Mandatory | Excluding VAT |
| Total per line | Mandatory | Quantity × unit price |
| Tax rate | Mandatory if VAT | 0%, 5%, or 8% (current) |
| VAT amount | Mandatory if VAT | Tax rate × taxable amount |

### Totals Section

| Field | Requirement | Notes |
|-------|------------|-------|
| Subtotal (before VAT) | Mandatory | Sum of all line totals |
| VAT rate(s) applied | Mandatory | Per current regulations |
| Total VAT amount | Mandatory | Sum of all VAT |
| Total amount payable | Mandatory | Subtotal + Total VAT |

### Payment Information (for amounts ≥ 20M VND)

| Field | Requirement | Notes |
|-------|------------|-------|
| Payment method | Mandatory | cash/bank_transfer/combined |
| Bank account (if bank) | Mandatory | Seller's receiving account |
| Bank name | Mandatory | If bank transfer |

### Additional Fields for Adjustments

| Field | Requirement | Notes |
|-------|------------|-------|
| Original invoice number | Mandatory | For E (adjustment) type |
| Original invoice date | Mandatory | For E (adjustment) type |
| Adjustment reason | Mandatory | Per Article 11 Decree 123 |
| Adjustment type | Mandatory | Correction, replacement, or refund |

---

## Invoice Types (Article 11, Decree 123/2020/ND-CP)

### C - Regular Sale Invoice

Issued for:
- Sale of goods
- Provision of services
- Construction and installation

Characteristics:
- Standard format
- Continuous numbering
- First invoice of series starts from 0000001

### E - Invoice Adjustment

Issued to correct errors on original C invoice:

| Adjustment Type | When Used |
|---------------|-----------|
| Correction | Minor errors in quantity, price, or description |
| Replacement | Full replacement of original invoice |
| Refund | Credit for returned goods or cancelled services |

**Requirements**:
- Must reference original invoice serial and number
- Adjustment amount = new amount - original amount
- Negative adjustments permitted

### H - Invoice for Replacement

Issued when replacing a C invoice that must be cancelled:
- References the C invoice being replaced
- New invoice number issued
- C invoice marked as replaced

---

## Article 9 - Timing Requirements (Decree 123/2020/ND-CP)

### General Principles

Invoices must be issued at the time goods are delivered or services are completed. The timing depends on the nature of the transaction.

### Transaction-Type Specific Rules

| Transaction Type | Invoice Timing | Legal Reference |
|-----------------|-----------------|-----------------|
| Immediate goods delivery | At point of sale | Article 9(1) |
| Goods delivery (deferred) | On delivery day | Article 9(1) |
| Service provision | When service completed OR payment received | Article 9(2) |
| Construction/installation | On acceptance by buyer | Article 9(3) |
| Periodic services | Monthly/quarterly summary | Article 9(2) |
| Goods on approval | On approval date | Article 9(1) |
| Imports | Customs declaration date | Article 9(4) |

### Timing Tolerances

| Situation | Tolerance | Documentation Required |
|-----------|-----------|----------------------|
| Same-day issue | 0 days | None |
| Delayed issue | Up to 7 days | Internal approval |
| Delayed issue | 8-30 days | Written explanation |
| Delayed issue | > 30 days | Detailed justification + management approval |
| Delayed issue | > 90 days | **Not recommended** - high audit risk |

### Future Dating Prohibition

**CRITICAL**: Invoices MUST NOT be issued with future dates.

Future-dated invoices are:
- Non-compliant with Decree 123
- May indicate GST fraud
- Subject to penalties if detected

---

## VAT Rate Regulations

### Current VAT Rates (as of Decree 174/2025/ND-CP)

Effective 1 January 2025, the standard VAT rate was reduced from 10% to 8%.

| Rate | Category | Examples | Legal Basis |
|------|----------|----------|-------------|
| 0% | Zero-rated | Exports, international transport, aviation | Article 9 Law 48/2024 |
| 5% | Reduced rate | Essential goods/services | Article 9 Law 48/2024 |
| 8% | Standard rate | General goods and services | Decree 174/2025 |

### 0% VAT Applicability

Zero-rated VAT applies to:
- Goods and services exported
- International transportation services
- Aviation and aviation support services
- Sea and inland waterway transportation
- Goods and services for diplomatic/consular missions
- Goods and services for international organizations

### 5% VAT Applicability

Reduced 5% rate applies to:
- Clean water for production and household use
- Teaching aids, textbooks
- Medical equipment and assistive devices
- Various agricultural products
- Scientific technology services
- Construction works with approved social housing

### 8% Standard Rate

The standard 8% rate applies to all other goods and services not specified for 0% or 5% rates.

### Transitional Rules (Decree 174/2025/ND-CP)

| Invoice Date | Applied Rate |
|-------------|--------------|
| Before 1 Jan 2025 | 10% (if issued by 31 Jan 2025 with goods/services delivered by 31 Dec 2024) |
| From 1 Jan 2025 | 8% |
| After 31 Dec 2026 | Reverts to 10% (unless extended) |

---

## Input VAT Deduction Requirements

### Article 14, Circular 219/2013/TT-BTC

For input VAT to be deductible, the following conditions must be met:

1. Invoice must be valid (proper form, all mandatory fields)
2. Goods/services used for taxable business activities
3. Payment documented (bank transfer for ≥ 20,000,000 VND)

### Bank Transfer Requirement (Critical)

**Per Article 14(1), Circular 219/2013/TT-BTC** (as amended):

For invoices with total value ≥ 20,000,000 VND, proof of bank transfer is **MANDATORY** for input VAT deduction.

| Amount | Payment Method | Input VAT Deductible |
|--------|---------------|---------------------|
| < 20M VND | Any documented method | Yes |
| ≥ 20M VND | Cash only | **NO** |
| ≥ 20M VND | Bank transfer documented | Yes |
| ≥ 20M VND | Combined (cash < 20M, bank ≥ remainder) | Yes, for documented portion |

### Supporting Documentation

For input VAT deduction on invoices ≥ 20M VND, maintain:
1. Original invoice
2. Bank transfer record showing:
   - Transfer date
   - Amount transferred
   - Seller bank account (must match invoice)
   - Buyer bank account

---

## Common Validation Patterns

### Tax Code Format Validation

| Type | Format | Example |
|------|--------|---------|
| Organization | 10 digits | 0123456789 |
| Individual | 13 digits (K + 12 digits) | K012345678912 |
| Foreign | 12 digits + country code | 123456789012@VN |

### Date Format

ISO 8601 format: `YYYY-MM-DD`
- Vietnamese standard: `DD/MM/YYYY` (for display)
- Always convert to ISO for processing

### Amount Precision

- All amounts in VND (no decimals for invoices)
- Round to nearest whole number
- Tax calculations: round down if < 0.5, round up if ≥ 0.5

---

## Reference Laws and Regulations

### Primary Regulations

1. **Decree 123/2020/ND-CP** (19 Oct 2020)
   - Invoice form and content requirements
   - Issuance timing
   - Adjustment procedures

2. **Law 48/2024/QH15** (21 Nov 2024)
   - Tax administration law
   - VAT rate specifications (Article 9)

3. **Decree 174/2025/ND-CP** (1 Jan 2025)
   - VAT rate reduction from 10% to 8%
   - Effective through 31 Dec 2026

### Supporting Regulations

4. **Circular 219/2013/TT-BTC** (31 Dec 2013)
   - Input VAT deduction conditions
   - Bank transfer requirements

5. **Circular 78/2021/TT-BTC** (17 Aug 2021)
   - Tax administration procedures
   - E-invoice implementation

6. **Circular 32/2025/TT-BTC** (20 Mar 2025)
   - Implementation guidance for Decree 174/2025
   - Transitional provisions

---

## Hypothetical Examples

### Example 1: Valid Invoice (Hypothetical only)

```
Invoice Number: CTHD-2025-0012345
Date: 2025-06-15

Seller:
  Name: ABC Manufacturing Co., Ltd
  Tax Code: 0123456789
  Address: 123 Industrial Zone, District 7, Ho Chi Minh City

Buyer:
  Name: XYZ Trading JSC
  Tax Code: 9876543210
  Address: 456 Commerce Building, District 1, Ho Chi Minh City

Items:
  | Product | Qty | Unit | Unit Price | Total |
  |---------|-----|------|------------|-------|
  | Widget A | 100 | piece | 10,000 | 1,000,000 |

VAT: 8% = 80,000
Total: 1,080,000 VND

Payment: Bank Transfer
Bank: Vietcombank - Account: 1234567890
```

**Analysis**: All mandatory fields present, VAT calculation correct (1,000,000 × 8% = 80,000), timing valid.

### Example 2: Invoice with Risk Flags (Hypothetical only)

```
Invoice Number: CTHD-2025-0099999
Date: 2025-08-01 (but delivery was 2025-04-15)

Seller:
  Name: DEF Supply Co.
  Tax Code: 1111111111
  Address: 789 Market Street, Hanoi

Buyer:
  Name: XYZ Trading JSC
  Tax Code: 9876543210
  Address: 456 Commerce Building, District 1, HCMC

Items:
  | Product | Qty | Unit | Unit Price | Total |
  |---------|-----|------|------------|-------|
  | Office Supplies | 1 | lot | 50,000,000 | 50,000,000 |

VAT: 8% = 4,000,000
Total: 54,000,000 VND

Payment: Cash
Bank: Not applicable
```

**Risk Flags**:
1. **Late Invoice**: Date is 2025-08-01 but delivery was 2025-04-15 (> 90 days late)
2. **Missing Bank Proof**: Amount ≥ 20M VND but paid by cash
3. **Both flags compound**: High audit risk for input VAT deduction

---

## Disclaimer

**This reference document is provided for informational purposes only.**

The information contained herein reflects publicly available regulations as of the skill creation date. Laws and regulations are subject to change. Always verify against the latest official gazettes and consult qualified tax professionals for definitive guidance.

This document does not constitute legal advice. The author and contributors are not responsible for any decisions made based on this information.

**For official guidance**:
- General Department of Taxation website: https://gdt.gov.vn
- Ministry of Finance website: https://mof.gov.vn

---

*Last updated: 2026-07-06*
