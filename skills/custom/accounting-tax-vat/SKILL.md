---
name: accounting-tax-vat
description: >
  Kê khai và quyết toán thuế Giá trị gia tăng (VAT) Việt Nam theo Luật
  48/2024/QH15, Nghị định 174/2025/NĐ-CP, Thông tư 219/2013/TT-BTC. Trigger
  khi user cần: lập tờ khai thuế GTGT (mẫu 01/GTGT), xác định thuế suất
  (0%/5%/8%/10%), kiểm tra điều kiện khấu trừ VAT đầu vào, lập bảng kê
  hóa đơn, hoặc quyết toán thuế cuối năm.
version: 1.1.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - vat
  - tax-filing
  - tax-finalization
  - input-vat-deduction
author: DeerFlow Community
created: 2025-07-06
updated: 2026-09-09
legal_basis:
  - Luật 48/2024/QH15 (Luật Quản lý thuế)
  - Luật Thuế GTGT 2024 (sửa đổi Luật 13/2008)
  - Nghị định 174/2025/NĐ-CP
  - Nghị định 123/2020/NĐ-CP
  - Thông tư 219/2013/TT-BTC
  - Thông tư 78/2021/TT-BTC
  - Thông tư 32/2025/TT-BTC
---

# Skill Thuế GTGT Việt Nam

## Mục đích

Hỗ trợ kê khai và quyết toán **thuế Giá trị gia tăng (VAT)** tại Việt Nam:
- Xác định thuế suất áp dụng
- Kiểm tra điều kiện khấu trừ VAT đầu vào
- Lập tờ khai thuế GTGT (mẫu 01/GTGT)
- Lập bảng kê hóa đơn đầu vào / đầu ra
- Quyết toán thuế cuối năm

Tuân thủ theo:
- Luật 48/2024/QH15 — Luật Quản lý thuế
- Luật Thuế GTGT 2024 — sửa đổi Luật 13/2008/QH12 (có hiệu lực từ
  01/07/2025)
- Nghị định 174/2025/NĐ-CP — giảm thuế suất VAT tiêu chuẩn 10% → 8%
  trong giai đoạn 01/07/2025 – 31/12/2026
- Thông tư 219/2013/TT-BTC — hướng dẫn thi hành Luật VAT cũ (vẫn áp dụng
  một số điều)

## Khi nào sử dụng

- **Lập tờ khai thuế GTGT khấu trừ** (mẫu 01/GTGT) hàng tháng/quý
- **Lập tờ khai thuế GTGT trực tiếp** (mẫu 02/GTGT, 03/GTGT)
- **Xác định thuế suất VAT** cho hàng hóa/dịch vụ cụ thể
- **Kiểm tra điều kiện khấu trừ VAT đầu vào**
- **Lập bảng kê hóa đơn** (mẫu 01-1/GTGT, 01-2/GTGT, 01-3/GTGT, ...)
- **Quyết toán thuế GTGT cuối năm** (mẫu 02-1/GTGT khi có điều chỉnh)
- **Tư vấn nội bộ về điều kiện khấu trừ, hóa đơn hợp lệ**

## Khi nào KHÔNG sử dụng

- **Thuế TNDN**: dùng `accounting-corporate-income-tax`
- **Thuế TNCN**: dùng `accounting-payroll`
- **Validate hóa đơn đầu vào** (kiểm tra trường, format): dùng
  `accounting-invoice-check` hoặc `accounting-einvoice`
- **Tư vấn pháp lý cuối cùng**: cần tư vấn viên thuế có chứng chỉ

---

## Đầu vào Bắt buộc

### Đầu vào Chung

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `period` | object | Có | Kỳ tính thuế: `{type, year, month, quarter}` |
| `company_info` | object | Có | Tên DN, MST, địa chỉ, kỳ kế toán |
| `filing_method` | enum | Có | `"monthly"` hoặc `"quarterly"` |
| `vat_method` | enum | Có | `"deduction"` (khấu trừ) hoặc `"direct"` (trực tiếp) |
| `sales_invoices` | array | Có | Hóa đơn đầu ra trong kỳ |
| `purchase_invoices` | array | Có | Hóa đơn đầu vào trong kỳ |

### Đầu vào Riêng theo Phương pháp

#### Phương pháp Khấu trừ (Deduction)

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `input_vat_breakdown` | object | Có | VAT đầu vào theo thuế suất và loại |
| `output_vat_breakdown` | object | Có | VAT đầu ra theo thuế suất |
| `carryover_vat` | number | Tùy chọn | VAT nộp thừa từ kỳ trước |
| `adjustments` | array | Tùy chọn | Điều chỉnh thuế (giảm giá, hàng khuyến mại, ...) |

#### Phương pháp Trực tiếp (Direct)

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `revenue_total` | number | Có | Tổng doanh thu trong kỳ |
| `industry_tier` | enum | Có | Phân ngành theo Thông tư 219 |

---

## Thuế suất VAT hiện hành (2026)

Theo Luật Thuế GTGT 2024 và Nghị định 174/2025/NĐ-CP:

| Thuế suất | Phạm vi | Có hiệu lực |
|-----------|---------|-------------|
| **0%** | Hàng hóa/dịch vụ xuất khẩu, vận tải quốc tế, hàng hóa/dịch vụ thiết yếu theo Phụ lục | Luôn |
| **5%** | Hàng hóa/dịch vụ thiết yếu: nước sạch, y tế, giáo dục, nông nghiệp, vận tải công cộng, sách, ... | Luôn |
| **8%** | **Thuế suất tiêu chuẩn** (giảm từ 10% theo NĐ 174/2025) cho hàng hóa/dịch vụ thông thường | 01/07/2025 – 31/12/2026 |
| **10%** | Thuế suất tiêu chuẩn (mặc định) — áp dụng cho HH/DV không thuộc diện 0%, 5%, 8%; và áp dụng SAU 31/12/2026 nếu NĐ 174/2025 không gia hạn | Luôn (mặc định) |

### Lưu ý quan trọng về thuế suất 8% (NĐ 174/2025)

- Áp dụng cho **hóa đơn phát hành** trong giai đoạn từ 01/07/2025 đến
  31/12/2026
- Giảm từ thuế suất 10% tiêu chuẩn xuống 8%
- **KHÔNG áp dụng** cho:
  - Hàng hóa/dịch vụ đã chịu 5%
  - Hàng hóa/dịch vụ đã chịu 0%
  - Hàng hóa/dịch vụ không chịu VAT (theo Điều 5, Luật 48/2024/QH15)
- Đối với hóa đơn bao trùm ngày 30/06/2025 và 01/07/2025: áp dụng theo
  ngày phát hành hóa đơn

### Xác định thuế suất cho hàng hóa/dịch vụ

Theo Điều 9, Luật 48/2024/QH15 và Phụ lục kèm theo:

| Nhóm | Thuế suất | Ví dụ |
|------|-----------|-------|
| Hàng hóa/dịch vụ xuất khẩu | 0% | Hàng hóa xuất khẩu, dịch vụ cung cấp cho tổ chức nước ngoài |
| Nông sản chưa qua chế biến | 0% | Lúa, ngô, rau quả tươi (một số) |
| Dịch vụ y tế, giáo dục | 0% / 5% | Khám chữa bệnh, dạy học |
| Hàng thiết yếu | 5% | Nước sạch, sách, dược phẩm |
| Vận tải công cộng | 5% | Xe buýt, tàu điện (một số) |
| Tiêu chuẩn (mặc định) | 8% (gđ 2025-2026) / 10% | Đồ gia dụng, quần áo, điện tử, dịch vụ thông thường |
| Hàng hóa/dịch vụ không chịu VAT | Không | Theo Điều 5, Luật 48/2024 |

> ⚠️ **Cần xác minh**: Phụ lục thuế suất 5% được sửa đổi bổ sung theo từng
> thời kỳ. Tra cứu văn bản hiện hành trước khi xác định.

---

## Phương pháp Tính thuế

### Phương pháp Khấu trừ (Deduction)

Áp dụng cho: DN, hợp tác xã có doanh thu > 1 tỷ VND/năm, hoặc tự nguyện
đăng ký.

**Công thức**:

```
VAT phải nộp = VAT đầu ra - VAT đầu vào được khấu trừ
            + VAT đầu vào không được khấu trừ (nếu có)
            ± Điều chỉnh thuế của kỳ trước
            - VAT nộp thừa kỳ trước (nếu có)
```

Trong đó:

```
VAT đầu ra = Σ (giá tính thuế × thuế suất) của tất cả hóa đơn bán ra trong kỳ

VAT đầu vào = Σ (giá tính thuế × thuế suất) của các hóa đơn mua vào
             được khấu trừ theo điều kiện (xem dưới)
```

### Phương pháp Trực tiếp trên GTGT (Direct Value Added)

Áp dụng cho: DN có doanh thu ≤ 1 tỷ VND/năm không theo phương pháp khấu trừ.

**Công thức**:

```
VAT phải nộp = Giá trị gia tăng × Tỷ lệ % thuế GTGT
```

Trong đó:

| Phân ngành | Tỷ lệ % |
|------------|---------|
| Phân phối, cung cấp hàng hóa | 1% |
| Dịch vụ, xây dựng không bao thầu NVL | 5% |
| Sản xuất, vận tải, dịch vụ có gắn với hàng hóa, xây dựng có bao thầu NVL | 3% |
| Hoạt động kinh doanh khác | 2% |

> ⚠️ **Cần xác minh**: Tỷ lệ % thuế suất trực tiếp có thể đã thay đổi theo
> các sửa đổi của Luật VAT 2024.

### Phương pháp Trực tiếp trên Doanh thu (Direct Revenue)

Áp dụng cho: cá nhân, hộ kinh doanh không theo phương pháp khấu trừ, doanh
thu từ hoạt động vàng/bạc/đá quý.

**Công thức**:

```
VAT phải nộp = Doanh thu tính thuế × Tỷ lệ % thuế GTGT
```

Trong đó:

| Loại doanh thu | Tỷ lệ % |
|----------------|---------|
| Vàng, bạc, đá quý | 10% (chưa bao gồm thuế VAT) |

---

## Điều kiện Khấu trừ VAT đầu vào

Để được khấu trừ, VAT đầu vào phải đáp ứng **đồng thời** các điều kiện
sau:

### Điều kiện 1: Có hóa đơn hợp lệ

- HĐĐT có mã CQT (cho B2B) — xem skill `accounting-einvoice`
- Hóa đơn giấy còn hiệu lực (chỉ trong trường hợp đặc biệt)
- Đầy đủ các trường bắt buộc theo Điều 10, NĐ 123/2020/NĐ-CP
- Ngày hóa đơn trong kỳ khai thuế hoặc kỳ trước liền kề (nếu chưa kê khai)
- **Không thuộc hóa đơn bị hủy, thay thế, điều chỉnh** mà không cập nhật

### Điều kiện 2: Có chứng từ thanh toán (cho hóa đơn ≥ 20 triệu VND)

Theo Khoản 11, Điều 1, Nghị định 100/2016/NĐ-CP (sửa đổi NĐ 51/2010):

> Khi mua hàng hóa, dịch vụ từ 20 triệu VND trở lên phải có chứng từ
> thanh toán qua ngân hàng.

Chứng từ hợp lệ:
- UNC (ủy nhiệm chi) qua ngân hàng
- Séc chuyển khoản
- Giấy nộp tiền vào NSNN (nếu thanh toán cho cơ quan nhà nước)
- Xác nhận chuyển tiền qua mobile/internet banking (kèm sao kê)

### Điều kiện 3: Phục vụ hoạt động SXKD chịu VAT

| Được khấu trừ | KHÔNG được khấu trừ |
|---------------|---------------------|
| Hàng hóa/dịch vụ dùng cho SXKD chịu VAT | Hàng hóa/dịch vụ dùng cho hoạt động không chịu VAT |
| Đầu vào cho xuất khẩu | Hàng hóa/dịch vụ dùng cho hoạt động miễn thuế |
| Đầu vào cho cả hai hoạt động → phân bổ theo tỷ lệ doanh thu | Đầu vào cho hoạt động tài chính, chuyển nhượng vốn |

> ⚠️ Trường hợp DN có cả hoạt động chịu VAT và không chịu VAT, phải phân
> bổ VAT đầu vào theo tỷ lệ doanh thu (Điều 10, TT 219/2013/TT-BTC).

### Điều kiện 4: Hóa đơn ghi đúng người mua

Hóa đơn phải ghi:
- Tên và MST của DN đang kê khai (KHÔNG phải chi nhánh khác)
- Hoặc chi nhánh được phép riêng (nếu DN đăng ký kê khai riêng)

### Điều kiện 5: Hạch toán đúng tài khoản

- VAT đầu vào hạch toán vào TK 1331 (theo TT 200/TT 99) hoặc TK 133
  (theo TT 133)
- Phân bổ cho phù hợp với hoạt động SXKD

---

## Trường hợp KHÔNG được khấu trừ

Theo Điều 10, Nghị định 174/2025/NĐ-CP:

| Trường hợp | Hướng dẫn |
|-----------|-----------|
| Hàng hóa/dịch vụ dùng cho hoạt động không chịu VAT | Hạch toán vào chi phí (đã bao gồm VAT) |
| Hàng hóa/dịch vụ dùng cho hoạt động miễn thuế | Tương tự |
| Chi phí không có hóa đơn (không đủ điều kiện) | Hạch toán vào chi phí |
| Hóa đơn không hợp lệ | Hạch toán vào chi phí |
| Hàng hóa thiếu không rõ nguyên nhân (có dấu hiệu gian lận) | Phải giảm trừ VAT đầu vào tương ứng |
| Phần VAT vượt mức khấu trừ cho ô tô | Theo quy định cụ thể |
| Tiền thuê nhà, điện, nước dùng cho cá nhân | Hạch toán vào chi phí cá nhân |
| Chi phí quà tặng, hỗ trợ không phục vụ SXKD | Hạch toán vào chi phí không được trừ |

---

## Quy trình Kê khai Thuế

### Kê khai theo Tháng (mặc định)

**Thời hạn nộp tờ khai**: Ngày 20 của tháng tiếp theo tháng phát sinh nghĩa
vụ thuế.

**Hồ sơ khai thuế**:
1. Tờ khai thuế GTGT (mẫu 01/GTGT)
2. Bảng kê hóa đơn bán ra (mẫu 01-1/GTGT)
3. Bảng kê hóa đơn mua vào (mẫu 01-2/GTGT)
4. Bảng kê hàng hóa/dịch vụ bán ra (nếu có)

### Kê khai theo Quý (doanh thu ≤ 50 tỷ VND/năm)

**Điều kiện**: Tổng doanh thu bán ra của năm trước liền kề ≤ 50 tỷ VND (trừ
trường hợp bắt buộc theo tháng).

**Thời hạn nộp**: Ngày cuối cùng của tháng đầu quý sau.

**Lưu ý**: Nếu kê khai theo quý, được trừ 2% VAT phải nộp (theo Nghị định
số 174/2025 hoặc văn bản hiện hành). Cần kiểm tra quy định mới nhất.

### Quyết toán thuế cuối năm

- Hạn nộp: Ngày cuối cùng của tháng thứ 3 kể từ ngày kết thúc năm tài chính
  (thường là 31/03 năm sau)
- Mẫu tờ khai quyết toán: 02/GTGT (TT 80/2019 hoặc văn bản mới hơn)
- Kèm bảng kê điều chỉnh nếu có sai sót trong năm

---

## Quy trình Từng bước để Lập Tờ khai

### Bước 1: Tổng hợp Doanh thu (đầu ra)

Tổng hợp tất cả hóa đơn bán ra trong kỳ, phân loại theo thuế suất:

```json
{
  "total_revenue": 1000000000,
  "by_rate": [
    {
      "rate": 10,
      "revenue_excl_vat": 500000000,
      "output_vat": 50000000
    },
    {
      "rate": 8,
      "revenue_excl_vat": 300000000,
      "output_vat": 24000000
    },
    {
      "rate": 5,
      "revenue_excl_vat": 100000000,
      "output_vat": 5000000
    },
    {
      "rate": 0,
      "revenue_excl_vat": 100000000,
      "output_vat": 0
    }
  ],
  "total_output_vat": 79000000
}
```

### Bước 2: Tổng hợp VAT đầu vào được khấu trừ

Phân loại theo thuế suất:

```json
{
  "total_input_vat": 45000000,
  "by_rate": [
    { "rate": 10, "input_vat": 30000000 },
    { "rate": 8, "input_vat": 12000000 },
    { "rate": 5, "input_vat": 3000000 }
  ]
}
```

### Bước 3: Tính VAT phải nộp

```
VAT phải nộp = VAT đầu ra - VAT đầu vào được khấu trừ
             = 79.000.000 - 45.000.000
             = 34.000.000 VND
```

### Bước 4: Kiểm tra chéo

| Kiểm tra | Cách thực hiện |
|-----------|----------------|
| Tổng Nợ 3331 + 3332 = VAT đầu ra | Đối chiếu sổ cái |
| Tổng Có 133 = VAT đầu vào | Đối chiếu sổ cái |
| VAT nộp kỳ này khớp với tờ khai | Đối chiếu UNC |

### Bước 5: Điều chỉnh (nếu có)

| Điều chỉnh | Xử lý |
|-----------|-------|
| Giảm giá hàng bán | Điều chỉnh giảm DT và VAT đầu ra |
| Hàng khuyến mại | Theo quy định cụ thể (có thể không phải điều chỉnh DT) |
| Hóa đơn sai → xuất lại | Điều chỉnh kỳ phát hiện |
| Phát hiện hóa đơn đầu vào thiếu kỳ trước | Khai bổ sung |

---

## Điều chỉnh Thuế và Xử lý Sai sót

### Sai sót trong cùng kỳ kê khai

- Phát hiện và sửa trước khi nộp tờ khai
- Không cần lập tờ khai bổ sung

### Sai sót đã nộp tờ khai (cùng năm tài chính)

- Lập **Tờ khai bổ sung** (mẫu 01/GTGT - BS)
- Nộp phạt nếu thiếu thuế (có thể miễn/giảm nếu tự giác khai bổ sung)
- Lãi chậm nộp (0,03%/ngày trên số thuế nộp thiếu)

### Sai sót năm trước (đã quyết toán)

- Lập **Tờ khai bổ sung cho quyết toán** (mẫu 02/GTGT - BS)
- Phạt + lãi chậm nộp (nếu thiếu thuế)
- Tự giác khai bổ sung → có thể miễn/giảm phạt

---

## Các Tình huống Đặc biệt

### 1. Xuất khẩu (VAT 0%)

Điều kiện:
- Có tờ khai hải quan điện tử
- Hàng hóa thực xuất qua cửa khẩu Việt Nam
- Thanh toán qua ngân hàng (trừ một số trường hợp)
- Hóa đơn ghi rõ "xuất khẩu" + mã số hải quan

> Cần có bảng kê riêng cho hàng hóa/dịch vụ xuất khẩu.

### 2. Hoàn thuế VAT

Theo Điều 26, Luật 48/2024/QH15:

**Trường hợp được hoàn**:
- Dự án đầu tư (chưa hoàn thành, hoặc đã hoàn thành trong giai đoạn đầu tư)
- Hàng hóa/dịch vụ xuất khẩu (một số trường hợp)
- DN nộp thừa trong kỳ (tự động khấu trừ kỳ sau hoặc hoàn)

**Hồ sơ hoàn thuế**:
- Tờ khai thuế hoàn
- Hợp đồng, hóa đơn, chứng từ
- Xác nhận của ngân hàng (nếu thanh toán ra nước ngoài)
- Hồ sơ kiểm tra tại trụ sở (nếu DN lần đầu hoàn)

### 3. Giảm trừ VAT đầu vào

Trường hợp phải giảm trừ:
- Hàng thiếu không rõ nguyên nhân (xem `accounting-stocktake`)
- Hàng hóa sử dụng sai mục đích (sau khi đã khấu trừ)
- Hóa đơn bị hủy, thay thế

```
Nợ TK 811    Chi phí khác (phần VAT)
    Có TK 1331   Thuế GTGT đầu vào (giảm)
```

### 4. VAT hàng nhập khẩu

- Khai thuế tại Chi cục Hải quan
- VAT NK được khấu trừ nếu đủ điều kiện
- Kê khai riêng trong tờ khai VAT (mục "Hàng nhập khẩu")

---

## Định dạng Đầu ra

```json
{
  "skill": "accounting-tax-vat",
  "version": "1.1.0",
  "period": { "year": 0, "month": 0, "quarter": 0 },
  "company_info": { "name": "", "tax_code": "" },
  "filing_method": "monthly|quarterly",
  "vat_method": "deduction|direct_value_added|direct_revenue",
  "output_vat_breakdown": {
    "by_rate": [
      { "rate": 0, "revenue_excl_vat": 0, "output_vat": 0 },
      { "rate": 5, "revenue_excl_vat": 0, "output_vat": 0 },
      { "rate": 8, "revenue_excl_vat": 0, "output_vat": 0 },
      { "rate": 10, "revenue_excl_vat": 0, "output_vat": 0 }
    ],
    "total_output_vat": 0
  },
  "input_vat_breakdown": {
    "by_rate": [
      { "rate": 0, "input_vat": 0, "deductible": 0, "non_deductible": 0 },
      { "rate": 5, "input_vat": 0, "deductible": 0, "non_deductible": 0 },
      { "rate": 8, "input_vat": 0, "deductible": 0, "non_deductible": 0 },
      { "rate": 10, "input_vat": 0, "deductible": 0, "non_deductible": 0 }
    ],
    "total_deductible": 0
  },
  "vat_payable": {
    "output_vat": 0,
    "input_vat_deductible": 0,
    "carryover_vat": 0,
    "adjustments": 0,
    "vat_payable_this_period": 0
  },
  "deduction_conditions_check": {
    "all_invoices_valid": true,
    "all_high_value_invoices_have_bank_proof": true,
    "all_for_business_purpose": true,
    "all_posted_correctly": true,
    "issues": []
  },
  "rate_reduction_check": {
    "period_covered": "2025-07-01_to_2026-12-31",
    "correctly_applied_8_percent": true,
    "issues": []
  },
  "filing_summary": {
    "total_revenue_excl_vat": 0,
    "total_output_vat": 0,
    "total_deductible_input_vat": 0,
    "vat_to_pay": 0,
    "vat_overpaid_carryover": 0,
    "filing_deadline": "YYYY-MM-DD"
  },
  "flags": [
    {
      "flag": "",
      "severity": "low|medium|high|critical",
      "description": ""
    }
  ],
  "recommendations": [],
  "disclaimer": "Bản kê khai dự thảo dựa trên dữ liệu user cung cấp. Cần xác minh với sổ sách và tư vấn thuế trước khi nộp chính thức."
}
```

---

## Quy tắc Chống Ảo giác

### Quy tắc 1: Không bịa thuế suất

Chỉ sử dụng thuế suất đã được xác minh theo Luật VAT hiện hành. Nếu không
chắc chắn, escalate cho tư vấn thuế.

### Quy tắc 2: Không tự ý áp điều kiện khấu trừ

Kiểm tra đủ 5 điều kiện khấu trừ. Nếu thiếu một điều kiện → flag, KHÔNG
khấu trừ.

### Quy tắc 3: Trích dẫn chính xác

Khi tham chiếu điều khoản, ghi rõ số hiệu văn bản. KHÔNG bịa điều khoản
không tồn tại.

### Quy tắc 4: Không tự đánh giá tính hợp lệ của hóa đơn

Chỉ kiểm tra logic. Việc xác minh mã CQT, MST đang hoạt động phải tra cứu
trên Cổng thuế.

### Quy tắc 5: Luôn kèm tuyên bố miễn trừ

Mọi đầu ra đều phải có disclaimer.

---

## Quy tắc Escalate

| Tình huống | Mức độ | Người nhận |
|-----------|--------|-----------|
| Chênh lệch VAT > 50 triệu so với kỳ trước | HIGH | Kế toán trưởng |
| Nghi ngờ hóa đơn đầu vào giả | CRITICAL | Kế toán trưởng + KTNB |
| VAT phải nộp > 1 tỷ VND/tháng | HIGH | Kế toán trưởng |
| Phát hiện nhiều hóa đơn không có chứng từ CK | HIGH | Kế toán trưởng |
| Sai sót > 100 triệu trong tờ khai | HIGH | Kế toán trưởng + Tư vấn thuế |
| Yêu cầu hoàn thuế | HIGH | Kế toán trưởng + Tư vấn thuế |

---

## Tuyên bố Miễn trừ Pháp lý

**QUAN TRỌNG**: Skill này cung cấp hướng dẫn và bản kê khai dự thảo. Không
phải tư vấn pháp lý. Việc xác định thuế suất, điều kiện khấu trừ cần:
- Đối chiếu với văn bản pháp luật hiện hành
- Tư vấn viên thuế có chứng chỉ
- Quyết định cuối cùng của cơ quan thuế

**Văn bản tham chiếu chính**:
- Luật 48/2024/QH15 — Luật Quản lý thuế (thông qua 21/11/2024)
- Luật Thuế GTGT 2024 — sửa đổi Luật 13/2008/QH12 (có hiệu lực từ
  01/07/2025)
- Nghị định 174/2025/NĐ-CP — giảm thuế suất VAT
- Nghị định 123/2020/NĐ-CP — hóa đơn, chứng từ
- Thông tư 219/2013/TT-BTC — hướng dẫn VAT

> ⚠️ **Cần xác minh**: Một số điều khoản cụ thể của Luật VAT 2024 và Nghị
> định 174/2025 có thể đã được sửa đổi hoặc hướng dẫn bổ sung. Tra cứu
> Cổng thuế điện tử và văn bản mới nhất trước khi áp dụng.

---

*Cập nhật lần cuối: 2026-09-09*
*Phiên bản skill: 1.1.0*