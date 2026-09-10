---
name: accounting-journal-entries
description: >
  Tự động định khoản và tạo bút toán kép (double-entry) cho giao dịch kế toán
  theo TT 99/2025/TT-BTC (hiệu lực 01/01/2026), TT 200/2014/TT-BTC và TT
  133/2016/TT-BTC. Trigger khi user cần: định khoản giao dịch, tạo phiếu kế
  toán, hạch toán mua bán hàng, thu chi tiền, khấu hao, phân bổ chi phí, kết
  chuyển cuối kỳ, hoặc bất kỳ yêu cầu nào liên quan đến bút toán / journal
  entry / hạch toán kế toán.
version: 1.1.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
---

# Accounting Journal Entries Skill

## Purpose

Tự động sinh bút toán kép (double-entry journal entries) cho các giao dịch kế
toán phổ biến theo chế độ kế toán Việt Nam. Skill này map giao dịch → tài
khoản → bút toán Nợ/Có với đầy đủ legal reference.

**Legal Framework:**
- Thông tư 200/2014/TT-BTC — Chế độ kế toán doanh nghiệp (DN lớn)
- Thông tư 133/2016/TT-BTC — Chế độ kế toán DN vừa và nhỏ
- **Thông tư 99/2025/TT-BTC** — Hệ thống tài khoản kế toán (hiệu lực 01/01/2026)
- Luật Kế toán 88/2015/QH13

**Account Mapping:** xem [`references/account-mapping.md`](references/account-mapping.md)
để biết ánh xạ TK giữa TT 99/2025 ↔ TT 200/2014 ↔ TT 133/2016.

## When to Use

- Định khoản giao dịch mua hàng, bán hàng, thu tiền, chi tiền
- Tạo bút toán kết chuyển cuối kỳ (closing entries)
- Hạch toán lương và các khoản trích theo lương
- Hạch toán khấu hao tài sản cố định
- Phân bổ chi phí trả trước, công cụ dụng cụ
- Ghi nhận doanh thu chưa thực hiện
- Hạch toán thuế (VAT đầu ra, VAT đầu vào, thuế TNDN tạm tính)
- Bút toán điều chỉnh (adjusting entries) cuối kỳ

## When NOT to Use

- Tính toán số tiền thuế phải nộp → dùng `accounting-tax-vat`
- Đối chiếu sổ sách với chứng từ → dùng `accounting-reconciliation`
- Phân bổ tồn kho theo FIFO → dùng `inventory-fifo-allocation`
- Lập báo cáo tài chính → dùng `accounting-financial-reports`
- Tư vấn chính sách kế toán, lựa chọn phương pháp

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `regime` | enum | Yes | `"tt200"` hoặc `"tt133"` |
| `company_info` | object | Yes | Tên, mã số thuế, loại hình DN |
| `transactions` | array | Yes | Danh sách giao dịch cần định khoản |
| `transactions[].id` | string | Yes | Mã giao dịch |
| `transactions[].date` | string | Yes | Ngày giao dịch (DD/MM/YYYY) |
| `transactions[].type` | enum | Yes | Loại giao dịch (xem Transaction Types) |
| `transactions[].amount_vnd` | number | Yes | Số tiền VND |
| `transactions[].description` | string | Yes | Diễn giải giao dịch |
| `transactions[].metadata` | object | No | Thông tin bổ sung theo từng loại giao dịch |
| `accounting_period` | object | Yes | `{ start_date, end_date }` DD/MM/YYYY |

## Transaction Types

### Nhóm 1: Mua hàng / Chi phí

| `type` | Diễn giải | Metadata cần thêm |
|--------|-----------|-------------------|
| `purchase_goods` | Mua hàng hóa / NVL | `supplier`, `vat_rate`, `payment_method` |
| `purchase_fixed_asset` | Mua TSCĐ | `asset_code`, `useful_life_years`, `vat_rate` |
| `purchase_service` | Mua dịch vụ | `service_type`, `vat_rate` |
| `prepaid_expense` | Chi phí trả trước | `allocation_months` |
| `tools_allocation` | Phân bổ CCDC | `allocation_months`, `allocation_method` |

### Nhóm 2: Bán hàng / Doanh thu

| `type` | Diễn giải | Metadata cần thêm |
|--------|-----------|-------------------|
| `sale_goods` | Bán hàng hóa | `customer`, `vat_rate`, `cost_of_goods` |
| `sale_service` | Cung cấp dịch vụ | `customer`, `vat_rate` |
| `sales_return` | Hàng bán trả lại | `original_invoice`, `vat_rate` |
| `deferred_revenue` | Doanh thu chưa thực hiện | `recognition_schedule` |

### Nhóm 3: Thu / Chi tiền

| `type` | Diễn giải | Metadata cần thêm |
|--------|-----------|-------------------|
| `cash_receipt` | Thu tiền mặt | `from_account` (TK đối ứng) |
| `bank_receipt` | Thu tiền ngân hàng | `bank_account`, `from_account` |
| `cash_payment` | Chi tiền mặt | `to_account` |
| `bank_payment` | Chi tiền ngân hàng | `bank_account`, `to_account` |
| `advance_payment` | Tạm ứng | `employee_id` |
| `advance_settlement` | Hoàn ứng | `advance_ref` |

### Nhóm 4: Lương và các khoản trích

| `type` | Diễn giải | Metadata cần thêm |
|--------|-----------|-------------------|
| `payroll` | Hạch toán lương | `bhxh_employee`, `bhyt_employee`, `bhtn_employee`, `pit_withhold`, `cost_center` |
| `payroll_contribution` | Trích BHXH/BHYT/BHTN phía DN | `bhxh_employer`, `bhyt_employer`, `bhtn_employer` |
| `payroll_payment` | Chi trả lương | `net_amount` |

### Nhóm 5: Cuối kỳ

| `type` | Diễn giải | Metadata cần thêm |
|--------|-----------|-------------------|
| `depreciation` | Khấu hao TSCĐ | `asset_code`, `depreciation_amount`, `cost_center` |
| `closing_revenue` | Kết chuyển doanh thu | `revenue_accounts` |
| `closing_expense` | Kết chuyển chi phí | `expense_accounts` |
| `corporate_tax_provision` | Tạm tính thuế TNDN | `taxable_profit`, `tax_rate` |
| `vat_offset` | Bù trừ VAT đầu vào/đầu ra | `input_vat`, `output_vat` |

---

## Step-by-Step Workflow

### Step 1: Xác định chế độ kế toán

```
IF regime == "tt200":
    chart_of_accounts = TT200_ACCOUNTS  (hệ thống 3-4 chữ số đầy đủ)
    reference_law = "Thông tư 200/2014/TT-BTC"
ELIF regime == "tt133":
    chart_of_accounts = TT133_ACCOUNTS  (hệ thống rút gọn)
    reference_law = "Thông tư 133/2016/TT-BTC"

NOTE: Từ 01/01/2026, đồng thời tham chiếu TT 99/2025/TT-BTC cho hệ thống
tài khoản cập nhật.
```

### Step 2: Map giao dịch → template bút toán

Tra cứu `JOURNAL_ENTRY_TEMPLATES` theo `transaction.type`. Mỗi template chứa:
- Tài khoản Nợ (debit accounts)
- Tài khoản Có (credit accounts)
- Điều kiện phân nhánh (nếu có)
- Legal reference

### Step 3: Populate số liệu

Thay thế placeholders trong template bằng giá trị thực tế:
- `{amount}` → `transaction.amount_vnd`
- `{vat_amount}` → `amount * vat_rate / (100 + vat_rate)` hoặc `amount * vat_rate / 100`
- `{net_amount}` → amount sau khi trừ các khoản khấu trừ

**CRITICAL:** Luôn verify: **Tổng Nợ = Tổng Có** cho mỗi bút toán.

### Step 4: Validate

```python
def validate_entry(entry):
    # Rule 1: Cân bằng Nợ/Có
    assert sum(line.debit for line in entry.lines) == \
           sum(line.credit for line in entry.lines), \
           "BALANCE_ERROR: Nợ ≠ Có"

    # Rule 2: Không có dòng vừa Nợ vừa Có
    for line in entry.lines:
        assert not (line.debit > 0 and line.credit > 0), \
               "MIXED_ENTRY_ERROR"

    # Rule 3: Tài khoản tồn tại trong chart of accounts
    for line in entry.lines:
        assert line.account_code in chart_of_accounts, \
               f"INVALID_ACCOUNT: {line.account_code}"

    # Rule 4: Số tiền > 0
    for line in entry.lines:
        assert line.debit >= 0 and line.credit >= 0
        assert line.debit + line.credit > 0
```

### Step 5: Output

Trả về danh sách bút toán đã validate, kèm legal reference cho mỗi entry.

---

## Journal Entry Templates

### T1: Mua hàng hóa / NVL có VAT (TT200)

```
Nghiệp vụ: Mua hàng hóa nhập kho, có hóa đơn VAT, thanh toán chuyển khoản

Nợ TK 152/156    Giá trị hàng hóa (chưa VAT)
Nợ TK 133        VAT đầu vào
    Có TK 331    Phải trả người bán (nếu chưa thanh toán)
    Có TK 112    Tiền gửi ngân hàng (nếu thanh toán ngay)

Legal: Điều 24, TT 200/2014/TT-BTC; Điều 14, Luật 48/2024/QH15 (VAT)
```

### T2: Bán hàng hóa có VAT (TT200)

```
Nghiệp vụ: Ghi nhận doanh thu bán hàng

Bước 1 - Ghi nhận doanh thu:
Nợ TK 131/112    Phải thu / Tiền về
    Có TK 511    Doanh thu bán hàng (chưa VAT)
    Có TK 3331   VAT đầu ra phải nộp

Bước 2 - Ghi nhận giá vốn:
Nợ TK 632        Giá vốn hàng bán
    Có TK 155/156  Thành phẩm / Hàng hóa

Legal: Điều 54, TT 200/2014/TT-BTC
```

### T3: Hạch toán lương (TT200)

```
Nghiệp vụ: Tính lương và các khoản trích theo lương

Bước 1 - Tính lương phải trả:
Nợ TK 641/642/622/623  Chi phí (theo bộ phận)
    Có TK 334           Phải trả người lao động (lương gross)

Bước 2 - Trích BHXH/BHYT/BHTN phần người lao động:
Nợ TK 334               Trừ vào lương NLĐ
    Có TK 3383/3384/3386  BHXH/BHYT/BHTN phải nộp (phần NLĐ)

Bước 3 - Trích phần doanh nghiệp:
Nợ TK 641/642/622/623  Chi phí (theo bộ phận)
    Có TK 3383/3384/3386  BHXH/BHYT/BHTN (phần DN)

Tỷ lệ trích theo Nghị định 58/2020/NĐ-CP (áp dụng từ 15/9/2020, hiệu lực
đến khi có văn bản thay thế — **cần xác minh tỷ lệ hiện hành tại thời điểm
áp dụng trên Cổng BHXH Việt Nam hoặc tổ chức BHXH**):
- BHXH: NLĐ 8%, DN 17.5%
- BHYT: NLĐ 1.5%, DN 3%
- BHTN: NLĐ 1%, DN 1%
- KPCĐ (Công đoàn): DN 2% (một số trường hợp)

Legal: Điều 64, TT 200/2014/TT-BTC; NĐ 58/2020/NĐ-CP
```

### T4: Kết chuyển cuối kỳ (TT200)

```
Nghiệp vụ: Kết chuyển doanh thu và chi phí để xác định kết quả kinh doanh

Bước 1 - Kết chuyển doanh thu:
Nợ TK 511/512/515    Doanh thu
    Có TK 911         Xác định KQKD

Bước 2 - Kết chuyển chi phí:
Nợ TK 911            Xác định KQKD
    Có TK 631/632/641/642/811/...  Các TK chi phí

Bước 3 - Kết chuyển lãi (nếu lãi):
Nợ TK 911
    Có TK 421

Bước 3' - Kết chuyển lỗ (nếu lỗ):
Nợ TK 421
    Có TK 911

Legal: Điều 79, TT 200/2014/TT-BTC
```

### T5: Bù trừ VAT (TT200)

```
Nghiệp vụ: Bù trừ VAT đầu vào với VAT đầu ra cuối kỳ

Trường hợp VAT đầu ra > VAT đầu vào (phải nộp thêm):
Nợ TK 3331   VAT đầu ra
    Có TK 133  VAT đầu vào (toàn bộ)
→ Số dư Nợ TK 3331 là VAT phải nộp

Trường hợp VAT đầu vào > VAT đầu ra (được khấu trừ/hoàn):
Nợ TK 3331   VAT đầu ra (toàn bộ)
    Có TK 133  VAT đầu vào
→ Số dư Có TK 133 là VAT được khấu trừ kỳ sau hoặc xin hoàn

Legal: Điều 15, TT 200/2014/TT-BTC; Điều 15, Luật 48/2024/QH15
```

### T6: Tương đương TT133 (rút gọn)

TT133 dùng hệ thống tài khoản rút gọn. Mapping chính:

| TT200 | TT133 | Diễn giải |
|-------|-------|-----------|
| 152, 153, 156 | 152, 153 | Hàng tồn kho |
| 641, 642 | 642 | Chi phí bán hàng + QLDN gộp |
| 211, 213 | 211 | TSCĐ |
| 421 | 421 | LNST chưa phân phối |

---

## TT133 vs TT200 — Key Differences

| Điểm khác biệt | TT200 | TT133 |
|----------------|-------|-------|
| Hệ thống TK | Đầy đủ (~100 TK) | Rút gọn (~40 TK) |
| Chi phí BH + QLDN | TK 641 + 642 tách riêng | TK 642 gộp chung |
| TSCĐ vô hình | TK 213 riêng | Gộp vào TK 211 |
| Phương pháp tồn kho | Kê khai thường xuyên hoặc kiểm kê định kỳ | Kê khai thường xuyên |
| Phù hợp với | DN lớn, niêm yết | DN vừa, nhỏ, siêu nhỏ |

---

## Anti-Hallucination Rules

### Rule 1: Không tự tạo tài khoản

Chỉ dùng tài khoản có trong hệ thống TT200, TT133, hoặc TT99/2025.
**SAI:** "Tôi sẽ dùng TK 999 để ghi nhận khoản này."
**ĐÚNG:** "Khoản này không có template chuẩn. Escalate để kế toán xác định."

### Rule 2: Luôn cite điều khoản

**SAI:** "Hạch toán Nợ TK 334, Có TK 111."
**ĐÚNG:** "Theo Điều 64, TT 200/2014/TT-BTC: Nợ TK 334 / Có TK 111."

### Rule 3: Không tính thuế thay

**SAI:** "Thuế TNDN phải nộp là X VND."
**ĐÚNG:** "Bút toán tạm tính thuế TNDN dựa trên số liệu user cung cấp. Xác nhận với kế toán trưởng trước khi hạch toán."

### Rule 4: Flag giao dịch bất thường

Nếu số tiền vượt ngưỡng hoặc tài khoản đối ứng bất thường:
```
FLAG: Giao dịch {id} có giá trị {amount} VND sử dụng tài khoản {account}.
Đây là giao dịch không thường xuyên. Đề xuất review bởi kế toán trưởng.
```

---

## Output Format

```json
{
  "skill": "accounting-journal-entries",
  "version": "1.0.0",
  "regime": "tt200|tt133",
  "accounting_period": { "start_date": "", "end_date": "" },
  "company_info": { "name": "", "tax_code": "" },
  "journal_entries": [
    {
      "entry_id": "JE-{YYYYMMDD}-{SEQ}",
      "transaction_id": "string",
      "date": "DD/MM/YYYY",
      "description": "string",
      "transaction_type": "string",
      "lines": [
        {
          "line_no": 1,
          "account_code": "string",
          "account_name": "string",
          "debit": 0,
          "credit": 0,
          "description": "string"
        }
      ],
      "total_debit": 0,
      "total_credit": 0,
      "balanced": true,
      "legal_reference": "string",
      "flags": [],
      "status": "POSTED|DRAFT|FLAGGED"
    }
  ],
  "summary": {
    "total_entries": 0,
    "total_posted": 0,
    "total_flagged": 0,
    "total_draft": 0,
    "balance_errors": []
  },
  "escalations": [],
  "disclaimer": "Bút toán được tạo tự động. Kế toán trưởng cần review trước khi ghi sổ chính thức."
}
```

---

## Escalation Rules

Escalate khi:
- Giao dịch > 500,000,000 VND
- Tài khoản đối ứng không có trong template chuẩn
- Giao dịch liên quan đến bên liên kết (related party)
- Cần phân bổ giữa nhiều kỳ kế toán
- Giao dịch ngoại tệ (cần xử lý tỷ giá)
- Giao dịch đặc thù ngành (xây dựng, ngân hàng, bảo hiểm)

---

## Legal Disclaimer

Skill này tạo bút toán dự thảo theo các template chuẩn. Không thay thế phán
quyết nghề nghiệp của kế toán viên. Kế toán trưởng chịu trách nhiệm cuối cùng
về tính đúng đắn của số liệu kế toán. Tham chiếu luật có thể thay đổi — kiểm
tra phiên bản hiện hành tại Cổng thông tin điện tử Bộ Tài chính.
