---
name: accounting-closing-period
description: >
  Bút toán kết chuyển cuối kỳ (tháng/quý/năm) theo TT 99/2025/TT-BTC và TT
  200/2014/TT-BTC. Trigger khi user cần: khấu hao cuối kỳ, phân bổ chi phí
  trả trước, phân bổ CCDC, kết chuyển doanh thu và chi phí về TK 911, tạm
  tính thuế TNDN, kết chuyển lãi/lỗ về 421, hoặc các nghiệp vụ điều chỉnh
  cuối kỳ.
version: 1.0.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - closing-entries
  - period-end
  - year-end
---

# Accounting Closing Period Skill

## Purpose

Tự động hóa quy trình kết chuyển cuối kỳ (tháng/quý/năm) cho doanh nghiệp
Việt Nam. Bao gồm các bút toán phân bổ, kết chuyển doanh thu/chi phí, tạm
tính thuế TNDN, và kết chuyển lãi/lỗ về lợi nhuận chưa phân phối.

**Legal Framework:**
- Thông tư 99/2025/TT-BTC — Chế độ kế toán DN (hiệu lực 01/01/2026)
- Thông tư 200/2014/TT-BTC — Chế độ kế toán DN
- Thông tư 133/2016/TT-BTC — Chế độ kế toán DN vừa và nhỏ
- Luật Kế toán 88/2015/QH13 — Quy định về kỳ kế toán, báo cáo tài chính

## When to Use

- Cuối tháng: tính khấu hao, phân bổ CP trả trước, kết chuyển DT-CP (nếu
  dùng phương pháp kê khai định kỳ — TT 200)
- Cuối quý: tạm tính thuế TNDN quý, nộp tờ khai quý
- Cuối năm:
  - Khoá sổ kế toán
  - Kết chuyển toàn bộ DT-CP về 911
  - Xác định KQKD
  - Tạm tính thuế TNDN cả năm
  - Kết chuyển lãi/lỗ về 421
  - Lập BCTC (dùng `accounting-financial-reports`)

## When NOT to Use

- Kết chuyển hàng ngày (không phải cuối kỳ)
- Đối chiếu sổ sách (dùng `accounting-reconciliation`)
- Lập BCTC (dùng `accounting-financial-reports`)
- Quyết toán thuế (dùng `accounting-tax-vat` hoặc
  `accounting-corporate-income-tax`)
- Phân bổ giá thành sản phẩm (cần skill riêng cho cost accounting)

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `regime` | enum | Yes | `"tt99"`, `"tt200"`, hoặc `"tt133"` |
| `period_type` | enum | Yes | `"month"`, `"quarter"`, hoặc `"year"` |
| `period` | object | Yes | `{ year, month, quarter }` |
| `company_info` | object | Yes | Tên DN, MST, kỳ kế toán |
| `account_balances` | object | Yes | Số dư và phát sinh TK đến cuối kỳ |
| `prepaid_expenses` | array | No | Danh sách TK 242 / 142 cần phân bổ |
| `tools_assets` | array | No | Danh sách TK 153 / CCDC cần phân bổ |
| `fixed_assets` | array | No | Danh sách TSCĐ cần tính khấu hao (hoặc dùng `accounting-fixed-assets`) |
| `tax_info` | object | No | Thông tin tạm tính thuế TNDN |

---

## Quy trình kết chuyển cuối kỳ

### Bước 1: Trước khi kết chuyển

**Checklist trước khi đóng kỳ**:
- [ ] Tất cả bút toán trong kỳ đã được ghi sổ
- [ ] Sổ cái đã đối chiếu với sổ phụ (TK chi tiết)
- [ ] Số dư các TK phải thu, phải trả đã đối chiếu với khách hàng
- [ ] Tồn kho đã kiểm kê (cuối năm)
- [ ] Khoản mục tiền tệ đã đối chiếu với ngân hàng
- [ ] Các nghiệp vụ cuối kỳ đã ghi nhận

### Bước 2: Các bút toán phân bổ cuối kỳ

#### 2.1. Tính khấu hao TSCĐ

> ⚠️ Dùng skill `accounting-fixed-assets` để có workflow chi tiết.

```
Nợ TK 641/642/627    Chi phí khấu hao (theo bộ phận)
    Có TK 2141        Hao mòn TSCĐ hữu hình
    Có TK 2143        Hao mòn TSCĐ vô hình (nếu có)
```

#### 2.2. Phân bổ chi phí trả trước (TK 242)

> Một số DN phân bổ theo tháng, một số theo quý. Tùy chính sách kế toán.

Phương pháp: thời gian (số tháng) hoặc công suất.

```
Nợ TK 641/642/627    Chi phí SXKD (theo bộ phận)
    Có TK 242         Chi phí trả trước (phân bổ trong kỳ)
```

#### 2.3. Phân bổ Công cụ dụng cụ (TK 153)

```
Nợ TK 641/642/627    Chi phí (theo bộ phận)
    Có TK 153         Công cụ dụng cụ (phân bổ trong kỳ)
```

#### 2.4. Trích trước chi phí (nếu có)

Một số DN trích trước chi phí chưa có hóa đơn (theo TT 200/TT 99):
- Chi phí sửa chữa lớn TSCĐ
- Chi phí bảo hành sản phẩm
- Chi phí quảng cáo, khuyến mại cuối năm

```
Nợ TK 641/642    Chi phí SXKD
    Có TK 352     Trích trước chi phí phải trả (hoặc TK tương đương)
```

### Bước 3: Kết chuyển doanh thu (cuối kỳ)

```
Nợ TK 511    Doanh thu bán hàng
Nợ TK 515    Doanh thu hoạt động tài chính
Nợ TK 711    Thu nhập khác
    Có TK 911    Xác định kết quả kinh doanh
```

> Áp dụng cho **TT 200 và TT 99**. TT 133 có thể gộp một số TK.

### Bước 4: Kết chuyển chi phí (cuối kỳ)

```
Nợ TK 911    Xác định kết quả kinh doanh
    Có TK 632    Giá vốn hàng bán
    Có TK 641    Chi phí bán hàng (TT 200/TT 99)
    Có TK 642    Chi phí QLDN (TT 200/TT 99) hoặc CP BH+QL (TT 133)
    Có TK 635    Chi phí tài chính
    Có TK 811    Chi phí khác
```

### Bước 5: Xác định kết quả kinh doanh

```
LN_khac = Tổng Có 911 (DT + TN khác) - Tổng Nợ 911 (CP + CP khác)

Nếu LN_khac > 0: Lãi
Nếu LN_khac < 0: Lỗ
```

### Bước 6: Tạm tính thuế TNDN

> ⚠️ Dùng skill `accounting-corporate-income-tax` để tính chính xác.

```
Nợ TK 8211    Chi phí thuế TNDN hiện hành
    Có TK 3334    Thuế TNDN phải nộp
```

Nếu muốn kết chuyển thuế TNDN vào 911 (một số DN làm):
```
Nợ TK 911
    Có TK 8211
```

### Bước 7: Kết chuyển lãi/lỗ về LNST chưa phân phối (cuối năm)

**Nếu LÃI**:
```
Nợ TK 911    Xác định KQKD (số dư Có)
    Có TK 4211    LNST chưa phân phối (lãi năm trước)
    Có TK 4212    LNST chưa phân phối (lãi năm nay)
```

**Nếu LỖ**:
```
Nợ TK 4211/4212    LNST chưa phân phối
    Có TK 911        Xác định KQKD (số dư Nợ)
```

### Bước 8: Đóng sổ cuối năm

- Khóa sổ cái, sổ phụ
- Lưu trữ sổ theo quy định (5 năm)
- Lập BCTC (gọi skill `accounting-financial-reports`)

---

## Step-by-Step Workflow chi tiết

### Workflow cuối THÁNG (TT 200/TT 99)

```
1. Tính khấu hao TSCĐ (gọi accounting-fixed-assets)
2. Phân bổ chi phí trả trước (242)
3. Phân bổ CCDC (153)
4. (Tùy DN) Kết chuyển DT-CP nếu dùng phương pháp kiểm kê định kỳ
5. (Tùy DN) Tính giá thành (nếu SX)
```

### Workflow cuối QUÝ

```
1. Toàn bộ workflow cuối tháng (chỉ tháng cuối quý)
2. Tạm tính thuế TNDN quý (gọi accounting-corporate-income-tax)
3. Lập tờ khai thuế TNDN tạm tính quý (mẫu 01/TNDN)
4. Nộp thuế (nếu có phát sinh)
```

### Workflow cuối NĂM

```
1. Toàn bộ workflow cuối tháng + quý (tháng 12)
2. Đối chiếu toàn bộ sổ sách (gọi accounting-reconciliation)
3. Kiểm kê tồn kho, tài sản (gọi accounting-stocktake)
4. Trích trước chi phí (nếu có)
5. Kết chuyển doanh thu về 911
6. Kết chuyển chi phí về 911
7. Tạm tính thuế TNDN cả năm (gọi accounting-corporate-income-tax)
8. Kết chuyển lãi/lỗ về 421
9. Phân phối lợi nhuận (nếu có quyết định):
   - Trích quỹ ĐTPT
   - Trích quỹ DPTC
   - Trích quỹ khen thưởng phúc lợi
   - Chia cổ tức
10. Đóng sổ, lập BCTC
11. Nộp BCTC cho cơ quan thuế
12. Quyết toán thuế TNDN (gọi accounting-corporate-income-tax)
```

---

## Anti-Hallucination Rules

### Rule 1: Không tự ý trích trước chi phí

Trích trước chỉ áp dụng cho **chi phí thực tế phát sinh nhưng chưa có hóa
đơn** (vd: tiền điện cuối tháng). Không được trích trước cho chi phí chưa
phát sinh.

### Rule 2: Không tự phân bổ chi phí trả trước nếu không có dữ liệu

Cần biết:
- Tổng giá trị CP trả trước ban đầu
- Thời gian phân bổ (số kỳ)
- Giá trị đã phân bổ đến đầu kỳ này
- Phương pháp phân bổ (thời gian / sản lượng)

Nếu thiếu → flag, yêu cầu user cung cấp.

### Rule 3: Không tự tính thuế TNDN

Dùng skill `accounting-corporate-income-tax` để có kết quả chính xác. Skill
này chỉ tạo bút toán tạm tính.

### Rule 4: Trình tự kết chuyển cố định

Thứ tự kết chuyển phải đúng:
1. Phân bổ CP (KH, CP trả trước, CCDC)
2. Kết chuyển DT về 911
3. Kết chuyển CP về 911
4. Xác định KQKD
5. Tạm tính thuế TNDN
6. Kết chuyển lãi/lỗ về 421

Không tự ý thay đổi thứ tự.

### Rule 5: Không tự đóng sổ nếu còn chênh lệch

Nếu tổng Nợ ≠ Tổng Có, hoặc còn bút toán chưa ghi, KHÔNG đóng sổ. Flag
lỗi.

---

## Output Format

```json
{
  "skill": "accounting-closing-period",
  "version": "1.0.0",
  "regime": "tt99|tt200|tt133",
  "period": { "year": 0, "month": 0, "quarter": "Q1|Q2|Q3|Q4|year" },
  "company_info": { "name": "", "tax_code": "" },
  "pre_closing_checklist": {
    "all_entries_posted": true,
    "subledgers_reconciled": true,
    "bank_reconciled": true,
    "inventory_counted": true,
    "outstanding_items": []
  },
  "closing_entries": [
    {
      "step": 1,
      "description": "Trích khấu hao TSCĐ",
      "entry_type": "allocation",
      "lines": [
        { "account_code": "627", "debit": 0, "credit": 0, "description": "" },
        { "account_code": "2141", "debit": 0, "credit": 0, "description": "" }
      ],
      "total_debit": 0,
      "total_credit": 0,
      "legal_reference": "..."
    },
    {
      "step": 2,
      "description": "Phân bổ chi phí trả trước",
      "entry_type": "allocation",
      "lines": [],
      "total_debit": 0,
      "total_credit": 0
    },
    {
      "step": 3,
      "description": "Kết chuyển doanh thu về 911",
      "entry_type": "closing_revenue",
      "lines": []
    },
    {
      "step": 4,
      "description": "Kết chuyển chi phí về 911",
      "entry_type": "closing_expense",
      "lines": []
    },
    {
      "step": 5,
      "description": "Tạm tính thuế TNDN",
      "entry_type": "tax_provision",
      "lines": []
    },
    {
      "step": 6,
      "description": "Kết chuyển lãi/lỗ về 421",
      "entry_type": "profit_transfer",
      "lines": [],
      "net_result": 0,
      "result_type": "profit|loss"
    }
  ],
  "summary": {
    "total_revenue": 0,
    "total_expense": 0,
    "profit_before_tax": 0,
    "tax_provision": 0,
    "net_profit": 0
  },
  "validation": {
    "balanced_entries": true,
    "all_revenue_closed": true,
    "all_expense_closed": true,
    "discrepancies": []
  },
  "flags": [],
  "disclaimer": "Bút toán kết chuyển cuối kỳ dựa trên dữ liệu user cung cấp. Kế toán trưởng xác nhận trước khi đóng sổ."
}
```

---

## Escalation Rules

| Tình huống | Mức độ | Recipient |
|-----------|--------|-----------|
| Tổng Nợ ≠ Tổng Có (sai cân đối) | CRITICAL | Kế toán trưởng |
| Còn bút toán chưa ghi | HIGH | Kế toán viên |
| Tồn kho chênh lệch > 5% | HIGH | Kế toán trưởng |
| Lỗ chuyển sang kỳ sau vượt 5 năm | MEDIUM | Kế toán trưởng |
| Khoản chi không có hóa đơn > 100 triệu | HIGH | Kế toán trưởng |
| Tạm tính TNDN có biến động > 20% so với năm trước | MEDIUM | Kế toán trưởng |

---

## Legal Disclaimer

Skill này tạo bút toán kết chuyển cuối kỳ dự thảo. **Kế toán trưởng phải
xác nhận trước khi đóng sổ.** Việc đóng sổ là thao tác quan trọng, không
thể hoàn tác; phải đảm bảo:
- Đã đối chiếu toàn bộ sổ sách
- Đã kiểm kê tài sản, tồn kho
- Đã lập đầy đủ chứng từ
- Đã tính toán đúng các khoản trích theo lương, BHXH, TNDN

Các con số và quy định có thể đã thay đổi. Luôn xác minh với văn bản hiện
hành trước khi áp dụng.