---
name: accounting-expense-claim
description: >
  Quản lý tạm ứng, hoàn ứng, và thanh toán chi phí (công tác phí, mua hàng
  nhỏ, ...) theo chế độ kế toán VN. Trigger khi user cần: lập phiếu tạm ứng,
  quyết toán công tác phí, hạch toán hoàn ứng thừa/thiếu, kiểm tra hóa đơn
  kèm theo đề nghị thanh toán, hoặc bất kỳ nghiệp vụ nào liên quan đến đề
  nghị thanh toán / tạm ứng.
version: 1.0.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - expense-claim
  - advance-payment
  - business-trip
---

# Accounting Expense Claim Skill

## Purpose

Hỗ trợ quy trình tạm ứng, hoàn ứng và thanh toán chi phí (công tác phí,
mua hàng nhỏ, ...) theo chế độ kế toán Việt Nam. Validation hóa đơn kèm
theo, tạo bút toán, kiểm tra tính hợp lý của chi phí.

**Legal Framework:**
- Thông tư 99/2025/TT-BTC — Chế độ kế toán DN
- Thông tư 200/2014/TT-BTC — Chế độ kế toán DN
- Thông tư 133/2016/TT-BTC — Chế độ kế toán DN vừa và nhỏ
- Luật Kế toán 88/2015/QH13
- Quy chế công tác phí nội bộ của DN (nếu có)
- Nghị định 70/2017/NĐ-CP về quản lý công tác phí (nếu vẫn còn hiệu lực)

## When to Use

- Lập phiếu tạm ứng (advance request) cho nhân viên
- Hạch toán chi tạm ứng (TK 141)
- Quyết toán công tác phí (business trip settlement)
- Kiểm tra hóa đơn kèm theo đề nghị thanh toán
- Hạch toán hoàn ứng thừa / thiếu
- Lập phiếu chi thanh toán cuối cùng
- Theo dõi tạm ứng chưa quyết toán

## When NOT to Use

- Tính lương và các khoản trích (dùng `accounting-payroll`)
- Thanh toán cho nhà cung cấp (hóa đơn mua hàng thông thường, dùng
  `accounting-journal-entries`)
- Mua TSCĐ (dùng `accounting-fixed-assets`)
- Tính thuế TNCN cho công tác phí (kết hợp với `accounting-payroll`)
- Quản lý hợp đồng mua bán (skill riêng)

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `claim_type` | enum | Yes | `"advance"` (tạm ứng), `"settlement"` (quyết toán), `"payment"` (thanh toán không qua tạm ứng) |
| `employee_id` | string | Yes | Mã nhân viên |
| `employee_name` | string | Yes | Họ tên |
| `department` | string | No | Phòng ban |
| `purpose` | string | Yes | Mục đích (công tác, mua hàng, ...) |
| `amount` | number | Yes | Số tiền (VND) |
| `payment_method` | enum | Yes | `"cash"` (tiền mặt), `"bank_transfer"` (CK ngân hàng) |
| `attachments` | array | No | Hóa đơn, chứng từ kèm theo |
| `trip_details` | object | No | Thông tin công tác (nếu là công tác phí) |

---

## Các loại nghiệp vụ

### 1. Tạm ứng (Advance)

Nhân viên xin tạm ứng tiền để chi cho mục đích công việc.

**Hạch toán**:
```
Nợ TK 141    Tạm ứng (theo NV)
    Có TK 1111 (tiền mặt) hoặc 1121 (CK ngân hàng)
```

### 2. Quyết toán tạm ứng (Settlement)

Nhân viên hoàn ứng (nộp chứng từ + hoàn tiền thừa/thiếu).

**Trường hợp A: Chi phí thực tế = Tạm ứng**
```
Nợ TK 641/642/627    Chi phí SXKD (theo bộ phận)
    Có TK 141          Tạm ứng
```

**Trường hợp B: Chi phí < Tạm ứng (hoàn thừa)**
```
Nợ TK 641/642/627    Chi phí SXKD (chi thực tế)
Nợ TK 1111/1121      Tiền hoàn ứng (phần thừa)
    Có TK 141          Tạm ứng (toàn bộ)
```

**Trường hợp C: Chi phí > Tạm ứng (DN trả thêm)**
```
Nợ TK 641/642/627    Chi phí SXKD (toàn bộ)
    Có TK 141           Tạm ứng (đã chi)
    Có TK 1111/1121     Tiền trả thêm (phần thiếu)
```

### 3. Thanh toán trực tiếp (không qua tạm ứng)

Chi phí phát sinh mà không qua tạm ứng, NV nộp đề nghị thanh toán sau khi chi:

```
Nợ TK 641/642/627    Chi phí SXKD
Nợ TK 133            VAT đầu vào (nếu có)
    Có TK 1111/1121    Tiền thanh toán
```

---

## Công tác phí (Business trip)

### Các khoản công tác phí phổ biến

| Khoản | Mức chi | Hạch toán |
|-------|---------|-----------|
| Tiền vé (máy bay, tàu, xe) | Theo thực tế | CP công tác |
| Tiền ở khách sạn | Theo thực tế + theo quy chế | CP công tác |
| Phụ cấp công tác phí | Theo quy chế DN / NĐ | CP công tác |
| Tiền taxi, xăng xe | Theo thực tế | CP công tác |

### Quyết toán công tác phí

Yêu cầu chứng từ:
- Vé (máy bay, tàu, xe): bản gốc
- Hóa đơn khách sạn (HĐĐT có mã CQT nếu B2B)
- Hóa đơn taxi, ăn uống (nếu quy chế cho phép)
- Bảng kê công tác phí (do NV lập, có xác nhận của quản lý)

**Hạch toán**:
```
Nợ TK 641/642 (CP QLDN)    Chi phí công tác
    Có TK 141                Tạm ứng (nếu có)
    Có TK 1111/1121          Tiền hoàn ứng hoặc thanh toán
```

---

## Validation chứng từ kèm theo

### Các loại chứng từ hợp lệ

| Chứng từ | Sử dụng cho |
|---------|-------------|
| HĐĐT có mã CQT | Chi phí B2B, có khấu trừ VAT |
| HĐĐT không mã CQT | Chi phí B2C, không khấu trừ VAT |
| Biên lai thu phí (nếu còn) | Phí hành chính |
| Vé máy bay / xe | Công tác |
| Hóa đơn khách sạn | Công tác |
| Giấy giới thiệu / Quyết định cử đi công tác | Công tác |

### Validation rules

| Rule | Mô tả | Hành động nếu fail |
|------|-------|---------------------|
| `invoice_valid_format` | Hóa đơn đúng format (HĐĐT hoặc HĐ giấy còn hiệu lực) | Flag `invalid_invoice` |
| `mst_seller_active` | MST người bán đang hoạt động | Flag `mst_inactive` |
| `invoice_within_period` | Hóa đơn trong kỳ thanh toán | Flag `out_of_period` |
| `vat_evidence` | Có hóa đơn VAT nếu claim VAT | Flag `missing_vat_invoice` |
| `bank_proof_required` | Chi ≥ 20 triệu phải có chứng từ CK NH | Flag `missing_bank_proof` |
| `trip_authorization` | Có quyết định cử đi công tác (nếu công tác phí) | Flag `no_authorization` |

### Anti-hallucination: Không tự verify HĐĐT

Không thể tự xác minh mã CQT. Flag nếu thiếu, yêu cầu NV cung cấp kết quả
tra cứu từ Cổng thuế.

---

## Step-by-Step Workflow

### Workflow 1: Tạm ứng

```
1. NV nộp đơn xin tạm ứng (mục đích, số tiền)
2. Quản lý duyệt
3. Kế toán lập phiếu chi tạm ứng
4. Chi tiền (CK NH hoặc tiền mặt)
5. Hạch toán: Nợ 141 / Có 1111 hoặc 1121
6. Theo dõi trong sổ TK 141 (theo NV)
```

### Workflow 2: Quyết toán tạm ứng

```
1. NV hoàn ứng (nộp chứng từ + tiền thừa hoặc xin trả thêm)
2. Kế toán kiểm tra chứng từ:
   - Validate hóa đơn
   - Kiểm tra số tiền
   - Kiểm tra mục đích chi
3. Lập phiếu quyết toán
4. Phê duyệt
5. Hạch toán (3 trường hợp A/B/C ở trên)
6. Chi tiền hoàn ứng hoặc nhận tiền thừa
```

### Workflow 3: Thanh toán không qua tạm ứng

```
1. NV chi tiền (thường cho chi phí nhỏ, cấp bách)
2. NV nộp đề nghị thanh toán (kèm hóa đơn, chứng từ)
3. Kế toán kiểm tra chứng từ
4. Phê duyệt
5. Lập phiếu chi thanh toán
6. Hạch toán: Nợ 641/642/133 / Có 1111 hoặc 1121
```

---

## Anti-Hallucination Rules

### Rule 1: Không tự duyệt chi phí

Mọi đề nghị thanh toán cần **phê duyệt của quản lý trực tiếp + kế toán
trưởng** (tùy mức giá trị). Skill chỉ tạo bút toán, không thay thế phê
duyệt.

### Rule 2: Không tự verify hóa đơn

Không thể verify HĐĐT có hợp lệ hay không mà không tra cứu trên Cổng thuế.
Skill chỉ kiểm tra format và sự đầy đủ của chứng từ.

### Rule 3: Không tự áp mức phụ cấp công tác

Mức phụ cấp công tác phí theo:
- Quy chế nội bộ của DN
- Hoặc NĐ/TT của nhà nước (nếu có)
- Không tự ý đặt mức → yêu cầu user xác nhận

### Rule 4: Không tự bù trừ chi phí không hợp lệ

Nếu chứng từ không hợp lệ → flag, không tự ý hạch toán vào chi phí khác
hoặc loại bỏ.

### Rule 5: Không tự ý chuyển đề nghị thành tạm ứng

Đề nghị thanh toán (sau khi chi) ≠ Tạm ứng (trước khi chi). Phân biệt rõ
trong output.

---

## Output Format

```json
{
  "skill": "accounting-expense-claim",
  "version": "1.0.0",
  "claim_type": "advance|settlement|payment",
  "claim_id": "REQ-{YYYYMMDD}-{SEQ}",
  "employee_info": {
    "employee_id": "",
    "name": "",
    "department": ""
  },
  "purpose": "",
  "amount": 0,
  "payment_method": "cash|bank_transfer",
  "attachments_validated": [
    {
      "attachment_type": "einvoice|hotel_invoice|transport_ticket|trip_decision",
      "invoice_number": "",
      "date": "DD/MM/YYYY",
      "amount": 0,
      "validation_status": "valid|warning|invalid",
      "issues": []
    }
  ],
  "validation_result": {
    "all_attachments_valid": true,
    "bank_proof_present": true,
    "trip_authorization_present": true,
    "issues": []
  },
  "journal_entry": {
    "debit_account": "",
    "credit_account": "",
    "amount": 0,
    "vat_amount": 0,
    "description": "",
    "legal_reference": ""
  },
  "settlement_details": {
    "advance_amount": 0,
    "actual_expense": 0,
    "refund_to_company": 0,
    "additional_payment": 0
  },
  "flags": [],
  "recommendations": [],
  "disclaimer": "Đề nghị thanh toán dựa trên dữ liệu user cung cấp. Cần phê duyệt quản lý + kế toán trưởng trước khi chi."
}
```

---

## Theo dõi tạm ứng chưa quyết toán

Cần theo dõi sổ TK 141 chi tiết theo từng nhân viên:

| NV | Tạm ứng | Đã quyết toán | Còn lại | Quá hạn? |
|----|---------|---------------|---------|---------|
| Nguyễn Văn A | 5,000,000 | 4,500,000 | 500,000 | Không |
| Trần Thị B | 10,000,000 | 0 | 10,000,000 | Có (>30 ngày) |

**Quy định thời hạn quyết toán**: Theo quy chế DN, thường:
- Tạm ứng công tác phí: quyết toán trong **7-15 ngày** sau khi kết thúc
  công tác
- Tạm ứng mua hàng: trong **3-7 ngày** sau khi giao hàng
- Trường hợp đặc biệt: có thể kéo dài hơn

NV còn tạm ứng chưa quyết toán > 30 ngày → **flag** cho kế toán trưởng.

---

## Escalation Rules

| Tình huống | Mức độ | Recipient |
|-----------|--------|-----------|
| Chi phí không có hóa đơn > 5 triệu | HIGH | Kế toán trưởng |
| Chi phí > 50 triệu/lần | MEDIUM | Kế toán trưởng + Giám đốc |
| Tạm ứng > 100 triệu | HIGH | Giám đốc |
| Tạm ứng quá hạn > 30 ngày | MEDIUM | Quản lý trực tiếp + Kế toán trưởng |
| NV nộp chứng từ không hợp lệ | MEDIUM | Kế toán trưởng |
| Công tác phí vượt quy chế DN | HIGH | Giám đốc |
| Chi phí ngoài phạm vi SXKD | HIGH | Giám đốc |
| Phát hiện dấu hiệu gian lận | CRITICAL | Giám đốc + Kiểm toán nội bộ |

---

## Legal Disclaimer

Skill này hỗ trợ tạo bút toán cho đề nghị thanh toán và quyết toán tạm
ứng. **Không thay thế phê duyệt của cấp quản lý.** Mọi chi phí cần được
kiểm tra:
- Có hóa đơn, chứng từ hợp lệ
- Phù hợp mục đích SXKD
- Được duyệt bởi người có thẩm quyền
- Phù hợp quy chế nội bộ DN
- Tuân thủ quy định pháp luật (thuế TNDN, TNCN nếu có)

Quy chế công tác phí và đề nghị thanh toán cần được HĐQT / Ban Giám đốc
ban hành văn bản. Kế toán trưởng chịu trách nhiệm cuối cùng về tính hợp
pháp, hợp lý của các khoản chi.