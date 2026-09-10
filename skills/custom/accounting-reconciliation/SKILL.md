---
name: accounting-reconciliation
description: >
  Đối chiếu sổ sách kế toán Việt Nam theo TT 99/2025/TT-BTC và TT 200/2014/TT-BTC.
  Trigger khi user cần: đối chiếu công nợ phải thu / phải trả (TK 131/331),
  đối chiếu ngân hàng (TK 112), đối chiếu tồn kho (TK 152/153/155/156),
  xử lý chênh lệch đối chiếu, xác nhận số dư với khách hàng / nhà cung cấp /
  ngân hàng / cơ quan thuế.
version: 1.1.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - reconciliation
  - ar-ap
  - bank-reconciliation
  - inventory-reconciliation
author: DeerFlow Community
created: 2025-07-06
updated: 2026-09-09
legal_basis:
  - Thông tư 99/2025/TT-BTC
  - Thông tư 200/2014/TT-BTC
  - Thông tư 133/2016/TT-BTC
  - Luật Kế toán 88/2015/QH13
---

# Skill Đối chiếu Sổ sách Kế toán

## Mục đích

Hỗ trợ đối chiếu sổ sách kế toán Việt Nam giữa:
- Sổ sách kế toán nội bộ (TK 131, 331, 112, 152/153/155/156, ...)
- Đối tác bên ngoài (khách hàng, nhà cung cấp, ngân hàng, cơ quan thuế)
- Sổ phụ với sổ cái

Xử lý các trường hợp chênh lệch phát sinh từ:
- Giao dịch đã ghi một bên, chưa ghi bên kia
- Chênh lệch thời gian (cut-off)
- Sai lệch số tiền, đơn vị tiền tệ
- Lỗi ghi sổ, nhầm lẫn

## Khi nào sử dụng

- **Đối chiếu công nợ cuối tháng/quý/năm**: xác nhận số dư TK 131/331 với
  từng khách hàng / nhà cung cấp
- **Đối chiếu ngân hàng**: so sánh sổ phụ ngân hàng (bank statement) với
  sổ cái TK 1121/1122/1123
- **Đối chiếu tồn kho**: so sánh sổ chi tiết vật tư / thành phẩm với thẻ kho
- **Quyết toán thuế**: đối chiếu số liệu kế toán với tờ khai thuế, Cổng thuế
- **Kiểm toán nội bộ / kiểm toán độc lập**: cung cấp bảng đối chiếu chuẩn

## Khi nào KHÔNG sử dụng

- **Tính giá xuất kho** (FIFO, bình quân gia quyền) → dùng
  `inventory-fifo-allocation`
- **Lập báo cáo tài chính** → dùng `accounting-financial-reports`
- **Kiểm kê kho** (xử lý thừa/thiếu) → dùng `accounting-stocktake`
- **Kết chuyển cuối kỳ** → dùng `accounting-closing-period`

---

## Đầu vào Bắt buộc

### Đầu vào Chung

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `reconciliation_type` | enum | Có | `"ar"`, `"ap"`, `"bank"`, `"inventory"`, `"tax"`, `"intercompany"`, `"subsidiary_ledger"` |
| `reconciliation_date` | string | Có | Ngày đối chiếu (DD/MM/YYYY hoặc YYYY-MM-DD) |
| `account_balance` | object | Có | Số dư sổ cái của TK cần đối chiếu |
| `external_data` | array | Có | Dữ liệu đối chiếu từ bên ngoài / sổ phụ |
| `tolerance` | object | Tùy chọn | Ngưỡng chấp nhận sai lệch |

### Đầu vào Riêng theo Loại

#### Đối chiếu Công nợ phải thu (AR) / phải trả (AP)

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `partner_id` | string | Có | MST (DN) hoặc CCCD (cá nhân) |
| `partner_name` | string | Có | Tên đối tác |
| `internal_ledger` | array | Có | Sổ chi tiết theo đối tác (mỗi dòng: ngày, số CT, diễn giải, Nợ, Có) |
| `partner_confirmation` | array | Tùy chọn | Xác nhận từ đối tác (thư xác nhận công nợ, sao kê) |

#### Đối chiếu Ngân hàng

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `bank_account_info` | object | Có | Số TK, tên NH, loại tiền |
| `bank_statement` | array | Có | Sao kê ngân hàng (ngày, diễn giải, Nợ, Có, số dư) |
| `cash_book` | array | Có | Sổ tiền (TK 1121/1122/1123) nội bộ |

#### Đối chiếu Tồn kho

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `item_code` | string | Có | Mã hàng hóa |
| `inventory_account` | string | Có | TK kho (152/153/155/156) |
| `stock_card` | array | Có | Thẻ kho (ngày, số CT, nhập, xuất, tồn) |
| `warehouse_record` | array | Tùy chọn | Sổ kho vật lý |

---

## Quy trình Từng bước Chung

### Bước 1: Xác định phạm vi đối chiếu

1. Xác định loại đối chiếu (AR/AP/Bank/Inventory/Tax/Intercompany/Subsidiary)
2. Xác định kỳ đối chiếu
3. Xác định đối tượng đối chiếu (theo từng đối tác / toàn bộ)
4. Lấy số dư sổ cái tại ngày đối chiếu

### Bước 2: Chuẩn bị dữ liệu

1. Xuất sổ chi tiết / sổ phụ từ hệ thống kế toán
2. Yêu cầu xác nhận công nợ từ đối tác (đối với AR/AP)
3. Tải sao kê ngân hàng (đối với Bank)
4. Lấy số liệu từ thẻ kho, sổ kho (đối với Inventory)

### Bước 3: Thực hiện đối chiếu

1. So khớp từng giao dịch (matching) — ưu tiên theo:
   - Số chứng từ / số tham chiếu
   - Số tiền (cho phép sai lệch nhỏ trong tolerance)
   - Ngày giao dịch
2. Ghi nhận các giao dịch đã khớp (matched)
3. Xác định các khoản chênh lệch:
   - Chỉ có bên trong (chưa ghi nhận bên ngoài / chưa đến hạn)
   - Chỉ có bên ngoài (chưa ghi nhận nội bộ)
   - Sai lệch số tiền

### Bước 4: Phân loại chênh lệch

| Loại | Mô tả | Cách xử lý |
|------|-------|------------|
| `timing_difference` | Giao dịch đã phát sinh nhưng chưa đến hạn ghi nhận | Theo dõi, chờ ghi nhận |
| `in_transit` | Đã trả tiền nhưng NCC chưa nhận / đã nhận tiền nhưng chưa ghi sổ | Xác nhận lại |
| `recording_error` | Sai lệch số tiền / nhầm TK | Điều chỉnh bút toán |
| `duplicate_entry` | Ghi trùng | Loại bỏ bút toán trùng |
| `missing_entry` | Chưa ghi sổ | Bổ sung bút toán |
| `exchange_difference` | Chênh lệch tỷ giá | Đánh giá lại TK ngoại tệ (TK 413) |
| `unidentified` | Không xác định được nguyên nhân | Điều tra thêm |

### Bước 5: Sinh bảng đối chiếu

Xuất bảng đối chiếu với:
- Cột bên trong (sổ sách nội bộ)
- Cột bên ngoài (sổ phụ / đối tác)
- Cột chênh lệch
- Cột diễn giải / ghi chú

### Bước 6: Đề xuất xử lý

Với mỗi chênh lệch, đề xuất:
- Bút toán điều chỉnh (nếu có lỗi)
- Bổ sung chứng từ (nếu thiếu)
- Theo dõi tiếp (nếu chưa đến hạn)
- Escalate lên cấp trên (nếu chênh lệch lớn)

---

## Quy trình Riêng theo Loại

### 1. Đối chiếu Công nợ Phải thu (TK 131)

#### Mục tiêu

Xác nhận số dư TK 131 chi tiết theo từng khách hàng tại ngày đối chiếu.

#### Quy trình

1. Lấy sổ chi tiết TK 131 theo từng khách hàng
2. So sánh với thư xác nhận công nợ hoặc sao kê từ khách hàng
3. Lập bảng đối chiếu theo mẫu (xem [Các Loại Đối chiếu](references/reconciliation-types.md))

#### Xử lý chênh lệch phổ biến

| Chênh lệch | Nguyên nhân | Xử lý |
|------------|-------------|-------|
| Khách hàng ghi nhỏ hơn DN | KH chưa ghi nhận hàng về / dịch vụ | Gửi bảng đối chiếu yêu cầu KH xác nhận |
| Khách hàng ghi lớn hơn DN | KH đã ghi nhận hàng chưa xuất hóa đơn | Kiểm tra lại hóa đơn |
| KH đã trả tiền nhưng DN chưa ghi | Thanh toán trong đường (in-transit) | Đối chiếu sao kê NH |
| DN ghi nhận doanh thu nhưng KH không nhận hàng | Có thể là giao dịch ảo / gian lận | Điều tra nội bộ |

#### Bút toán điều chỉnh

Với chênh lệch do sai sót ghi sổ:
```
Nợ/Có TK 131    Điều chỉnh tăng/giảm công nợ phải thu
    Có/Nợ TK 511/711/333    (Tùy nguyên nhân: DT chưa ghi, giảm DT, ...)
```

### 2. Đối chiếu Công nợ Phải trả (TK 331)

Tương tự AR nhưng với TK 331 và phía nhà cung cấp.

### 3. Đối chiếu Ngân hàng (TK 1121/1122/1123)

#### Mục tiêu

So sánh sổ tiền nội bộ với sao kê ngân hàng. Phát hiện các giao dịch:
- Đã ghi nhận nội bộ nhưng NH chưa xử lý (outstanding checks/cheques chưa
  thanh toán)
- Đã xử lý trên NH nhưng chưa ghi nhận nội bộ (deposits in transit / thu
  NH chưa rõ nguồn)

#### Quy trình

1. Lấy sổ tiền (cash book) nội bộ theo từng tài khoản NH
2. Tải sao kê NH tại ngày đối chiếu
3. Khớp từng dòng theo:
   - Số tiền
   - Ngày
   - Nội dung (memo)
   - Số tham chiếu (nếu có)
4. Lập **Bảng Đối chiếu Ngân hàng (Bank Reconciliation Statement)** theo
   mẫu:

```
Số dư sổ tiền nội bộ (TK 1121):          X
Cộng: Thu từ NH chưa ghi sổ              +A
Trừ: Chi từ sổ tiền chưa thanh toán       -B
+/- Điều chỉnh sai lệch                  ±C
                                         ----
Số dư theo sao kê NH:                     Y (phải khớp)
```

#### Xử lý chênh lệch

| Chênh lệch | Xử lý |
|------------|-------|
| Séc đã ký nhưng chưa ghi có trên NH (outstanding cheque) | Ghi nhận vào dòng "Chi chưa thanh toán", theo dõi đến khi NH xử lý |
| Tiền đã về NH nhưng chưa ghi sổ (deposit in transit) | Ghi nhận vào dòng "Thu chưa ghi", theo dõi |
| Phí NH chưa ghi nhận | Tạo bút toán phí NH: Nợ 642 / Có 1121 |
| Lãi NH chưa ghi nhận | Tạo bút toán: Nợ 1121 / Có 515 |
| Chênh lệch tỷ giá | Đánh giá lại TK ngoại tệ (TK 4131 - CLTG đã thực hiện, 4132 - CLTG chưa thực hiện) |
| Sai lệch không xác định | Escalate cho kế toán trưởng |

#### Bút toán điều chỉnh thường gặp

**Phí NH**:
```
Nợ TK 642    Chi phí QLDN
    Có TK 1121   Tiền gửi NH (giảm)
```

**Lãi NH**:
```
Nợ TK 1121    Tiền gửi NH (tăng)
    Có TK 515    Doanh thu hoạt động tài chính
```

**Chênh lệch tỷ giá**:
```
Nợ/Có TK 1122   Tiền gửi (ngoại tệ)
    Có/Nợ TK 413   Chênh lệch tỷ giá
```

### 4. Đối chiếu Tồn kho

So sánh sổ chi tiết vật tư / thành phẩm (theo thẻ kho) với sổ cái TK
152/153/155/156. Nếu chênh lệch → dùng skill `accounting-stocktake` để
kiểm kê xử lý.

### 5. Đối chiếu Thuế

So sánh:
- Sổ sách kế toán (TK 333) với tờ khai thuế đã nộp
- Tờ khai thuế với dữ liệu trên Cổng thuế điện tử
- Hóa đơn đầu vào/ra với tờ khai VAT

### 6. Đối chiếu Liên công ty (Intercompany)

Đối với tập đoàn / công ty mẹ - con: đối chiếu TK 1368 (phải thu khác)
hoặc 3368 (phải trả khác) với bên liên quan.

### 7. Đối chiếu Sổ phụ - Sổ cái (Subsidiary Ledger vs General Ledger)

Đảm bảo tổng số dư các sổ phụ = số dư sổ cái.

---

## Quy tắc Chung

### Nguyên tắc 1: Tổng phải khớp

Tổng dư các sổ chi tiết = Tổng số dư sổ cái. Nếu lệch → tìm ngay.

### Nguyên tắc 2: Sai số phải xác định nguyên nhân

Mọi chênh lệch dù nhỏ cũng cần tìm nguyên nhân. Không được "treo" lại.

### Nguyên tắc 3: Bút toán điều chỉnh đúng kỳ

Bút toán điều chỉnh phải ghi vào **kỳ phát sinh lỗi**, không ghi kỳ hiện
tại (theo Luật Kế toán 88/2015/QH13).

### Nguyên tắc 4: Đối chiếu định kỳ

- Công nợ: đối chiếu hàng tháng, gửi xác nhận công nợ cuối năm
- Ngân hàng: đối chiếu hàng ngày/tháng
- Tồn kho: đối chiếu cuối tháng, kiểm kê định kỳ (cuối năm bắt buộc)

### Nguyên tắc 5: Lưu trữ chứng từ

Bảng đối chiếu phải được lưu trữ cùng chứng từ gốc (5 năm theo Luật Kế
toán).

---

## Quy tắc Chống Ảo giác

### Quy tắc 1: Không tự ý khớp các khoản

Không tự động match các khoản nghi ngờ. Phải có chứng từ gốc hỗ trợ.

### Quy tắc 2: Không điều chỉnh số liệu của đối tác

Bảng đối chiếu phản ánh cả hai phía. Không tự thay đổi số liệu đối tác.

### Quy tắc 3: Không bỏ qua chênh lệch nhỏ

Lệch 1.000 VND cũng cần tìm nguyên nhân. Nếu không xác định được → escalate.

### Quy tắc 4: Trích dẫn chính xác

Khi tham chiếu đến thông tư / điều khoản, ghi rõ số hiệu văn bản và điều
khoản. Không bịa.

### Quy tắc 5: Tách biệt sai sót kỳ này / kỳ trước

Lỗi phát hiện trong kỳ này nhưng phát sinh từ kỳ trước → phải điều chỉnh
vào kỳ trước (nếu nằm trong cùng năm tài chính) hoặc trình bày trong thuyết
minh BCTC.

---

## Định dạng Đầu ra

```json
{
  "skill": "accounting-reconciliation",
  "version": "1.1.0",
  "reconciliation_type": "ar|ap|bank|inventory|tax|intercompany|subsidiary_ledger",
  "reconciliation_date": "DD/MM/YYYY",
  "account_info": {
    "account_code": "131|331|1121|1122|...|152|153|155|156|333",
    "account_name": "",
    "balance_per_ledger": 0,
    "balance_per_external": 0,
    "difference": 0
  },
  "matched_items": [
    {
      "internal_ref": "",
      "external_ref": "",
      "date": "DD/MM/YYYY",
      "description": "",
      "amount": 0,
      "match_confidence": "high|medium|low"
    }
  ],
  "unmatched_items": [
    {
      "side": "internal|external",
      "date": "DD/MM/YYYY",
      "description": "",
      "amount": 0,
      "reference": "",
      "investigation_status": "pending|cleared|escalated",
      "suggested_reason": "timing_difference|in_transit|recording_error|duplicate_entry|missing_entry|exchange_difference|unidentified",
      "proposed_treatment": ""
    }
  ],
  "summary": {
    "total_matched": 0,
    "total_unmatched_internal": 0,
    "total_unmatched_external": 0,
    "net_difference": 0,
    "tolerance_exceeded": false
  },
  "adjustment_entries": [
    {
      "scenario": "",
      "lines": [
        { "account_code": "", "debit": 0, "credit": 0, "description": "" }
      ],
      "legal_reference": ""
    }
  ],
  "flags": [
    {
      "flag": "",
      "severity": "low|medium|high|critical",
      "description": ""
    }
  ],
  "approvals_required": [],
  "disclaimer": "Bảng đối chiếu dựa trên dữ liệu user cung cấp. Cần xác nhận của kế toán trưởng trước khi hạch toán điều chỉnh."
}
```

---

## Quy tắc Escalate

| Tình huống | Mức độ | Người nhận |
|-----------|--------|-----------|
| Chênh lệch > 100 triệu VND | HIGH | Kế toán trưởng + Giám đốc |
| Chênh lệch > 5% tổng số dư | HIGH | Kế toán trưởng |
| Chênh lệch không tìm được nguyên nhân sau 30 ngày | HIGH | Kế toán trưởng + KTNB |
| Nghi ngờ gian lận | CRITICAL | Giám đốc + KTNB + Công an (nếu cần) |
| Xác nhận công nợ bị từ chối / không phản hồi | MEDIUM | Kinh doanh + Kế toán |
| Đối chiếu thuế chênh lệch | HIGH | Kế toán trưởng + Tư vấn thuế |
| Sai lệch tỷ giá > 5% | MEDIUM | Kế toán trưởng |
| Đối chiếu ngân hàng chênh lệch > 30 ngày | HIGH | Kế toán trưởng + NH |

---

## Tuyên bố Miễn trừ Pháp lý

Skill này hỗ trợ lập bảng đối chiếu và đề xuất xử lý. **Không thay thế
phán đoán của kế toán trưởng** về bút toán điều chỉnh.

Khi phát hiện chênh lệch nghiêm trọng:
- Dừng khớp tự động
- Báo cáo cho cấp quản lý
- Không tự ý hạch toán số tiền lớn
- Lưu trữ bảng đối chiếu cùng chứng từ gốc

Các con số và quy định có thể đã thay đổi. Luôn xác minh với văn bản hiện
hành trước khi áp dụng.

---

*Cập nhật lần cuối: 2026-09-09*
*Phiên bản skill: 1.1.0*