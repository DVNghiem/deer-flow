---
name: accounting-invoice-check
description: >
  Kiểm tra hóa đơn thương mại Việt Nam về tính đầy đủ, tuân thủ quy định và
  cờ rủi ro thuế theo Nghị định 123/2020/NĐ-CP, Luật 48/2024/QH15 và Nghị
  định 174/2025/NĐ-CP. Trigger khi user cần review hóa đơn đầu vào, đánh
  giá hóa đơn chi phí được trừ, hoặc chuẩn bị quyết toán thuế.
version: 1.1.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - invoice-validation
  - tax-compliance
  - decree-123
  - decree-174
author: DeerFlow Community
created: 2025-07-06
updated: 2026-09-09
legal_basis:
  - Nghị định 123/2020/NĐ-CP
  - Luật 48/2024/QH15
  - Nghị định 174/2025/NĐ-CP
  - Thông tư 219/2013/TT-BTC
  - Thông tư 78/2021/TT-BTC
  - Thông tư 32/2025/TT-BTC
---

# Skill Kiểm tra Hóa đơn Kế toán

## Mục đích

Rà soát hóa đơn thương mại Việt Nam nhằm kiểm tra tính tuân thủ quy định,
tính đầy đủ và phát hiện cờ rủi ro thuế. Skill này kiểm tra hóa đơn theo:
- Yêu cầu trường bắt buộc tại Điều 10, Nghị định 123/2020/NĐ-CP
- Quy định thuế suất tại Điều 9, Luật 48/2024/QH15
- Điều kiện khấu trừ thuế GTGT đầu vào

Từ đó nhận diện các lỗi phổ biến có thể dẫn đến phát hiện kiểm toán hoặc
truy thu từ cơ quan thuế.

## Khi nào sử dụng

- **Kiểm tra chi phí được trừ**: Trước khi duyệt đề nghị thanh toán cho hóa
  đơn từ 20 triệu VND trở lên cần có chứng từ chuyển khoản
- **Quyết toán thuế quý/năm**: Trong quá trình chuẩn bị tờ khai thuế, phát
  hiện hóa đơn thiếu chứng từ hoặc có rủi ro
- **Tự động hóa xử lý hóa đơn**: Làm checkpoint trong hệ thống workflow kế toán
- **Onboarding nhà cung cấp**: Kiểm tra chất lượng hóa đơn trước khi phê duyệt NCC
- **Chuẩn bị kiểm toán**: Chủ động phát hiện và khắc phục các thiếu sót

## Khi nào KHÔNG sử dụng

- **Kết luận pháp lý cuối cùng**: Skill chỉ cung cấp hướng dẫn; cần tư vấn
  thuế có chứng chỉ hành nghề cho kết luận pháp lý chính thức
- **Hóa đơn trước 2015**: Quy định khác; cần review chuyên biệt
- **Validate hóa đơn điện tử chuyên sâu** (mã CQT, tra cứu trên Cổng thuế,
  XML schema): dùng skill `accounting-einvoice`
- **Tờ khai hải quan / nhập khẩu**: Không phải nghiệp vụ kiểm tra hóa đơn

## Lưu ý về Hóa đơn điện tử (Tóm tắt)

Theo Thông tư 78/2021/TT-BTC (được sửa đổi bởi Thông tư 32/2025/TT-BTC),
hóa đơn điện tử có yêu cầu bổ sung:
- Mã CQT (mã xác thực từ cơ quan thuế) phải có
- XML hóa đơn phải tuân theo định dạng tại Thông tư 78/2021
- Đối với hóa đơn có mã CQT, có thể tra cứu trên Cổng thuế điện tử

Để validate HĐĐT chuyên sâu (mã CQT, parse XML, đối chiếu với CSDL cơ quan
thuế), dùng skill riêng `accounting-einvoice`.

---

## Đầu vào Bắt buộc

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `invoice_data` | object | Có | Các trường cốt lõi của hóa đơn |
| `invoice_date` | string | Có | Ngày phát hành hóa đơn (YYYY-MM-DD) |
| `seller_info` | object | Có | Thông tin người bán/đơn vị phát hành |
| `buyer_info` | object | Có | Thông tin người mua/đơn vị nhận |
| `line_items` | array | Có | Chi tiết các dòng hàng hóa/dịch vụ |
| `tax_breakdown` | object | Có | Phân tích thuế suất và số thuế |
| `total_amount` | number | Có | Tổng giá trị hóa đơn (VND) |

### Schema đầu vào

```typescript
interface InvoiceCheckInput {
  invoice_data: {
    invoice_number?: string;      // Số serial + số hóa đơn
    invoice_series?: string;       // Bắt buộc cho DN dùng ký hiệu
    payment_method?: string;       // cash|bank_transfer|combined
    adjustment_type?: string;       // Chỉ cho hóa đơn điều chỉnh
  };
  invoice_date: string;            // Chuỗi ngày ISO
  seller_info: {
    tax_code: string;              // MST 10 hoặc 13 số
    company_name: string;
    address: string;
    bank_account?: string;
    bank_name?: string;
  };
  buyer_info: {
    tax_code: string;
    company_name: string;
    address: string;
  };
  line_items: Array<{
    description: string;
    quantity: number;
    unit: string;
    unit_price: number;
    total: number;
    tax_rate?: number;             // 0, 5, 8, hoặc 10 (%)
  }>;
  tax_breakdown: {
    subtotal_ex_vat: number;
    total_vat: number;
    total_inclusive: number;
    vat_rates_applied: number[];
  };
  total_amount: number;
  // Chứng từ hỗ trợ (tùy chọn)
  supporting_docs?: {
    has_bank_transfer_proof?: boolean;
    has_contract?: boolean;
    has_delivery_note?: boolean;
    has_import_declaration?: boolean;
  };
}
```

---

## Quy trình Từng bước

### Bước 1: Xác minh loại hóa đơn

**Mục tiêu**: Xác nhận loại hóa đơn khớp với bản chất giao dịch.

1. Xác định đây là hóa đơn bán hàng/dịch vụ tiêu chuẩn hay hóa đơn điều chỉnh
2. Với hóa đơn điều chỉnh, kiểm tra:
   - Liên kết đến số và ngày hóa đơn gốc
   - Loại điều chỉnh thuộc một trong: sửa chữa, thay thế, giảm giá
   - Số tiền điều chỉnh nhất quán với loại điều chỉnh

**Cờ rủi ro**: Thiếu tham chiếu hóa đơn gốc cho hóa đơn điều chỉnh.

### Bước 2: Kiểm tra Trường Bắt buộc (Điều 10, NĐ 123/2020)

**Tham chiếu**: [Yêu cầu Hóa đơn](references/invoice-requirements.md)

Kiểm tra TẤT CẢ các trường bắt buộc theo Điều 10:

| Trường | Kiểm tra |
|--------|----------|
| Số serial + số hóa đơn | Bắt buộc, đúng định dạng |
| Ngày phát hành | Bắt buộc, ngày hợp lệ |
| Tên người bán | Bắt buộc, khớp đăng ký thuế |
| MST người bán | Bắt buộc, 10 hoặc 13 số |
| Địa chỉ người bán | Bắt buộc |
| Tên người mua | Bắt buộc |
| MST người mua | Bắt buộc |
| Địa chỉ người mua | Bắt buộc |
| Danh sách hàng hóa | Ít nhất 1 dòng |
| Đơn giá | Bắt buộc, > 0 |
| Tổng tiền | Bắt buộc, khớp tổng các dòng |
| Phân tích thuế | Bắt buộc nếu áp VAT |
| Phương thức thanh toán | Bắt buộc cho hóa đơn từ 20 triệu VND |

**Cờ rủi ro**: Mọi trường bắt buộc bị thiếu được flag với `severity: high`.

### Bước 3: Kiểm tra Thuế suất (Điều 9, Luật 48/2024/QH15)

**Thuế suất VAT hiện hành theo quy định**:

| Thuế suất | Phạm vi áp dụng |
|-----------|-----------------|
| 0% | Hàng hóa/dịch vụ thiết yếu (xuất khẩu, y tế, giáo dục, nông nghiệp) |
| 5% | Hàng hóa/dịch vụ thiết yếu (nước, y tế, giáo dục, vận tải, ...) |
| 8% | Thuế suất tiêu chuẩn (10% giảm xuống 8% theo Nghị định 174/2025/NĐ-CP, áp dụng đến 31/12/2026 cho hàng hóa/dịch vụ hiện đang chịu 10%) |
| 10% | Thuế suất mặc định — áp dụng cho hàng hóa/dịch vụ KHÔNG thuộc diện 0%, 5%, hoặc 8%; cũng áp dụng sau 31/12/2026 nếu Nghị định 174/2025 không được gia hạn |

**Các kiểm tra**:
1. Xác minh thuế suất thuộc một trong: 0%, 5%, 8%, hoặc 10% (theo Điều 9, Luật 48/2024/QH15)
2. Xác minh thuế suất khớp với loại hàng hóa/dịch vụ
3. Đối với hóa đơn từ 01/07/2025 đến 31/12/2026: xác minh 8% được áp dụng đúng cho hàng hóa/dịch vụ trước đây chịu 10%
4. Xác minh tính thuế: `số thuế = giá tính thuế × thuế suất`
5. Xác minh tờ khai VAT khớp với số liệu trên hóa đơn

**Ví dụ minh họa**:
```
Đầu vào: Tiền hàng = 1.000.000 VND, Thuế suất = 8%, VAT = 80.000 VND
Kiểm tra tính toán: 1.000.000 × 0,08 = 80.000 ✓
```

### Bước 4: Kiểm tra Thời điểm (Điều 9, NĐ 123/2020)

**Quy tắc thời điểm**:

| Loại giao dịch | Thời hạn |
|----------------|----------|
| Giao hàng hóa | Phát hành ngay khi giao hoặc trong ngày kết thúc giao hàng |
| Cung ứng dịch vụ | Phát hành khi hoàn thành dịch vụ hoặc nhận thanh toán |
| Xây dựng/lắp đặt | Phát hành khi nghiệm thu |
| Bán hàng thanh toán ngay | Phát hành tại điểm bán |
| Bán hàng trả chậm | Phát hành khi nhận thanh toán |

**Kiểm tra**:
1. Ngày hóa đơn không phải ngày tương lai
2. Ngày hóa đơn không trễ quá mức (> 30 ngày không có lý do)
3. Với hóa đơn điều chỉnh: ngày điều chỉnh phải sau ngày gốc

**Cờ rủi ro**: Hóa đơn ghi ngày tương lai là `severity: critical`. Hóa đơn
trễ quá 90 ngày là `severity: high`.

### Bước 5: Kiểm tra Chứng từ Hỗ trợ (Điều 14, TT 219/2013/TT-BTC)

**Yêu cầu chuyển khoản ngân hàng**: Đối với khấu trừ VAT đầu vào trên hóa
đơn từ 20.000.000 VND trở lên, BẮT BUỘC phải có chứng từ chuyển khoản.

| Giá trị | Chứng từ bắt buộc |
|---------|-------------------|
| < 20 triệu VND | Hóa đơn + chứng từ hỗ trợ khác (nếu có) |
| ≥ 20 triệu VND | Hóa đơn + chứng từ chuyển khoản ngân hàng |
| Thanh toán kết hợp | Phần tiền mặt có chứng từ, phần ngân hàng có xác nhận |

**Kiểm tra**:
1. Nếu tổng ≥ 20 triệu VND, xác minh `has_bank_transfer_proof: true`
2. Nếu thanh toán một phần qua ngân hàng, xác minh chứng từ tương ứng
3. Xác minh tài khoản ngân hàng trên hóa đơn khớp với giao dịch thực tế

**Cờ rủi ro**: Thiếu chứng từ chuyển khoản cho hóa đơn ≥ 20 triệu VND là
`severity: critical` đối với khấu trừ VAT đầu vào.

### Bước 6: Đánh giá Cờ Rủi ro

**Các cờ rủi ro phổ biến**:

| Cờ | Mức độ | Mô tả |
|----|--------|-------|
| `missing_mandatory_field` | High | Thiếu trường bắt buộc |
| `tax_rate_mismatch` | High | Thuế suất áp dụng không khớp loại hàng hóa |
| `calculation_error` | Critical | Sai lệch khi kiểm tra tính toán |
| `missing_bank_proof` | Critical | Hóa đơn ≥ 20 triệu VND không có chứng từ CK |
| `future_dated` | Critical | Ngày hóa đơn trong tương lai |
| `late_invoice` | Medium | Hóa đơn trễ > 30 ngày |
| `tax_code_invalid` | High | Định dạng MST không đúng |
| `unusual_amount` | Low | Số tiền bất thường ngoài phạm vi bình thường |
| `round_number` | Low | Tổng tiền tròn bất thường (cần xét đoán của con người) |
| `seller_buyer_same` | High | MST người bán và người mua trùng nhau |

### Bước 7: Sinh Kết quả

Sinh output có cấu trúc với các phát hiện và đánh giá rủi ro.

---

## Quy tắc Kiểm tra Dữ liệu

| Quy tắc | Mô tả | Hành động khi fail |
|---------|-------|---------------------|
| `invoice_number_format` | Phải có tiền tố serial + số | Flag `format_warning` |
| `tax_code_length` | 10 hoặc 13 số | Flag `invalid_tax_code` |
| `amount_positive` | Mọi số tiền > 0 | Flag `invalid_amount` |
| `tax_rate_valid` | Phải là 0, 5, 8, hoặc 10 | Flag `invalid_tax_rate` |
| `line_sum_matches` | Tổng dòng = subtotal khai báo | Flag `calculation_error` |
| `vat_calculation` | VAT = subtotal × thuế suất | Flag `calculation_error` |
| `total_matches` | Subtotal + VAT = tổng | Flag `calculation_error` |
| `date_valid` | Định dạng ISO, không phải tương lai | Flag `date_invalid` hoặc `future_dated` |

---

## Checklist Xác minh Pháp lý Việt Nam

### Nghị định 123/2020/NĐ-CP Điều 10 - Trường Bắt buộc

- [ ] Số serial và số thứ tự hóa đơn
- [ ] Họ tên, địa chỉ, MST người bán
- [ ] Họ tên, địa chỉ, MST người mua
- [ ] Ngày phát hành hóa đơn
- [ ] Tên, số lượng, đơn vị tính, đơn giá, tổng giá hàng hóa/dịch vụ
- [ ] Tổng giá trước VAT
- [ ] Thuế suất và số thuế VAT (nếu áp dụng)
- [ ] Tổng giá thanh toán

### Nghị định 123/2020/NĐ-CP Điều 9 - Thời điểm

- [ ] Hóa đơn phát hành tại thời điểm giao hàng/hoàn thành dịch vụ
- [ ] Không ghi ngày tương lai
- [ ] Không trễ bất hợp lý (> 90 ngày)

### Điều 14, Thông tư 219/2013/TT-BTC - VAT đầu vào

- [ ] Có chứng từ chuyển khoản cho hóa đơn ≥ 20.000.000 VND
- [ ] Tài khoản ngân hàng trên hóa đơn khớp với giao dịch thực tế

### Nghị định 174/2025/NĐ-CP - Giảm thuế suất VAT

- [ ] Hóa đơn phát hành 2025-2026 áp dụng thuế suất 8% tiêu chuẩn (không phải 10%)
- [ ] Xử lý chuyển tiếp đúng cho hóa đơn bao trùm ngày có hiệu lực

---

## Định dạng Đầu ra

```json
{
  "review_status": "pass" | "pass_with_warnings" | "fail",
  "summary": {
    "total_checks": 12,
    "passed": 10,
    "warnings": 1,
    "failures": 1
  },
  "mandatory_field_check": {
    "status": "complete" | "incomplete",
    "missing_fields": [],
    "present_fields": ["invoice_number", "invoice_date", "seller_name", "seller_tax_code", "seller_address", "buyer_name", "buyer_tax_code", "buyer_address", "line_items", "unit_price", "total", "vat_breakdown"]
  },
  "tax_calculation_check": {
    "status": "correct" | "incorrect" | "cannot_verify",
    "subtotal": 1000000,
    "declared_vat": 80000,
    "calculated_vat": 80000,
    "total": 1080000,
    "errors": []
  },
  "timing_check": {
    "status": "valid" | "late" | "future_dated" | "cannot_verify",
    "invoice_date": "2025-06-15",
    "issues": []
  },
  "supporting_docs_check": {
    "status": "complete" | "incomplete" | "not_required",
    "required_for_amount": true,
    "has_bank_proof": true,
    "missing_docs": []
  },
  "risk_flags": [
    {
      "flag": "missing_bank_proof",
      "severity": "critical",
      "description": "Hóa đơn vượt 20 triệu VND nhưng không có chứng từ chuyển khoản",
      "impact": "VAT đầu vào có thể không được khấu trừ cho hóa đơn này",
      "recommendation": "Yêu cầu cung cấp chứng từ chuyển khoản hoặc chứng minh thanh toán khác"
    }
  ],
  "recommendations": [
    "Yêu cầu người bán phát hành lại với đầy đủ trường bắt buộc",
    "Lấy chứng từ chuyển khoản để khấu trừ VAT đầu vào"
  ],
  "legal_disclaimer": "Đây là bản rà soát hướng dẫn. Cần tư vấn thuế có chứng chỉ để có kết luận chính thức về chi phí được trừ."
}
```

---

## Xử lý Dữ liệu Thiếu

| Trường thiếu | Mức độ | Xử lý |
|--------------|--------|-------|
| Số hóa đơn | High | Flag, không thể hoàn thành rà soát |
| Ngày hóa đơn | Critical | Flag, không thể hoàn thành rà soát |
| MST người bán | High | Flag, không thể đối chiếu với CSDL thuế |
| Danh sách hàng hóa | High | Flag, không thể kiểm tra tính thuế |
| Phân tích thuế | Medium | Flag nếu phải có VAT |
| Thông tin người mua | High | Flag, bắt buộc với hóa đơn B2B |

**Quy trình**:
1. Nếu trường `Critical` thiếu → trả `review_status: fail`, dừng kiểm tra tiếp
2. Nếu trường `High` thiếu → trả `review_status: fail`, ghi chú kiểm tra chưa hoàn thành
3. Nếu chỉ trường `Medium` thiếu → trả `review_status: pass_with_warnings`
4. Nếu trường ưu tiên thấp thiếu → ghi nhận thông tin bổ sung

---

## Xử lý Lỗi

### Lỗi Dữ liệu

| Lỗi | Phản hồi |
|-----|----------|
| Định dạng ngày không hợp lệ | Flag `date_invalid`, yêu cầu làm rõ |
| Số tiền không phải số | Flag `invalid_amount`, từ chối hóa đơn |
| Giá trị âm | Flag `invalid_amount`, từ chối hóa đơn |
| Số tiền vượt phạm vi hợp lý | Flag `unusual_amount`, escalate xem xét |

### Lỗi Xử lý

| Lỗi | Phản hồi |
|-----|----------|
| Thiếu đầu vào bắt buộc | Trả `review_status: fail`, liệt kê trường thiếu |
| Tràn số khi tính toán | Flag `calculation_error`, escalate |
| Định dạng đầu vào bất ngờ | Flag `format_warning`, cố gắng parse tốt nhất có thể |

---

## Quy tắc Chống Ảo giác (QUAN TRỌNG)

Các quy tắc này PHẢI được tuân thủ không ngoại lệ:

### Quy tắc 1: Không bao giờ kết luận hợp lệ

**SAI**: "Hóa đơn này hợp lệ và tuân thủ."
**ĐÚNG**: "Hóa đơn có vẻ đầy đủ dựa trên dữ liệu cung cấp. Tính hợp lệ chính
thức cần xác minh qua hệ thống cơ quan thuế."

### Quy tắc 2: Không bao giờ khẳng định khấu trừ được

**SAI**: "VAT trên hóa đơn này được khấu trừ."
**ĐÚNG**: "Số VAT được ghi nhận trên hóa đơn. Khả năng khấu trừ phụ thuộc
vào mục đích kinh doanh, chứng từ đầy đủ và chấp nhận của cơ quan thuế."

### Quy tắc 3: Không bao giờ bịa trích dẫn pháp lý

**SAI**: "Theo Điều 5, Thông tư 123..." (nếu Thông tư 123 không tồn tại)
**ĐÚNG**: Chỉ sử dụng trích dẫn đã xác minh từ văn bản pháp luật đã biết.
Nếu không chắc chắn, ghi "dựa trên hiểu biết chung về Nghị định 123/2020/NĐ-CP"
thay vì trích điều cụ thể.

### Quy tắc 4: Luôn kèm tuyên bố miễn trừ

**SAI**: Kết thúc rà soát mà không có disclaimer
**ĐÚNG**: Mọi đầu ra PHẢI bao gồm tuyên bố miễn trừ pháp lý

### Quy tắc 5: Không bao giờ thay thế phán đoán con người

**SAI**: "Hóa đơn này pass kiểm tra, không cần làm gì thêm."
**ĐÚNG**: "Hóa đơn vượt qua kiểm tra tự động. Quyết định cuối cùng cần do
nhân viên kế toán được ủy quyền đưa ra."

### Quy tắc 6: Trích dẫn chính xác nguồn

**SAI**: "Theo những thay đổi gần đây về luật VAT..."
**ĐÚNG**: "Theo Nghị định 174/2025/NĐ-CP, giảm thuế suất VAT tiêu chuẩn từ
10% xuống 8% có hiệu lực từ [ngày], thuế suất áp dụng có vẻ đúng cho hóa
đơn phát hành ngày [ngày]."

---

## Quy tắc Escalate

Escalate cho người xem xét khi:

| Điều kiện | Lý do | Ưu tiên |
|-----------|-------|---------|
| Phát hiện lỗi tính toán | Có thể là gian lận hoặc nhập liệu sai | High |
| Hóa đơn ghi ngày tương lai | Vấn đề tuân thủ tiềm ẩn | Critical |
| Thiếu chứng từ CK cho ≥ 20 triệu | Nguy cơ khấu trừ thuế | Critical |
| MST không hợp lệ | Người bán có thể không tồn tại | High |
| Giá trị > 1 tỷ VND | Cần rà soát giao dịch giá trị lớn | High |
| Mẫu hình hóa đơn trễ | Vấn đề quy trình hệ thống | Medium |
| Tất cả trường bắt buộc đều thiếu | Không thể thực hiện rà soát | Critical |
| Phát hiện dấu hiệu nghi ngờ | Gian lận tiềm ẩn | Critical |

---

## Tuyên bố Miễn trừ Pháp lý

**QUAN TRỌNG**: Skill này cung cấp rà soát tự động dựa trên phân tích dữ
liệu và quy định thuế Việt Nam được biết đến công khai. Skill này KHÔNG cấu
thành tư vấn pháp lý và KHÔNG nên được dùng làm căn cứ duy nhất cho quyết
định thuế.

**Giới hạn**:
- Kiểm tra tự động không thể xác minh tính xác thực với CSDL cơ quan thuế
- Skill không thể xác nhận tính hợp lý về mục đích kinh doanh
- Quyết định cuối cùng về khấu trừ thuế cần nhân viên thuế có thẩm quyền
- Quy định có thể thay đổi; xác minh luật hiện hành trước khi quyết định cuối

**Để có hướng dẫn chính thức**, tham khảo:
- Tổng cục Thuế (gdt.gov.vn)
- Tư vấn viên thuế được cấp phép tại Việt Nam
- Ấn phẩm chính thức của cơ quan thuế

**Văn bản tham chiếu** (tại ngày tạo skill):
- Nghị định 123/2020/NĐ-CP ngày 19/10/2020
- Luật 48/2024/QH15 (Luật Quản lý thuế) thông qua 21/11/2024
- Nghị định 174/2025/NĐ-CP ngày 01/01/2025
- Thông tư 219/2013/TT-BTC ngày 31/12/2013
- Thông tư 78/2021/TT-BTC ngày 17/08/2021
- Thông tư 32/2025/TT-BTC ngày 20/03/2025

---

*Cập nhật lần cuối: 2026-09-09*
*Phiên bản skill: 1.1.0*