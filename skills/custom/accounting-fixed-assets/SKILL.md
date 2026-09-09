---
name: accounting-fixed-assets
description: >
  Quản lý và tính khấu hao tài sản cố định (TSCĐ) theo TT 99/2025 (hiệu lực
  01/01/2026), TT 200/2014, TT 133/2016 và TT 45/2013/TT-BTC. Trigger khi user
  cần: tính khấu hao TSCĐ, lập bảng khấu hao, ghi nhận mua/thanh lý/nhượng bán
  TSCĐ, kiểm tra thời gian khấu hao theo khung quy định, phân bổ khấu hao theo
  bộ phận sử dụng, hoặc bất kỳ nghiệp vụ nào liên quan đến fixed assets / TSCĐ
  / khấu hao.
version: 1.1.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
---

# Accounting Fixed Assets Skill

## Purpose

Tính toán, lập lịch và phân bổ khấu hao tài sản cố định theo quy định Việt
Nam. Kiểm tra tính hợp lệ của thời gian và phương pháp khấu hao, tạo bảng
khấu hao và bút toán phân bổ theo kỳ.

**Legal Framework:**
- Thông tư 45/2013/TT-BTC — Quản lý, sử dụng và trích khấu hao TSCĐ
- Thông tư 147/2016/TT-BTC — Sửa đổi TT 45/2013 (thời gian khấu hao)
- Thông tư 200/2014/TT-BTC — Hạch toán TSCĐ (TK 211, 212, 213, 214)
- Thông tư 133/2016/TT-BTC — Hạch toán TSCĐ cho DN vừa và nhỏ
- **Thông tư 99/2025/TT-BTC** — Chế độ kế toán DN (hiệu lực 01/01/2026, thay
  thế TT 200/2014) — xem `references/account-mapping.md` để biết ánh xạ TK
- Nghị định 218/2013/NĐ-CP — Khấu hao tối đa được trừ thuế TNDN

**Account Mapping Across Regimes:** xem
[`references/account-mapping.md`](references/account-mapping.md) để biết ánh xạ
tài khoản TSCĐ giữa TT 99/2025 ↔ TT 200/2014 ↔ TT 133/2016.

## When to Use

- Tính khấu hao tháng/quý/năm cho từng TSCĐ
- Lập bảng khấu hao toàn bộ danh mục TSCĐ
- Ghi nhận mua mới TSCĐ (bút toán vào TK 211/212/213)
- Ghi nhận thanh lý / nhượng bán TSCĐ
- Kiểm tra thời gian khấu hao có nằm trong khung TT 45
- Phân bổ khấu hao theo bộ phận (sản xuất, bán hàng, QLDN)
- Tính giá trị còn lại (Net Book Value) tại thời điểm bất kỳ
- Lập sổ TSCĐ và thẻ TSCĐ

## When NOT to Use

- Đánh giá lại TSCĐ (revaluation) theo IFRS
- Xử lý TSCĐ thuê tài chính phức tạp (IFRS 16)
- Phân tích đầu tư / ROI tài sản
- Quyết định thanh lý / giữ lại TSCĐ

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `regime` | enum | Yes | `"tt200"` hoặc `"tt133"` |
| `action` | enum | Yes | `"compute_depreciation"`, `"register_asset"`, `"dispose_asset"`, `"generate_schedule"` |
| `assets` | array | Yes | Danh sách TSCĐ |
| `assets[].asset_code` | string | Yes | Mã TSCĐ |
| `assets[].asset_name` | string | Yes | Tên TSCĐ |
| `assets[].category` | enum | Yes | Nhóm TSCĐ (xem Asset Categories) |
| `assets[].original_cost` | number | Yes | Nguyên giá (VND) |
| `assets[].purchase_date` | string | Yes | Ngày mua / đưa vào sử dụng (DD/MM/YYYY) |
| `assets[].useful_life_years` | number | Yes | Thời gian sử dụng dự kiến (năm) |
| `assets[].depreciation_method` | enum | Yes | `"straight_line"`, `"declining_balance"`, `"units_of_production"` |
| `assets[].cost_center` | string | No | Bộ phận sử dụng (để phân bổ chi phí) |
| `assets[].residual_value` | number | No | Giá trị thanh lý ước tính (mặc định 0) |
| `computation_period` | object | Yes | `{ year, month }` kỳ tính khấu hao |

## Asset Categories & Useful Life Range (TT 45/2013, TT 147/2016)

| Nhóm | Loại TSCĐ | Thời gian tối thiểu | Thời gian tối đa |
|------|-----------|--------------------|--------------------|
| 1 | Nhà cửa, vật kiến trúc | 6 năm | 50 năm |
| 2 | Máy móc, thiết bị | 3 năm | 30 năm |
| 3 | Phương tiện vận tải | 6 năm | 30 năm |
| 4 | Thiết bị quản lý | 3 năm | 15 năm |
| 5 | TSCĐ là súc vật, vườn cây | 4 năm | 40 năm |
| 6 | TSCĐ vô hình (phần mềm, bằng sáng chế...) | 2 năm | 20 năm |

**CRITICAL:** Thời gian khấu hao `useful_life_years` PHẢI nằm trong khung trên.
Nếu vượt khung → FLAG và yêu cầu xác nhận.

## Depreciation Methods

### 1. Straight-Line (Đường thẳng) — Phổ biến nhất

```
monthly_depreciation = (original_cost - residual_value) / (useful_life_years * 12)
annual_depreciation_rate = 1 / useful_life_years * 100  (%)
```

**Điều kiện:** TSCĐ sử dụng ổn định.
**Legal:** Điều 13, TT 45/2013/TT-BTC

### 2. Declining Balance (Số dư giảm dần)

```
annual_rate = straight_line_rate * acceleration_factor
  acceleration_factor: 1.5 (nếu useful_life 3-4 năm)
                       2.0 (nếu useful_life 5-6 năm)
                       2.5 (nếu useful_life > 6 năm)

annual_depreciation = net_book_value * annual_rate
monthly_depreciation = annual_depreciation / 12

Khi annual_depreciation < straight_line_depreciation:
  → Chuyển sang phương pháp đường thẳng cho phần còn lại
```

**Điều kiện:** TSCĐ chịu hao mòn nhanh do tiến bộ kỹ thuật.
**Legal:** Điều 14, TT 45/2013/TT-BTC

### 3. Units of Production (Sản lượng)

```
depreciation_per_unit = (original_cost - residual_value) / total_estimated_units
period_depreciation = depreciation_per_unit * actual_units_produced
```

**Điều kiện:** TSCĐ mà mức độ hao mòn phụ thuộc số lượng sản phẩm.
**Legal:** Điều 15, TT 45/2013/TT-BTC

---

## Step-by-Step Workflow

### Action: `register_asset` — Ghi nhận TSCĐ mới

**Step 1:** Validate nguyên giá
```
IF original_cost < 30,000,000 VND (TT200) hoặc < 10,000,000 VND (TT133):
    FLAG: "Giá trị dưới ngưỡng ghi nhận TSCĐ. Xem xét hạch toán vào CCDC
           hoặc chi phí ngay."
```

**Step 2:** Validate useful_life nằm trong khung TT 45

**Step 3:** Tạo thẻ TSCĐ và bút toán ghi nhận:
```
Nợ TK 211/212/213    Nguyên giá TSCĐ (chưa VAT)
Nợ TK 133            VAT đầu vào (nếu có)
    Có TK 331/112    Phải trả / Tiền thanh toán
```

**Step 4:** Output thẻ TSCĐ + bảng khấu hao dự kiến toàn bộ vòng đời.

---

### Action: `compute_depreciation` — Tính khấu hao kỳ

**Step 1:** Với mỗi TSCĐ, xác định:
- Nguyên giá
- Giá trị đã khấu hao lũy kế
- Giá trị còn lại (NBV)
- Số tháng đã khấu hao
- Số tháng còn lại

**Step 2:** Tính khấu hao kỳ này theo method.

**Step 3:** Kiểm tra không vượt nguyên giá:
```
IF (accumulated_depreciation + period_depreciation) > original_cost:
    period_depreciation = original_cost - accumulated_depreciation
    FLAG: "TSCĐ {asset_code} đã khấu hao hết. Kiểm tra thanh lý hoặc
           tiếp tục sử dụng."
```

**Step 4:** Tạo bút toán khấu hao:
```
Nợ TK 641/642/627  Chi phí khấu hao (theo bộ phận)
    Có TK 214       Hao mòn lũy kế TSCĐ

Legal: Điều 35, TT 200/2014/TT-BTC
```

---

### Action: `dispose_asset` — Thanh lý / Nhượng bán TSCĐ

**Step 1:** Tính giá trị còn lại tại thời điểm thanh lý:
```
nbv = original_cost - accumulated_depreciation
```

**Step 2:** Bút toán xóa sổ TSCĐ:
```
Nợ TK 214    Hao mòn lũy kế (toàn bộ)
Nợ TK 811    Chi phí khác (giá trị còn lại nếu có)
    Có TK 211/212/213   Nguyên giá

Nếu có thu hồi từ thanh lý:
Nợ TK 111/112    Tiền thu hồi
    Có TK 711     Thu nhập khác
    Có TK 3331    VAT (nếu có)
```

**Step 3:** Tính lãi/lỗ thanh lý:
```
gain_loss = proceeds - nbv
IF gain_loss > 0: Lãi thanh lý → TK 711
IF gain_loss < 0: Lỗ thanh lý → TK 811
```

---

### Action: `generate_schedule` — Lập bảng khấu hao

Output bảng khấu hao đầy đủ theo từng kỳ (tháng/năm) cho toàn bộ vòng đời TSCĐ.

---

## Anti-Hallucination Rules

### Rule 1: Không tự chọn useful_life

Không được tự ý gán thời gian khấu hao. Nếu user không cung cấp, yêu cầu
nhập hoặc đề xuất khung từ TT 45 và để user quyết định.

### Rule 2: Không override ngưỡng TSCĐ

Ngưỡng 30M VND (TT200) là quy định, không phải gợi ý.
**SAI:** "Bạn có thể linh hoạt hạch toán tài sản 25M VND vào TSCĐ."
**ĐÚNG:** "Theo TT 200/2014, tài sản 25M VND dưới ngưỡng 30M VND. Cần xác
nhận chính sách nội bộ và có văn bản phê duyệt nếu muốn ghi nhận TSCĐ."

### Rule 3: Luôn kiểm tra khung useful_life

Flag ngay nếu useful_life nằm ngoài khung TT 45/2013.

### Rule 4: Không làm tròn tùy tiện

Khấu hao tháng làm tròn đến đồng VND, sử dụng ROUND_HALF_UP. Ghi rõ phương
pháp làm tròn trong output.

---

## Output Format

```json
{
  "skill": "accounting-fixed-assets",
  "version": "1.0.0",
  "regime": "tt200|tt133",
  "action": "string",
  "computation_period": { "year": 0, "month": 0 },
  "assets": [
    {
      "asset_code": "string",
      "asset_name": "string",
      "original_cost": 0,
      "purchase_date": "DD/MM/YYYY",
      "useful_life_years": 0,
      "useful_life_within_range": true,
      "depreciation_method": "straight_line",
      "accumulated_depreciation_start": 0,
      "period_depreciation": 0,
      "accumulated_depreciation_end": 0,
      "net_book_value": 0,
      "remaining_months": 0,
      "fully_depreciated": false,
      "cost_center": "string",
      "journal_entry": {
        "debit_account": "641|642|627",
        "credit_account": "214",
        "amount": 0,
        "legal_reference": "Điều 35, TT 200/2014/TT-BTC"
      },
      "flags": []
    }
  ],
  "period_summary": {
    "total_assets": 0,
    "total_period_depreciation": 0,
    "breakdown_by_cost_center": {},
    "fully_depreciated_assets": [],
    "flagged_assets": []
  },
  "depreciation_schedule": [],
  "escalations": [],
  "disclaimer": "Khấu hao được tính theo thông số user cung cấp. Kế toán trưởng xác nhận trước khi ghi sổ."
}
```

---

## Legal Disclaimer

Skill này tính khấu hao dựa trên dữ liệu đầu vào. Không thay thế phán quyết
chuyên môn của kiểm toán viên hoặc cơ quan thuế. Thời gian và phương pháp
khấu hao cần được Hội đồng quản trị / Giám đốc phê duyệt bằng văn bản. Cơ
quan thuế có quyền điều chỉnh nếu phương pháp khấu hao không phù hợp quy định.
