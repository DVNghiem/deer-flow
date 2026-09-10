---
name: accounting-stocktake
description: >
  Kiểm kê tồn kho và xử lý chênh lệch thừa / thiếu theo TT 99/2025/TT-BTC
  và TT 200/2014/TT-BTC. Trigger khi user cần: lập biên bản kiểm kê, so
  sánh tồn kho sổ sách với thực tế, hạch toán hàng thừa, hạch toán hàng
  thiếu trong định mức hao hụt / ngoài định mức, xử lý bồi thường NLĐ,
  giảm trừ VAT đầu vào tương ứng với hàng thiếu không rõ nguyên nhân.
version: 1.0.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - inventory
  - stocktake
  - shortage
  - excess
---

# Accounting Stocktake Skill

## Purpose

Hỗ trợ kiểm kê tồn kho và xử lý chênh lệch giữa sổ sách kế toán và thực
tế. Lập biên bản kiểm kê, xác định nguyên nhân chênh lệch, hạch toán xử lý
theo đúng quy định Việt Nam.

**Legal Framework:**
- Thông tư 99/2025/TT-BTC — Chế độ kế toán DN
- Thông tư 200/2014/TT-BTC — Chế độ kế toán DN
- Thông tư 133/2016/TT-BTC — Chế độ kế toán DN vừa và nhỏ
- Luật Kế toán 88/2015/QH13 — Quy định về kiểm kê
- Luật Thuế GTGT 48/2024/QH15 — Điều kiện khấu trừ VAT đầu vào

## When to Use

- Lập biên bản kiểm kê kho (theo định kỳ hoặc đột xuất)
- So sánh tồn kho sổ sách với thực tế
- Xử lý hàng thừa (phát hiện tăng so với sổ sách)
- Xử lý hàng thiếu (phát hiện giảm so với sổ sách)
- Phân loại nguyên nhân hàng thiếu (hao hụt tự nhiên, mất mát, hư hỏng)
- Hạch toán bồi thường NLĐ
- Xử lý VAT đầu vào tương ứng với hàng thiếu (nếu có)

## When NOT to Use

- Phân bổ tồn kho cho đơn hàng / BOM (dùng `inventory-fifo-allocation`)
- Tính giá xuất kho theo phương pháp (FIFO, bình quân gia quyền, ...)
- Phân tích tồn kho tối ưu
- Lập báo cáo quản trị về tồn kho
- Quản lý kho vật lý (WMS)
- Đánh giá lại tồn kho (revaluation)

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `stocktake_date` | string | Yes | Ngày kiểm kê (DD/MM/YYYY) |
| `location` | string | No | Kho / vị trí kiểm kê |
| `book_inventory` | array | Yes | Tồn kho theo sổ sách (item_code, item_name, qty, value, ...) |
| `actual_inventory` | array | Yes | Tồn kho thực tế đếm được |
| `allowance_rates` | object | No | Tỷ lệ hao hụt cho phép (theo từng nhóm hàng) |
| `investigation_notes` | object | No | Kết quả điều tra nguyên nhân |

---

## Phân loại chênh lệch

### Hàng thừa (Actual > Book)

| Tình huống | Nguyên nhân | Xử lý |
|-----------|-------------|-------|
| Có chứng từ nhập | Nhập kho nhưng quên ghi sổ | Ghi tăng kho + điều chỉnh phiếu nhập |
| Không rõ nguồn gốc | Không xác định được | Ghi nhận thu nhập khác (TK 711) |
| Từ nhà cung cấp gửi nhầm | NCC gửi thừa | Trả lại / ghi nhận hàng nhận giữ hộ (TK 002) |
| Từ khách hàng trả | KH trả hàng đã bán | Tùy trường hợp (xử lý đơn hàng) |

### Hàng thiếu (Actual < Book)

| Tình huồng | Nguyên nhân | Xử lý |
|-----------|-------------|-------|
| Hao hụt trong định mức | Bay hơi, vỡ, hao mòn tự nhiên | CP SXKD (TK 632 hoặc 811) |
| Hao hụt ngoài định mức | Mất mát, hư hỏng không lý do | CP khác (TK 811) + xử lý trách nhiệm |
| NLĐ làm hư hỏng | NV làm hỏng | CP khác + phải thu NLĐ (TK 138) |
| NLĐ lấy cắp / tham ô | Gian lận | CP khác + phải thu NLĐ + có thể truy cứu PL |
| Lỗi sổ sách | Ghi sai số lượng | Điều chỉnh lại sổ |

### Lưu ý về VAT

Khi hàng thiếu không rõ nguyên nhân (có dấu hiệu gian lận / sử dụng không
đúng mục đích):
- **Phải giảm trừ VAT đầu vào** tương ứng với giá trị hàng thiếu
- Theo Luật 48/2024/QH15, hàng hóa bị thiếu không có lý do hợp lý thì
  VAT đầu vào tương ứng không được khấu trừ

---

## Step-by-Step Workflow

### Bước 1: Chuẩn bị kiểm kê

```
1. Ra quyết định kiểm kê (Giám đốc ký)
2. Thành lập hội đồng kiểm kê:
   - Chủ trì: Phó Giám đốc / Trưởng phòng
   - Thành viên: Kế toán kho, thủ kho, NV kiểm kê
   - Thư ký: ghi chép
3. Xác định thời gian, địa điểm kiểm kê
4. Khoá sổ kho (ngưng nhập/xuất trong thời gian kiểm kê)
```

### Bước 2: Tiến hành kiểm kê

```
1. Đếm số lượng thực tế từng mặt hàng
2. Cân / đo (nếu cần)
3. Kiểm tra chất lượng (phân loại A/B/C, hạn sử dụng, ...)
4. Ghi vào bảng kiểm kê (theo mẫu)
5. Ký xác nhận của thành viên hội đồng
```

### Bước 3: Lập biên bản kiểm kê

Biên bản gồm:
- Thời gian, địa điểm
- Thành phần hội đồng
- Phương pháp kiểm kê
- Bảng tổng hợp chênh lệch (thừa/thiếu)
- Nguyên nhân (nếu xác định được)
- Đề xuất xử lý
- Chữ ký các bên

### Bước 4: So sánh sổ sách vs thực tế

```
for each item:
    book_qty = tồn kho sổ sách
    actual_qty = tồn kho thực tế
    diff = actual_qty - book_qty
    if diff > 0: hàng thừa
    if diff < 0: hàng thiếu (lấy abs(diff))
```

### Bước 5: Điều tra nguyên nhân

| Vấn đề | Câu hỏi cần trả lời |
|--------|---------------------|
| Hàng thừa | Có hóa đơn nhập không? Có lý do không? |
| Hàng thiếu | Có biên bản xuất không? Trong định mức? NV chịu trách nhiệm? |
| NV lấy cắp | Bằng chứng? |
| Lỗi sổ | Kiểm tra phiếu nhập/xuất? |

### Bước 6: Hạch toán xử lý

#### 6.1. Hàng thừa

**Trường hợp 1: Có hóa đơn nhập nhưng quên ghi sổ**
```
Ghi bổ sung phiếu nhập kho
Nợ TK 152/153/155/156    Hàng tồn kho
    Có TK 331/1111/1121   Phải trả NCC / Tiền
```

**Trường hợp 2: Không rõ nguồn gốc**
```
Nợ TK 152/153/155/156    Hàng tồn kho (giá trị thị trường)
    Có TK 711              Thu nhập khác
```

#### 6.2. Hàng thiếu

**Trường hợp 1: Hao hụt trong định mức**
```
Nợ TK 632 (giá vốn) hoặc TK 811 (CP khác)
    Có TK 152/153/155/156   Hàng tồn kho
```

**Trường hợp 2: Hao hụt ngoài định mức / mất mát**
```
Nợ TK 811              Chi phí khác
    Có TK 152/153/155/156   Hàng tồn kho

Nếu NLĐ bồi thường:
Nợ TK 138              Phải thu NLĐ
    Có TK 711             Thu nhập khác (hoặc Có TK 811 nếu không có TN)
```

**Trường hợp 3: Giảm trừ VAT đầu vào (nếu hàng thiếu không rõ nguyên nhân)**

Khi hàng thiếu > định mức, không rõ nguyên nhân, có dấu hiệu sử dụng không
đúng mục đích:
```
Nợ TK 811              Chi phí khác (phần VAT)
    Có TK 1331            Thuế GTGT đầu vào (giảm)
```

> ⚠️ Việc giảm trừ VAT đầu vào chỉ áp dụng khi:
> - Hàng thiếu không có lý do hợp lý
> - Có dấu hiệu sử dụng vào mục đích không chịu thuế / không được khấu trừ
> - Cần tham khảo tư vấn thuế trước khi áp dụng

#### 6.3. Điều chỉnh sai sổ

```
Điều chỉnh lại phiếu nhập/xuất sai
Đảo dấu bút toán cũ + ghi bút toán mới
```

### Bước 7: Lập BCTC sau kiểm kê

Sau kiểm kê, giá trị tồn kho được điều chỉnh. Nếu dùng **phương pháp
kiểm kê định kỳ**, cuối kỳ:
- Tính giá vốn hàng bán = Giá trị đầu kỳ + Mua trong kỳ - Giá trị cuối kỳ
  (theo kiểm kê thực tế)
- Hạch toán tăng/giảm giá vốn

---

## Anti-Hallucination Rules

### Rule 1: Không tự ý xác định nguyên nhân

Nếu không có thông tin điều tra → flag `pending_investigation`, không tự
phân loại nguyên nhân.

### Rule 2: Không tự ý khẳng định NV trộm cắp

Đây là phán đoán pháp lý nghiêm trọng. Skill chỉ flag `unexplained_shortage`,
KHÔNG kết luận "NV lấy cắp". Để Hội đồng kiểm kê + Giám đốc kết luận.

### Rule 3: Không tự đặt tỷ lệ hao hụt định mức

Tỷ lệ hao hụt định mức phải do:
- Cơ quan có nh quyền quy định (vd: Bộ, ngành)
- Hoặc quy chế nội bộ DN
- Hoặc thực tế phát sinh có xác nhận

Không tự ý lấy tỷ lệ.

### Rule 4: Không tự giảm trừ VAT

Giảm trừ VAT đầu vào là quyết định phức tạp. Flag nếu có dấu hiệu, để kế
toán trưởng / tư vấn thuế quyết định.

### Rule 5: Trình tự xử lý phải đúng

Phải có đầy đủ:
- Quyết định kiểm kê
- Biên bản kiểm kê (đúng thành phần, đúng nội dung)
- Kết quả điều tra
- Phê duyệt xử lý
- Mới đến bước hạch toán

---

## Output Format

```json
{
  "skill": "accounting-stocktake",
  "version": "1.0.0",
  "stocktake_id": "KK-{YYYYMMDD}-{SEQ}",
  "stocktake_date": "DD/MM/YYYY",
  "location": "",
  "summary": {
    "total_items_counted": 0,
    "items_with_surplus": 0,
    "items_with_shortage": 0,
    "items_match": 0,
    "total_surplus_value": 0,
    "total_shortage_value": 0
  },
  "details": [
    {
      "item_code": "",
      "item_name": "",
      "unit": "",
      "book_quantity": 0,
      "actual_quantity": 0,
      "difference": 0,
      "unit_price": 0,
      "difference_value": 0,
      "difference_type": "surplus|shortage|match",
      "within_allowance": false,
      "investigation_status": "cleared|pending|unexplained",
      "proposed_treatment": "increase_inventory|expense|write_off|employee_liable|vat_adjustment|pending_investigation",
      "legal_reference": ""
    }
  ],
  "journal_entries": [
    {
      "scenario": "surplus_unknown_source",
      "lines": [
        { "account_code": "152", "debit": 0, "credit": 0, "description": "" },
        { "account_code": "711", "debit": 0, "credit": 0, "description": "" }
      ],
      "legal_reference": ""
    },
    {
      "scenario": "shortage_within_allowance",
      "lines": [
        { "account_code": "632", "debit": 0, "credit": 0, "description": "" },
        { "account_code": "152", "debit": 0, "credit": 0, "description": "" }
      ]
    }
  ],
  "vat_adjustment_required": false,
  "vat_adjustment_amount": 0,
  "flags": [],
  "approvals_required": [
    "audit_committee_sign_off",
    "finance_manager_sign_off",
    "ceo_approval_for_write_off"
  ],
  "disclaimer": "Kiểm kê dựa trên dữ liệu user cung cấp. Cần Hội đồng kiểm kê xác nhận trước khi hạch toán."
}
```

---

## Escalation Rules

| Tình huống | Mức độ | Recipient |
|-----------|--------|-----------|
| Chênh lệch giá trị > 100 triệu | HIGH | Giám đốc + HĐQT |
| Chênh lệch > 5% tổng tồn kho | HIGH | Giám đốc + Kiểm toán nội bộ |
| Hàng thiếu không rõ nguyên nhân | HIGH | Giám đốc + Công an (nếu nghi gian lận) |
| Hàng hư hỏng > 50 triệu | MEDIUM | Kế toán trưởng |
| Phát hiện hàng quá hạn > 30 ngày | MEDIUM | Kế toán trưởng |
| NV gây thiệt hại nhiều lần | HIGH | HR + Giám đốc |
| Cần giảm trừ VAT đầu vào | HIGH | Tư vấn thuế |

---

## Legal Disclaimer

Skill này hỗ trợ kiểm kê tồn kho và xử lý chênh lệch. **Không thay thế Hội
đồng kiểm kê** do Giám đốc thành lập. Quyết định xử lý phải được:
- Hội đồng kiểm kê thống nhất
- Ban Giám đốc / HĐQT phê duyệt
- Đối với khoản giảm trừ VAT: có tư vấn thuế xác nhận

Kiểm kê là cơ sở quan trọng cho BCTC cuối năm. Kết quả kiểm kê phải được
lưu trữ theo quy định (5 năm). Trường hợp có dấu hiệu gian lận, cần báo
cơ quan có thẩm quyền.