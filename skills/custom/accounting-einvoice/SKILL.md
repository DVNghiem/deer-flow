---
name: accounting-einvoice
description: >
  Kiểm tra và xác thực hóa đơn điện tử (HĐĐT) theo NĐ 123/2020, TT 78/2021,
  TT 32/2025. Trigger khi user cần: validate hóa đơn điện tử có mã CQT, ki
  tra tra cứu trên Cổng thuế điện tử, validate XML schema theo chuẩn của Tổng
  cục Thuế, kiểm tra tính hợp lệ khi hạch toán VAT đầu vào.
version: 1.0.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - e-invoice
  - tax-compliance
  - vat
---

# Accounting E-Invoice Skill

## Purpose

Kiểm tra, xác thực hóa đơn điện tử (HĐĐT) theo quy định hiện hành của Việt
Nam. Hỗ trợ validation các trường quan trọng, kiểm tra mã CQT, kiểm tra
XML schema theo chuẩn Tổng cục Thuế, phát hiện các rủi ro trước khi sử dụng
hóa đơn để hạch toán VAT đầu vào.

**Legal Framework:**
- Nghị định 123/2020/NĐ-CP — Quy định về hóa đơn, chứng từ
- Thông tư 78/2021/TT-BTC — Hướng dẫn hóa đơn điện tử
- Thông tư 32/2025/TT-BTC — Sửa đổi bổ sung TT 78/2021
- Luật Thuế GTGT (Luật 48/2024/QH15)
- Quyết định của Tổng cục Thuế về định dạng XML hóa đơn điện tử

> ⚠️ **Cần xác minh**: Chuẩn XML hóa đơn điện tử được cập nhật định kỳ.
> Cần kiểm tra phiên bản schema hiện hành trên Cổng thuế điện tử.

## When to Use

- Validate HĐĐT trước khi hạch toán VAT đầu vào
- Kiểm tra mã CQT (mã xác thực của cơ quan thuế)
- Validate XML schema theo chuẩn TCT
- Kiểm tra trạng thái hóa đơn (đã cấp mã, đang sử dụng, đã hủy, ...)
- Tra cứu MST người bán / người mua
- Kiểm tra hóa đơn bị thay thế / điều chỉnh / hủy
- Phân biệt HĐĐT có mã CQT và không có mã CQT

## When NOT to Use

- Hóa đơn giấy truyền thống → dùng `accounting-invoice-check`
- Ký số và cấp chứng thư số (do nhà cung cấp HĐĐT)
- Tích hợp API với TCT (do nhà phát triển HĐĐT)
- Lập tờ khai thuế liên quan đến HĐĐT
- Kiểm tra pháp lý hợp đồng mua bán hàng hóa

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `invoice_data` | object | Yes | Core invoice fields |
| `invoice_type` | enum | Yes | `"with_cqt_code"` (có mã CQT) hoặc `"without_cqt_code"` (B2C) |
| `xml_data` | object | No | XML parsed nếu có |
| `cqt_code` | string | No | Mã CQT (nếu có mã) |
| `lookup_evidence` | object | No | Kết quả tra cứu trên Cổng thuế |

---

## Hệ thống HĐĐT tại Việt Nam

### Hai loại hóa đơn điện tử chính

| Loại | Đặc điểm | Sử dụng khi |
|------|----------|--------------|
| **HĐĐT có mã CQT** | Có mã xác thực do cơ quan thuế cấp | B2B, cần khấu trừ VAT, đầu vào |
| **HĐĐT không có mã CQT** | Không có mã CQT (chỉ có chữ ký số NCC) | B2C, bán lẻ, không cần khấu trừ |

### Lưu ý quan trọng

> Từ 01/07/2022, hóa đơn điện tử được sử dụng đại trà. Hóa đơn giấy hầu
> như không còn được phát hành mới (trừ một số trường hợp đặc biệt).

---

## Step-by-Step Workflow

### Bước 1: Kiểm tra loại hóa đơn

```
IF invoice_type == "with_cqt_code":
    Yêu cầu cqt_code hợp lệ
    Bắt buộc có đầy đủ thông tin B2B
ELIF invoice_type == "without_cqt_code":
    Không bắt buộc mã CQT
    Đơn giản hơn nhưng không dùng để khấu trừ VAT
```

### Bước 2: Validate các trường bắt buộc (Điều 10, NĐ 123/2020)

| Trường | Bắt buộc? | Validation |
|--------|-----------|------------|
| Số hóa đơn | Có | Theo format từng nhà cung cấp |
| Ngày lập | Có | DD/MM/YYYY hoặc ISO 8601 |
| Tên người bán | Có | Khớp đăng ký kinh doanh |
| MST người bán | Có | 10 hoặc 13 số, đúng checksum |
| Địa chỉ người bán | Có | Khớp đăng ký |
| Tên người mua | Có (B2B) | Khớp MST người mua |
| MST người mua | Có (B2B) | 10 hoặc 13 số |
| Địa chỉ người mua | Có (B2B) | Đầy đủ |
| Mặt hàng | Có | Ít nhất 1 dòng |
| Số lượng, đơn giá | Có | > 0 |
| Tổng tiền chưa VAT | Có | = Σ line items |
| VAT rate, VAT amount | Có | Khớp luật áp dụng |
| Tổng thanh toán | Có | = subtotal + VAT |
| Mã CQT | Có (nếu B2B) | Format từ TCT cấp |

### Bước 3: Validate MST (mã số thuế)

**Format MST Việt Nam**:
- Cá nhân: 10 số (có thể 13 số)
- DN: 10 số hoặc 13 số
- MST bắt đầu bằng: 0 (cá nhân), 0xx (DN), 8xx (DN nước ngoài)...

**Validation**:
```
1. Check độ dài (10 hoặc 13)
2. Check checksum (nếu có thuật toán MST)
3. Tra cứu trên tracuunnt.gdt.gov.vn để verify DN đang hoạt động
```

### Bước 4: Validate mã CQT (nếu có)

Mã CQT là chuỗi do cơ quan thuế cấp sau khi nhận HĐĐT từ NCC. Bao gồm:
- Mã số CQT (mã cơ quan thuế)
- Số thứ tự cấp mã
- Mã xác thực

**Cách kiểm tra**:
1. Đối chiếu format mã CQT do TCT quy định
2. Tra cứu trên Cổng thuế điện tử (hoặc APP eTax Mobile)
3. Verify trạng thái: VALID / INVALID / CANCELLED

### Bước 5: Validate XML schema (nếu có)

XML HĐĐT phải tuân theo schema do TCT ban hành. Các trường quan trọng:
- `<Invoice>` — root
- `<InvoiceNumber>` — số hóa đơn
- `<InvoiceDate>` — ngày lập (YYYY-MM-DD)
- `<SellerInfo>`, `<BuyerInfo>` — thông tin bên bán/mua
- `<ItemList>` — danh sách mặt hàng
- `<TaxBreakdown>` — phân tích thuế
- `<Signature>` — chữ ký số
- `<CQTCode>` — mã CQT (nếu có)

> ⚠️ Schema XML được cập nhật theo từng phiên bản. Cần tra cứu schema
> hiện hành trên Cổng thuế điện tử.

### Bước 6: Kiểm tra trạng thái hóa đơn

Các trạng thái có thể có:
- `ISSUED` — đã phát hành
- `USED_FOR_DEDUCTION` — đã dùng để khấu trừ VAT
- `REPLACED` — đã thay thế (có HĐĐT khác thay)
- `ADJUSTED` — đã điều chỉnh (có HĐĐT điều chỉnh)
- `CANCELLED` — đã hủy

### Bước 7: Risk Flag Assessment

| Cờ | Mức độ | Mô tả |
|----|--------|-------|
| `missing_cqt_code` | HIGH | HĐĐT B2B không có mã CQT |
| `invalid_mst_seller` | HIGH | MST người bán không hợp lệ |
| `invalid_mst_buyer` | HIGH | MST người mua không hợp lệ |
| `cqt_code_invalid` | CRITICAL | Mã CQT không verify được |
| `invoice_cancelled` | CRITICAL | HĐĐT đã bị hủy |
| `invoice_replaced` | HIGH | HĐĐT đã bị thay thế |
| `seller_not_active` | CRITICAL | Người bán không hoạt động (tra MST) |
| `mst_mismatch` | HIGH | MST trên HĐ không khớp thực tế |
| `amount_mismatch` | HIGH | Tổng tiền không khớp Σ lines |
| `vat_rate_invalid` | HIGH | VAT rate không hợp lệ |
| `format_warning` | MEDIUM | XML format không chuẩn |
| `late_issuance` | MEDIUM | HĐ phát hành trễ (>30 ngày) |

---

## Output Format

```json
{
  "skill": "accounting-einvoice",
  "version": "1.0.0",
  "review_status": "pass|pass_with_warnings|fail",
  "invoice_summary": {
    "invoice_number": "",
    "invoice_date": "YYYY-MM-DD",
    "invoice_type": "with_cqt_code|without_cqt_code",
    "total_amount": 0,
    "vat_amount": 0
  },
  "mandatory_field_check": {
    "status": "complete|incomplete",
    "missing_fields": [],
    "present_fields": []
  },
  "mst_validation": {
    "seller_mst_valid": true,
    "seller_mst_active": true,
    "buyer_mst_valid": true,
    "buyer_mst_active": true
  },
  "cqt_code_check": {
    "has_cqt_code": true,
    "cqt_code_format_valid": true,
    "lookup_status": "valid|invalid|not_found",
    "lookup_date": "YYYY-MM-DD"
  },
  "xml_validation": {
    "is_well_formed": true,
    "schema_version": "",
    "schema_compliant": true,
    "issues": []
  },
  "invoice_status_check": {
    "status": "ISSUED|REPLACED|ADJUSTED|CANCELLED",
    "linked_invoices": []
  },
  "amount_verification": {
    "subtotal_calculated": 0,
    "subtotal_declared": 0,
    "vat_calculated": 0,
    "vat_declared": 0,
    "matches": true
  },
  "risk_flags": [
    {
      "flag": "",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "description": "",
      "recommendation": ""
    }
  ],
  "recommendations": [],
  "disclaimer": "Skill hỗ trợ kiểm tra HĐĐT dựa trên dữ liệu cung cấp. Việc xác thực cuối cùng cần tra cứu trực tiếp trên Cổng thuế điện tử."
}
```

---

## Quy trình tra cứu trên Cổng thuế điện tử

### Tra cứu MST

1. Truy cập: `https://tracuunnt.gdt.gov.vn`
2. Nhập MST cần tra cứu
3. Kiểm tra:
   - Tên DN có khớp với HĐĐT
   - Địa chỉ có khớp
   - Tình trạng hoạt động (đang hoạt động / ngừng / giải thể)
   - Người đại diện

### Tra cứu HĐĐT

1. Truy cập Cổng thuế điện tử (etax.gdt.gov.vn)
2. Hoặc APP eTax Mobile
3. Nhập:
   - MST người bán
   - Số hóa đơn
   - Ngày lập
   - Tổng tiền (để verify)
4. Kiểm tra trạng thái HĐĐT

### Lưu ý

- Tra cứu qua APP cần đăng ký thuế điện tử trước
- Tra cứu qua Cổng thuế cần có tài khoản thuế điện tử
- Một số trường hợp HĐĐT có thể không tra cứu được (lỗi hệ thống TCT)

---

## Anti-Hallucination Rules

### Rule 1: Không tự verify mã CQT

Không thể xác thực mã CQT chỉ dựa trên format. Phải tra cứu trực tiếp trên
Cổng thuế. Skill chỉ kiểm tra format, không verify xác thực.

### Rule 2: Không tự verify MST đang hoạt động

Trạng thái "đang hoạt động" của MST phải tra cứu trên TCT. Skill chỉ kiểm
tra format (10/13 số, checksum).

### Rule 3: Không tự đánh dấu HĐĐT "hợp lệ"

HĐĐT hợp lệ = đủ trường + MST active + mã CQT valid + trạng thái không bị
hủy. Mỗi mục đều cần kiểm tra thực tế.

### Rule 4: Không tự điều chỉnh format XML

Nếu XML không đúng chuẩn, chỉ flag — không tự sửa.

### Rule 5: Trích dẫn cẩn thận

Schema XML, format mã CQT được cập nhật định kỳ. Luôn ghi "theo phiên bản
hiện hành" và khuyến nghị xác minh.

---

## Các tình huống đặc biệt

### HĐĐT thay thế / điều chỉnh

Khi cần sửa HĐĐT đã phát hành:
1. Lập HĐĐT mới (thay thế) với ghi chú "Hóa đơn thay thế cho HĐ số X ngày Y"
2. Hoặc lập HĐĐT điều chỉnh (tăng/giảm tiền)
3. HĐĐT cũ bị hủy tự động trên hệ thống TCT

### HĐĐT hủy

- Được hủy khi chưa kê khai thuế
- Phải có thông báo hủy gửi TCT
- HĐĐT đã dùng để khấu trừ thì không hủy được

### HĐĐT xuất khẩu

- Áp dụng VAT 0%
- Cần kèm tờ khai hải quan
- Mã số hải quan ghi trên HĐĐT

---

## Legal Disclaimer

Skill này hỗ trợ kiểm tra HĐĐT dự thảo dựa trên dữ liệu cung cấp. **Xác
thực cuối cùng phải thực hiện trên Cổng thuế điện tử** của Tổng cục Thuế
(etax.gdt.gov.vn) hoặc APP eTax Mobile.

Các yếu tố phụ thuộc phiên bản:
- Chuẩn XML HĐĐT (cập nhật định kỳ)
- Format mã CQT
- Quy định về hóa đơn (TT 78/2021, TT 32/2025, các sửa đổi tiếp theo)

DN sử dụng HĐĐT để khấu trừ VAT đầu vào cần:
- Tra cứu mã CQT trên Cổng thuế
- Lưu trữ HĐĐT theo quy định (5 năm)
- Đối chiếu HĐĐT với sổ sách kế toán hàng kỳ