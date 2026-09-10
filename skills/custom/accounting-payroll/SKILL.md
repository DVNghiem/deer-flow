---
name: accounting-payroll
description: >
  Tính lương, BHXH/BHYT/BHTN và thuế thu nhập cá nhân (TNCN) cho người lao
  động Việt Nam. Trigger khi user cần: tính lương gross → net, tính BHXH
  phía NLĐ và DN, tính thuế TNCN theo biểu lũy tiến 5 bậc, lập bảng lương,
  tạm khấu trừ TNCN hàng tháng, lập cam kết 08/CK-TNCN, quyết toán thuế
  TNCN cuối năm (05/QTT-TNCN).
version: 1.0.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - payroll
  - bhxh
  - bhyt
  - bhtn
  - personal-income-tax
---

# Accounting Payroll Skill

## Purpose

Tính toán lương, các khoản trích theo lương (BHXH/BHYT/BHTN/KPCĐ) và thuế
thu nhập cá nhân (TNCN) cho người lao động tại Việt Nam, bao gồm cả lao
động Việt Nam và lao động nước ngoài làm việc tại Việt Nam.

> ⚠️ **Lưu ý quan trọng**: Các tỷ lệ BHXH, mức giảm trừ gia cảnh, và biểu
> thuế TNCN có thể đã được cập nhật. **Cần xác minh tỷ lệ hiện hành** trên
> Cổng BHXH Việt Nam và Tổng cục Thuế trước khi áp dụng cho kỳ tính.

**Legal Framework:**
- Luật Bảo hiểm xã hội 2014 (có hiệu lực từ 01/01/2016)
- Luật BHXH sửa đổi 2025 (nếu có) — **cần xác minh**
- Luật Thuế TNCN 04/2007/QH13 (sửa đổi bổ sung bởi Luật 71/2014/QH13)
- Nghị định 58/2020/NĐ-CP — Tỷ lệ đóng BHXH/BHYT/BHTN
- Nghị định 126/2020/NĐ-CP — Hướng dẫn Luật Quản lý thuế (TNCN)
- Nghị định 65/2013/NĐ-CP — Hướng dẫn Luật Thuế TNCN
- Thông tư 111/2013/TT-BTC — Hướng dẫn thuế TNCN
- Thông tư 92/2015/TT-BTC — Sửa đổi TT 111/2013

## When to Use

- Tính lương gross → net cho từng NLĐ
- Tính BHXH/BHYT/BHTN phía NLĐ và phía DN
- Tính thuế TNCN theo biểu lũy tiến 5 bậc
- Lập bảng lương hàng tháng
- Tạm khấu trừ TNCN hàng tháng (mẫu 05/KK-TNCN hoặc 02/KK-TNCN)
- Lập cam kết không khấu trừ TNCN (mẫu 08/CK-TNCN) cho NLĐ có thu nhập
  thấp
- Quyết toán thuế TNCN cuối năm (mẫu 05/QTT-TNCN)
- Hạch toán lương vào sổ sách kế toán

## When NOT to Use

- Tính lương gross-up theo cơ chế đặc thù (công ty nước ngoài, FDI) — cần
  xem xét riêng
- BHXH cho người nước ngoài (áp dụng hiệp định song phương — phức tạp)
- Chính sách thưởng, phúc lợi không thuộc hệ thống lương
- Lương hưu, trợ cấp BHXH — sau khi NLĐ nghỉ việc
- Thuế cho lao động tự do, hợp đồng cộng tác viên (có cách tính riêng)
- Tính thuế cho người chuyển nhượng vốn, chứng khoán (TNCN khác loại)

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `payroll_period` | object | Yes | `{ year, month }` kỳ lương |
| `company_info` | object | Yes | Tên DN, MST, địa chỉ, đăng ký BHXH |
| `employees` | array | Yes | Danh sách NLĐ (mã, tên, MST TNCN, phòng ban) |
| `employees[].employee_id` | string | Yes | Mã nhân viên nội bộ |
| `employees[].name` | string | Yes | Họ tên NLĐ |
| `employees[].tax_code` | string | No | MST TNCN (nếu có) |
| `employees[].citizen_id` | string | No | CCCD/CMND |
| `employees[].contract_type` | enum | Yes | `"official"` (≥3 tháng), `"probation"`, `"part_time"` |
| `employees[].gross_salary` | number | Yes | Lương gross tháng |
| `employees[].dependents` | number | No | Số người phụ thuộc đã đăng ký |
| `employees[].tax_commitment` | boolean | No | Đã có cam kết 08/CK-TNCN chưa |
| `employees[].is_resident` | boolean | Yes | Cư trú hay không cư trú (mặc định true) |
| `payroll_components` | object | No | Các khoản phụ cấp, thưởng, làm thêm |

---

## Tỷ lệ BHXH/BHYT/BHTN/KPCĐ (tham khảo NĐ 58/2020)

> ⚠️ **Cần xác minh tỷ lệ hiện hành** tại thời điểm áp dụng. Có thể đã có
> NĐ mới thay thế/sửa đổi NĐ 58/2020.

| Khoản | NLĐ đóng | DN đóng | Tổng | Cơ sở tính |
|-------|----------|---------|------|-----------|
| BHXH (hưu trí, tử tuất) | 8% | 17.5% | 25.5% | Lương đóng BHXH |
| BHYT | 1.5% | 3% | 4.5% | Lương đóng BHXH |
| BHTN | 1% | 1% | 2% | Lương đóng BHXH |
| **Tổng NLĐ đóng** | **10.5%** | - | - | - |
| **Tổng DN đóng** | - | **21.5%** | - | - |
| KPCĐ (Công đoàn) | - | 2% | 2% | Lương đóng BHXH (DN có tổ chức CĐ) |

**Lương đóng BHXH**: Theo NĐ 58/2020, từ 01/07/2020:
- Lương đóng BHXH = Lương tháng đóng BHXH (mức lương trong HĐLĐ)
- Tối thiểu = Lương tối thiểu vùng (theo NĐ 38/2022/NĐ-CP — **cần xác minh**)
- Tối đa = 20 lần lương cơ sở (1,490,000 VND/tháng → 29,800,000 VND/tháng,
  có thể đã thay đổi)

---

## Thuế TNCN — Biểu lũy tiến 5 bậc (tham khảo)

> ⚠️ **Cần xác minh biểu thuế hiện hành** theo Luật Thuế TNCN hiện hành.

| Bậc | Thu nhập tính thuế / tháng | Thuế suất |
|-----|---------------------------|-----------|
| 1 | Đến 5 triệu VND | 5% |
| 2 | 5 - 10 triệu VND | 10% |
| 3 | 10 - 18 triệu VND | 15% |
| 4 | 18 - 32 triệu VND | 20% |
| 5 | Trên 32 triệu VND | 25% |

**Mức giảm trừ gia cảnh (tham khảo)**:
- Bản thân: 11 triệu VND/tháng (có thể đã thay đổi)
- Người phụ thuộc: 4,4 triệu VND/người/tháng (có thể đã thay đổi)

**Công thức tính thuế theo biểu lũy tiến từng phần** (tính nhanh):

```
Thu nhập tính thuế (TNTT) = Tổng TN chịu thuế - Giảm trừ bản thân
                           - Giảm trừ người phụ thuộc - Đóng góp từ thiện
                           - Phần không chịu thuế khác

Thuế TNCN = Σ (TNTT từng bậc × Thuế suất từng bậc)
```

Hoặc dùng **phương pháp tính nhanh** (chỉ áp dụng khi TNTT ≤ ~50 triệu):
```
Thuế TNCN = TNTT × Thuế suất - Số giảm nhanh theo bậc
```

| TNTT | Công thức nhanh |
|------|-----------------|
| ≤ 5 triệu | TNTT × 5% |
| 5 - 10 triệu | TNTT × 10% - 0,25 triệu |
| 10 - 18 triệu | TNTT × 15% - 0,75 triệu |
| 18 - 32 triệu | TNTT × 20% - 1,65 triệu |
| > 32 triệu | TNTT × 25% - 3,25 triệu |

---

## Step-by-Step Workflow

### Bước 1: Xác định loại NLĐ và áp dụng chính sách

```
IF contract_type == "official":
    Đóng BHXH/BHYT/BHTN đầy đủ nếu HĐLĐ ≥ 1 tháng
ELIF contract_type == "probation":
    Một số trường hợp không đóng BHXH (HĐLĐ < 1 tháng)
ELIF contract_type == "part_time":
    Không đóng BHXH/BHTN nếu mức lương < lương tối thiểu vùng
```

### Bước 2: Tính lương đóng BHXH

```
IF gross_salary < luong_toi_thieu_vung:
    luong_dong_bhxh = luong_toi_thieu_vung
ELIF gross_salary > trần_bhxh:
    luong_dong_bhxh = trần_bhxh
ELSE:
    luong_dong_bhxh = gross_salary
```

### Bước 3: Tính BHXH/BHYT/BHTN/KPCĐ phía NLĐ

```
bhxh_nld = luong_dong_bhxh * 8%
bhyt_nld = luong_dong_bhxh * 1.5%
bhtn_nld = luong_dong_bhxh * 1%
tong_bhxh_nld = bhxh_nld + bhyt_nld + bhtn_nld  # 10.5%
```

### Bước 4: Tính BHXH/BHYT/BHTN/KPCĐ phía DN

```
bhxh_dn = luong_dong_bhxh * 17.5%
bhyt_dn = luong_dong_bhxh * 3%
bhtn_dn = luong_dong_bhxh * 1%
kpcd_dn = luong_dong_bhxh * 2%  # nếu DN có CĐ
tong_bhxh_dn = bhxh_dn + bhyt_dn + bhtn_dn + kpcd_dn  # 23.5%
```

### Bước 5: Xác định thu nhập chịu thuế TNCN

```
TN_chiu_thue = gross_salary
              - bhxh_nld  # phần NLĐ đóng được trừ
              - cac_khoan_khong_chiu_thue  # vd: phụ cấp ăn trưa theo quy định
```

### Bước 6: Tính thu nhập tính thuế (TNTT)

```
IF is_resident:
    TNTT = TN_chiu_thue - giam_tru_ban_than - (giam_tru_phu_thuoc * dependents)
ELSE:  # không cư trú
    TNTT = TN_chiu_thue
    thue_TNCN = TNTT * 20%  # thuế suất cố định cho người không cư trú
```

### Bước 7: Tính thuế TNCN theo biểu lũy tiến

Áp dụng cho người cư trú có TNTT > 0.

```
IF tax_commitment == True AND TN_chiu_thue <= muc_chiu_thue_thap:
    thue_TNCN = 0  # đã có cam kết 08/CK-TNCN, không tạm khấu trừ
ELIF TNTT <= 0:
    thue_TNCN = 0
ELSE:
    Tính lũy tiến từng phần theo biểu 5 bậc
```

### Bước 8: Tính lương NET

```
luong_net = gross_salary
          - bhxh_nld - bhyt_nld - bhtn_nld
          - thue_TNCN
          + cac_khoan_cong_them  # thưởng, trợ cấp không chịu thuế
```

### Bước 9: Hạch toán lương

**Bước 1: Tính lương phải trả**
```
Nợ TK 641/642/622/623    Chi phí lương (theo bộ phận)
    Có TK 334              Phải trả NLĐ (gross)
```

**Bước 2: Trích BHXH/BHYT/BHTN phần NLĐ**
```
Nợ TK 334
    Có TK 3383    BHXH phải nộp (phần NLĐ)
    Có TK 3384    BHYT phải nộp (phần NLĐ)
    Có TK 3386    BHTN phải nộp (phần NLĐ)
```

**Bước 3: Trích BHXH/BHYT/BHTN phần DN vào chi phí**
```
Nợ TK 641/642/622/623
    Có TK 3383    BHXH (phần DN)
    Có TK 3384    BHYT (phần DN)
    Có TK 3386    BHTN (phần DN)
```

**Bước 4: Trích thuế TNCN**
```
Nợ TK 334
    Có TK 3335    Thuế TNCN phải nộp
```

**Bước 5: Chi trả lương**
```
Nợ TK 334    Phải trả NLĐ (sau các khoản trừ)
    Có TK 1111/1121    Tiền mặt/Tiền gửi NH
```

---

## Output Format

```json
{
  "skill": "accounting-payroll",
  "version": "1.0.0",
  "period": { "year": 0, "month": 0 },
  "company_info": { "name": "", "tax_code": "" },
  "payroll_summary": {
    "total_employees": 0,
    "total_gross_salary": 0,
    "total_bhxh_employee": 0,
    "total_bhxh_employer": 0,
    "total_kpcd": 0,
    "total_pit": 0,
    "total_net_salary": 0
  },
  "employees": [
    {
      "employee_id": "",
      "name": "",
      "tax_code": "",
      "is_resident": true,
      "dependents": 0,
      "gross_salary": 0,
      "bhxh_base": 0,
      "bhxh_employee": 0,
      "bhyt_employee": 0,
      "bhtn_employee": 0,
      "bhxh_employer": 0,
      "bhyt_employer": 0,
      "bhtn_employer": 0,
      "kpcd": 0,
      "taxable_income": 0,
      "personal_deduction": 0,
      "dependent_deduction": 0,
      "taxable_income_after_deduction": 0,
      "pit_amount": 0,
      "net_salary": 0,
      "has_tax_commitment": false,
      "flags": []
    }
  ],
  "journal_entries": [
    {
      "step": "1_calculate_salary",
      "debit": "641/642/622/623",
      "credit": "334",
      "amount": 0
    },
    {
      "step": "2_withhold_bhxh_employee",
      "debit": "334",
      "credit": "3383/3384/3386",
      "amount_breakdown": {}
    }
  ],
  "pit_return": {
    "monthly_declaration_required": true,
    "commitment_required": [],
    "total_pit_to_declare": 0
  },
  "annual_summary_required": true,
  "disclaimer": "Tính lương dựa trên dữ liệu user cung cấp. Kế toán trưởng xác nhận trước khi chi trả."
}
```

---

## Cam kết 08/CK-TNCN

Điều kiện NLĐ được cam kết không tạm khấu trừ TNCN:
1. Có MST TNCN và cam kết bằng văn bản (mẫu 08/CK-TNCN)
2. Tổng thu nhập từ tiền lương, tiền công trong năm ≤ mức chịu thuế thấp
3. Cam kết chỉ có 1 nguồn thu nhập tại 1 DN

**Lợi ích**: NLĐ không bị tạm khấu trừ tháng, nhưng vẫn phải quyết toán
cuối năm nếu tổng TN > mức giảm trừ.

## Quyết toán thuế TNCN cuối năm (mẫu 05/QTT-TNCN)

Hạn nộp: 90 ngày từ ngày kết thúc năm (thường là 31/03 năm sau).

| Tình huống | Phải quyết toán? |
|-----------|------------------|
| Đã tạm khấu trừ TNCN cả năm | Có (nếu có MST) |
| Có cam kết 08/CK-TNCN | Có, nếu tổng TN > mức giảm trừ |
| NLĐ nghỉ việc giữa năm | Có (theo phần từng DN) |
| NLĐ có nhiều nguồn thu nhập | Có (tổng hợp tất cả) |

---

## Anti-Hallucination Rules

### Rule 1: Không tự áp tỷ lệ BHXH

Tỷ lệ BHXH, mức lương tối thiểu vùng, trần BHXH **có thể đã thay đổi**.
Luôn hỏi user hoặc flag để xác minh. Mặc định dùng tỷ lệ NĐ 58/2020 chỉ
khi user xác nhận.

### Rule 2: Không tự tính người phụ thuộc

Chỉ tính giảm trừ người phụ thuộc khi:
- NLĐ đã đăng ký với cơ quan thuế
- Người phụ thuộc đáp ứng điều kiện (con cái, cha mẹ, vợ/chồng không có
  thu nhập, ...)

Không tự ý giả định NLĐ có người phụ thuộc.

### Rule 3: Không tự quyết định người không cư trú

Tình trạng cư trú được xác định theo quy định (số ngày hiện diện tại VN):
- Cư trú: hiện diện ≥ 183 ngày/năm
- Không cư trú: < 183 ngày/năm

Không tự ý phân loại.

### Rule 4: Không tính thuế TNCN cho thu nhập không chịu thuế

Một số khoản không chịu thuế TNCN (theo TT 111/2013):
- Phụ cấp ăn trưa (một phần), phụ cấp xăng xe (một phần)
- Tiền thưởng sáng kiến, cải tiến kỹ thuật (một phần)
- Trợ cấp khó khăn, trợ cấp thôi việc (theo quy định)
- BHXH một lần nhận từ quỹ BHXH

Phải tham chiếu cụ thể khi áp dụng.

### Rule 5: Cẩn thận với lao động nước ngoài

Lao động nước ngoài làm việc tại VN:
- Thuế suất cố định 20% trên TN chịu thuế (không qua biểu lũy tiến)
- Một số hiệp định song phương có thể miễn/giảm

Cần xác minh hiệp định áp dụng (nếu có).

---

## Escalation Rules

| Tình huống | Mức độ | Recipient |
|-----------|--------|-----------|
| NLĐ nước ngoài có hiệp định tránh đánh thuế 2 lần | HIGH | Tư vấn thuế quốc tế |
| Tranh chấp về tỷ lệ BHXH | HIGH | Cơ quan BHXH |
| NLĐ có thu nhập từ nhiều nguồn | MEDIUM | Kế toán trưởng |
| NLĐ có cam kết sai (đã có >1 nguồn thu nhập) | HIGH | Kế toán trưởng |
| Mức lương đóng BHXH thấp hơn lương thực tế (trốn BHXH) | CRITICAL | Cảnh báo pháp lý |
| Quyết toán TNCN có chênh > 5 triệu/tháng/NLĐ | HIGH | Kế toán trưởng |

---

## Legal Disclaimer

Skill này hỗ trợ tính toán lương và các khoản trích theo lương dự thảo.
**Không thay thế tư vấn thuế hoặc BHXH chuyên nghiệp.** Tỷ lệ BHXH, mức
giảm trừ gia cảnh, biểu thuế TNCN có thể đã thay đổi. Cần xác minh:
- Nghị định 58/2020/NĐ-CP hoặc NĐ mới thay thế
- Luật Thuế TNCN hiện hành và TT 111/2013/TT-BTC (hoặc TT mới)
- Mẫu tờ khai thuế TNCN mới nhất (05/QTT-TNCN, 02/KK-TNCN, 08/CK-TNCN)

Bảng lương chính thức dùng để chi trả phải được HR và kế toán trưởng xác
nhận. Tờ khai thuế TNCN nộp cho cơ quan thuế phải qua hệ thống thuế điện tử.