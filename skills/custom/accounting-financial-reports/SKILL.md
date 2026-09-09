---
name: accounting-financial-reports
description: >
  Lập báo cáo tài chính (BCTC) Việt Nam theo TT 99/2025/TT-BTC (hiệu lực
  01/01/2026) và TT 200/2014/TT-BTC. Trigger khi user cần: lập Bảng cân đối
  kế toán (B01), Báo cáo KQKD (B02), Báo cáo LCTT (B03), Thuyết minh BCTC
  (B04/B09), Báo cáo biến động vốn chủ sở hữu (B05); hoặc mapping số liệu
  từ bút toán sang mẫu biểu BCTC.
version: 1.0.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - financial-statements
  - balance-sheet
  - income-statement
  - cash-flow
---

# Accounting Financial Reports Skill

## Purpose

Lập các báo cáo tài chính (BCTC) doanh nghiệp theo chế độ kế toán Việt Nam.
Mapping số liệu từ hệ thống bút toán sang các mẫu biểu theo quy định.

**Legal Framework:**
- **Thông tư 99/2025/TT-BTC** — Chế độ kế toán DN (hiệu lực 01/01/2026)
  — áp dụng cho BCTC kỳ kế toán từ 01/01/2026
- Thông tư 200/2014/TT-BTC — Chế độ kế toán DN (áp dụng cho BCTC kỳ kế
  toán trước 01/01/2026)
- Thông tư 133/2016/TT-BTC — Mẫu BCTC rút gọn cho DN vừa và nhỏ
- Luật Kế toán 88/2015/QH13 — Quy định chung về BCTC

## When to Use

- Lập Bảng cân đối kế toán (Mẫu B01-DN)
- Lập Báo cáo kết quả hoạt động kinh doanh (Mẫu B02-DN)
- Lập Báo cáo lưu chuyển tiền tệ (Mẫu B03-DN) — trực tiếp hoặc gián tiếp
- Lập Thuyết minh BCTC (Mẫu B04-DN / B09-DN)
- Lập Báo cáo tình hình biến động vốn chủ sở hữu (Mẫu B05-DN)
- Kiểm tra tính cân đối giữa các báo cáo (inter-report validation)
- Mapping số dư TK kế toán → chỉ tiêu BCTC
- So sánh số liệu qua các kỳ (BCTC so sánh)

## When NOT to Use

- Lập báo cáo thuế (tờ khai thuế GTGT, thuế TNDN) — dùng
  `accounting-tax-vat` và `accounting-corporate-income-tax`
- Phân tích tài chính (chỉ số ROE, ROA, thanh khoản) — skill chuyên biệt
- Báo cáo quản trị (nội bộ) — không phải BCTC theo quy định
- BCTC hợp nhất (consolidated FS) — cần logic riêng (loại trừ giao dịch nội bộ)
- BCTC quyết toán vốn đầu tư XDCB — mẫu riêng theo TT riêng
- Báo cáo kiểm toán — do kiểm toán viên lập, không phải kế toán

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `regime` | enum | Yes | `"tt99"`, `"tt200"`, hoặc `"tt133"` |
| `report_type` | enum | Yes | `"B01"` (Bảng CĐKT), `"B02"` (KQKD), `"B03"` (LCTT), `"B04"` / `"B09"` (Thuyết minh), `"B05"` (biến động VCSH), `"all"` |
| `accounting_period` | object | Yes | `{ start_date, end_date, prior_period }` DD/MM/YYYY |
| `trial_balance` | array | Yes | Danh sách TK + số dư đầu kỳ, cuối kỳ, phát sinh Nợ/Có |
| `company_info` | object | Yes | Tên DN, mã số thuế, địa chỉ, ngành nghề, người đại diện |
| `output_format` | enum | No | `"json"` (mặc định), `"html"`, `"excel"` |

---

## Hệ thống mẫu biểu BCTC

| Mã mẫu | Tên | Áp dụng |
|--------|-----|---------|
| B01-DN | Bảng cân đối kế toán | TT 200, TT 99 |
| B01-DN (rút gọn) | Bảng CĐKT rút gọn | TT 133 |
| B02-DN | Báo cáo KQKD (dạng đầy đủ) | TT 200, TT 99 |
| B02-DN (rút gọn) | Báo cáo KQKD rút gọn | TT 133 |
| B03-DN | Báo cáo LCTT (phương pháp trực tiếp/gián tiếp) | TT 200, TT 99 |
| B03-DN (rút gọn) | Báo cáo LCTT rút gọn | TT 133 |
| B04-DN / B09-DN | Thuyết minh BCTC | TT 200, TT 99 |
| B05-DN | Báo cáo biến động vốn chủ sở hữu | TT 200, TT 99 |

> **Lưu ý**: Mẫu biểu BCTC theo TT 99/2025 có thể đã được cập nhật. **Cần xác
> minh mẫu biểu hiện hành** trên Cổng thông tin Bộ Tài chính trước khi nộp
> BCTC chính thức.

---

## Step-by-Step Workflow

### Bước 1: Xác định chế độ kế toán & mẫu biểu

```
IF regime == "tt99" hoặc "tt200":
    Sử dụng bộ mẫu biểu đầy đủ (B01-DN, B02-DN, B03-DN, B04-DN/B09-DN, B05-DN)
ELIF regime == "tt133":
    Sử dụng bộ mẫu biểu rút gọn theo TT 133/2016
```

### Bước 2: Mapping số dư TK → chỉ tiêu BCTC

Mỗi chỉ tiêu BCTC tương ứng với một hoặc nhiều TK. Mapping chính:

#### Bảng CĐKT (B01-DN) — mapping chính

| Chỉ tiêu | Mã chỉ tiêu | Nguồn |
|----------|-------------|-------|
| Tiền và tương đương tiền | 110 | TK 111, 1121, 1122, 113 (một phần) |
| Đầu tư tài chính ngắn hạn | 120 | TK 121, 1281, 1282 |
| Phải thu ngắn hạn khách hàng | 131 | TK 131 |
| Trả trước cho người bán ngắn hạn | 132 | TK 132 |
| Phải thu ngắn hạn khác | 136 | TK 138, 136, 141 (nếu <12 tháng) |
| Hàng tồn kho | 140 | TK 152, 153, 154, 155, 156, 157 |
| Tài sản ngắn hạn khác | 150 | TK 242 (một phần) |
| **TỔNG TÀI SẢN NGẮN HẠN** | **200** | Tổng 110+120+130+150 |
| Phải thu dài hạn khách hàng | 211 | TK 131 (một phần dài hạn) |
| Trả trước dài hạn | 212 | TK 242 |
| TSCĐ hữu hình | 221 | TK 211 - 2141 |
| TSCĐ vô hình | 227 | TK 213 - 2143 |
| Bất động sản đầu tư | 230 | TK 217 |
| Đầu tư tài chính dài hạn | 250 | TK 221, 222, 228 |
| **TỔNG TÀI SẢN DÀI HẠN** | **260** | Tổng 210+220+230+250+260 |
| **TỔNG TÀI SẢN** | **270** | 200 + 260 |
| Phải trả người bán ngắn hạn | 311 | TK 331 (phần ngắn hạn) |
| Người mua trả tiền trước | 312 | TK 131 (ghi Có) |
| Thuế phải nộp | 313 | TK 333 |
| Phải trả NLĐ | 314 | TK 334 |
| Phải trả ngắn hạn khác | 319 | TK 335, 336, 338 |
| Vay ngắn hạn | 320 | TK 341, 34311 (nếu <12 tháng) |
| **TỔNG NỢ NGẮN HẠN** | **310** | Tổng 311+312+313+... |
| Phải trả dài hạn | 331 | TK 331, 334, 338 (phần dài hạn) |
| Vay dài hạn | 341 | TK 341, 34312 (phần dài hạn) |
| **TỔNG NỢ DÀI HẠN** | **330** | Tổng 331+...+340 |
| **TỔNG NỢ PHẢI TRẢ** | **300** | 310 + 330 |
| Vốn góp của chủ sở hữu | 411 | TK 4111, 4112 |
| Thặng dư vốn cổ phần | 412 | TK 412 |
| LNST chưa phân phối | 421 | TK 4211, 4212 |
| Quỹ dự trữ | 414 | TK 414 |
| **TỔNG VỐN CHỦ SỞ HỮU** | **440** | 411+412+413+414+421 |
| **TỔNG NGUỒN VỐN** | **440** | 300 + 440 |

#### Báo cáo KQKD (B02-DN) — mapping chính

| Chỉ tiêu | Mã | Nguồn |
|----------|-----|-------|
| Doanh thu bán hàng | 01 | TK 5111, 5112, 5113 |
| Các khoản giảm trừ DT | 02 | TK 521 |
| **Doanh thu thuần** | **10** | 01 - 02 |
| Giá vốn hàng bán | 11 | TK 632 |
| **Lợi nhuận gộp** | **20** | 10 - 11 |
| DT hoạt động tài chính | 21 | TK 515 |
| CP tài chính | 22 | TK 635 |
| CP bán hàng | 25 | TK 641 |
| CP QLDN | 26 | TK 642 |
| **LN thuần từ HĐKD** | **30** | 20 + 21 - 22 - 25 - 26 |
| Thu nhập khác | 31 | TK 711 |
| CP khác | 32 | TK 811 |
| **LN khác** | **40** | 31 - 32 |
| Tổng LN trước thuế | 50 | 30 + 40 |
| CP thuế TNDN hiện hành | 51 | TK 8211 |
| CP thuế TNDN hoãn lại | 52 | TK 8212 |
| **LN sau thuế** | **60** | 50 - 51 - 52 |

### Bước 3: Validate tính cân đối

```
# Bảng CĐKT phải cân đối
TỔNG TÀI SẢN (270) == TỔNG NGUỒN VỐN (440)
```

### Bước 4: So sánh với kỳ trước

Nếu cung cấp `prior_period`, hiển thị cả số liệu kỳ trước và biến động
(thay đổi tuyệt đối, %).

### Bước 5: Sinh Thuyết minh (B04/B09)

Thuyết minh BCTC bao gồm các thông tin bắt buộc:
- Đặc điểm hoạt động của DN
- Kỳ kế toán, đơn vị tiền tệ
- Chuẩn mực kế toán và chế độ kế toán áp dụng
- Các chính sách kế toán quan trọng
- Chi tiết các chỉ tiêu trên B01, B02, B03
- Thông tin bổ sung khác (nếu có)

---

## Anti-Hallucination Rules

### Rule 1: Không tự ý điều chỉnh số liệu

Số liệu trên BCTC phải khớp 100% với số dư TK trên sổ cái. Nếu có chênh
lệch → flag, KHÔNG tự điều chỉnh để khớp.

### Rule 2: Không tự ý phân loại ngắn hạn/dài hạn

Phân loại dựa trên quy định (kỳ hạn < 12 tháng = ngắn hạn). Nếu không rõ →
yêu cầu user xác nhận.

### Rule 3: Không tự ý thêm/bớt chỉ tiêu

Mẫu biểu BCTC có danh sách chỉ tiêu cố định. Không tự thêm chỉ tiêu ngoài
mẫu, không tự bớt chỉ tiêu có trong mẫu (có thể để trống = 0).

### Rule 4: Luôn kiểm tra cân đối kế toán

TỔNG TÀI SẢN = TỔNG NGUỒN VỐN. Nếu không cân → KHÔNG xuất BCTC, flag lỗi.

### Rule 5: Trích dẫn đúng văn bản

Khi nói "theo TT 99/2025" phải chắc chắn đang tham chiếu đúng văn bản. Nếu
không chắc → dùng "theo quy định hiện hành" và để kế toán trưởng xác nhận.

---

## Output Format

### Bảng CĐKT (B01)

```json
{
  "skill": "accounting-financial-reports",
  "report_type": "B01",
  "version": "1.0.0",
  "company_info": { "name": "", "tax_code": "" },
  "period": { "as_of_date": "DD/MM/YYYY", "prior_period_as_of": "DD/MM/YYYY" },
  "regime": "tt99",
  "report_template": "B01-DN",
  "balance_sheet": {
    "TAI_SAN": {
      "A_TAI_SAN_NGAN_HAN": {
        "Tien_va_tuong_duong_tien": 0,
        "Dau_tu_tai_chinh_ngan_han": 0,
        "Phai_thu_ngan_han_khach_hang": 0,
        "Tra_truoc_nguoi_ban_ngan_han": 0,
        "Phai_thu_ngan_han_khac": 0,
        "Hang_ton_kho": 0,
        "Tai_san_ngan_han_khac": 0,
        "TONG_TAI_SAN_NGAN_HAN": 0
      },
      "B_TAI_SAN_DAI_HAN": {
        "Phai_thu_dai_han_khach_hang": 0,
        "Tra_truoc_dai_han": 0,
        "TSCD_huu_hinh": 0,
        "TSCD_vo_hinh": 0,
        "Bat_dong_san_dau_tu": 0,
        "Dau_tu_tai_chinh_dai_han": 0,
        "TONG_TAI_SAN_DAI_HAN": 0
      },
      "TONG_TAI_SAN": 0
    },
    "NGUON_VON": {
      "C_NO_PHAI_TRA": {
        "No_ngan_han": {
          "Phai_tra_nguoi_ban_ngan_han": 0,
          "Nguoi_mua_tra_tien_trước": 0,
          "Thue_phai_nop": 0,
          "Phai_tra_NLD": 0,
          "Phai_tra_ngan_han_khac": 0,
          "Vay_ngan_han": 0,
          "TONG_NO_NGAN_HAN": 0
        },
        "No_dai_han": {
          "TONG_NO_DAI_HAN": 0
        },
        "TONG_NO_PHAI_TRA": 0
      },
      "D_VON_CHU_SO_HUU": {
        "Von_gop_cua_chu_so_huu": 0,
        "Thang_du_von_co_phan": 0,
        "Quy_dau_tu_phat_trien": 0,
        "Quy_du_phong_tai_chinh": 0,
        "Quy_khac_thuoc_von_chu_so_huu": 0,
        "LNST_chua_phan_phoi": 0,
        "TONG_VON_CHU_SO_HUU": 0
      },
      "TONG_NGUON_VON": 0
    }
  },
  "validation": {
    "balance_check": true,
    "total_assets": 0,
    "total_equity_liabilities": 0,
    "difference": 0
  },
  "comparative_period": {},
  "disclaimer": "BCTC dự thảo. Kế toán trưởng và kiểm toán viên xác nhận trước khi nộp."
}
```

### Báo cáo KQKD (B02)

```json
{
  "skill": "accounting-financial-reports",
  "report_type": "B02",
  "period": { "from_date": "DD/MM/YYYY", "to_date": "DD/MM/YYYY" },
  "regime": "tt99",
  "income_statement": {
    "Doanh_thu_ban_hang": 0,
    "Cac_khoan_giam_tru_DT": 0,
    "Doanh_thu_thuan": 0,
    "Gia_von_hang_ban": 0,
    "Loi_nhuan_gop": 0,
    "Doanh_thu_hoat_dong_tai_chinh": 0,
    "Chi_phi_tai_chinh": 0,
    "Chi_phi_ban_hang": 0,
    "Chi_phi_QLDN": 0,
    "Loi_nhuan_thuan_HDKD": 0,
    "Thu_nhap_khac": 0,
    "Chi_phi_khac": 0,
    "Loi_nhuan_khac": 0,
    "Tong_LN_truoc_thue": 0,
    "Chi_phi_thue_TNDN_hien_hanh": 0,
    "Chi_phi_thue_TNDN_hoan_lai": 0,
    "Loi_nhuan_sau_thue": 0
  },
  "disclaimer": "..."
}
```

---

## Escalation Rules

Escalate khi:
- Tổng tài sản ≠ Tổng nguồn vốn (sai cân đối)
- Tổng phát sinh Nợ ≠ Tổng phát sinh Có trên sổ cái
- Có TK không thể ánh xạ vào chỉ tiêu BCTC
- Có chỉ tiêu bất thường (vd: LNST âm nhưng vốn chủ sở hữu dương kéo dài)
- BCTC hợp nhất (cần loại trừ giao dịch nội bộ)
- Có giao dịch ngoại tệ cần tính tỷ giá

---

## Legal Disclaimer

Skill này hỗ trợ lập BCTC dự thảo theo chế độ kế toán VN. Không thay thế phán
quyết chuyên môn của kế toán trưởng, kiểm toán viên, hoặc cơ quan thuế. Mẫu
biểu BCTC theo TT 99/2025 cần được xác minh là phiên bản hiện hành trên
Cổng thông tin Bộ Tài chính. BCTC chính thức nộp cho cơ quan nhà nước phải
được ký và đóng dấu bởi người có thẩm quyền.