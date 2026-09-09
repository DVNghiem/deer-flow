---
name: accounting-corporate-income-tax
description: >
  Tính toán và quyết toán thuế thu nhập doanh nghiệp (TNDN) theo Luật Thuế
  TNDN và các văn bản hướng dẫn. Trigger khi user cần: tính thuế TNDN tạm
  tính quý, lập tờ khai quyết toán thuế TNDN (mẫu 03/QTT-TNDN), xác định
  chi phí không được trừ, tính ưu đãi thuế, chuyển lỗ, hoặc bất kỳ nghiệp
  vụ nào liên quan đến thuế TNDN.
version: 1.0.0
domain: vietnam-accounting
tags:
  - accounting
  - vietnam
  - tax
  - corporate-income-tax
  - cit
---

# Accounting Corporate Income Tax Skill

## Purpose

Tính toán, tạm tính và quyết toán thuế thu nhập doanh nghiệp (TNDN) theo
quy định Việt Nam. Hỗ trợ xác định thu nhập chịu thuế, chi phí được trừ /
không được trừ, ưu đãi thuế, chuyển lỗ, và lập tờ khai.

> ⚠️ **Lưu ý quan trọng**: Luật Thuế TNDN hiện hành là Luật 67/2025/QH15
> (sửa đổi, có thể có hiệu lực từ kỳ tính thuế 2026). Trước đó là Luật
> 14/2008/QH13 (sửa đổi bổ sung bởi Luật 71/2014/QH13). **Cần xác minh
> luật hiện hành** trên Cổng thông tin điện tử Bộ Tài chính hoặc Tổng cục
> Thuế trước khi áp dụng.

**Legal Framework:**
- Luật Thuế TNDN (hiện hành tại thời điểm áp dụng — **xác minh phiên bản**)
- Nghị định 218/2013/NĐ-CP — Hướng dẫn thi hành Luật Thuế TNDN (và các
  NĐ sửa đổi bổ sung)
- Thông tư 78/2014/TT-BTC — Hướng dẫn về thuế TNDN (và các TT sửa đổi)
- Các văn bản hướng dẫn khác có liên quan

## When to Use

- Tính thuế TNDN tạm tính hàng quý
- Lập tờ khai quyết toán thuế TNDN (mẫu 03/QTT-TNDN)
- Xác định chi phí không được trừ khi tính thuế TNDN
- Tính thuế TNDN ưu đãi (giảm/miễn thuế theo lĩnh vực, địa bàn)
- Tính chuyển lỗ giữa các năm (tối đa 5 năm)
- Phân bổ thuế TNDN cho bên liên kết / liên doanh
- Hạch toán thuế TNDN vào sổ sách kế toán

## When NOT to Use

- Tính thuế giá trị gia tăng → dùng `accounting-tax-vat`
- Thuế thu nhập cá nhân → dùng `accounting-payroll` (TNCN là phần của payroll)
- Kê khai thuế nhà thầu nước ngoài → mẫu riêng, không thuộc CIT
- Thuế tài nguyên, thuế bảo vệ môi trường → các skill thuế chuyên ngành
- Tư vấn chuyển giá (transfer pricing) — phạm vi riêng, cần chuyên gia
- Quyết toán thuế TNDN cho doanh nghiệp có giao dịch liên kết phức tạp

## Required Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `tax_year` | object | Yes | `{ year, fiscal_year_start, fiscal_year_end }` |
| `company_info` | object | Yes | Tên DN, MST, ngành nghề, địa bàn hoạt động, loại hình DN |
| `financial_data` | object | Yes | DT, CP, lợi nhuận kế toán trước thuế |
| `deductible_expenses` | array | Yes | Danh sách chi phí (kèm loại: được trừ/không được trừ) |
| `non_deductible_items` | array | No | Các khoản chi phí không được trừ (nếu đã xác định) |
| `incentive_info` | object | No | Thông tin ưu đãi thuế (nếu có) |
| `loss_carryforward` | object | No | Thông tin lỗ các năm trước (nếu có) |
| `related_party_transactions` | array | No | Giao dịch liên kết (nếu có) |

---

## Thuế suất TNDN phổ biến (tham khảo)

> **Cần xác minh thuế suất hiện hành** tại thời điểm áp dụng. Các thuế suất
> dưới đây dựa trên Luật Thuế TNDN trước sửa đổi 2025.

| Thuế suất | Đối tượng áp dụng |
|-----------|-------------------|
| **20%** | Mặc định cho mọi DN |
| **17%** | DN nhỏ và vừa (DNNVV) — có thể đã thay đổi |
| **15%** | Thu nhập từ lĩnh vực ưu đãi đầu tư (giáo dục, y tế, KHCN, ...) |
| **10%** | Thu nhập từ dự án đầu tư mới trong lĩnh vực ưu đãi đặc biệt |
| **10%** | DNNVV thành lập mới trong lĩnh vực ưu đãi |
| **0%** | Một số trường hợp đặc biệt (cần GB) |

> ⚠️ Sau sửa đổi 2025, các thuế suất có thể đã thay đổi. Xác minh trên
> NĐ 218/2013/NĐ-CP (sửa đổi bổ sung) hoặc NĐ mới.

---

## Step-by-Step Workflow

### Bước 1: Xác định thu nhập chịu thuế (TNCT)

```
TNCT = (Doanh thu - Chi phí được trừ) + Thu nhập khác
     = Lợi nhuận kế toán trước thuế
     + Điều chỉnh tăng (chi phí không được trừ)
     - Điều chỉnh giảm (thu nhập không chịu thuế, ưu đãi)
```

### Bước 2: Xác định chi phí được trừ

Chi phí được trừ khi **đồng thời** thỏa mãn (theo NĐ 218/2013):
1. Phát sinh từ hoạt động SXKD thực tế của DN
2. Có đầy đủ hóa đơn, chứng từ hợp lệ
3. Không thuộc khoản chi không được trừ (xem Bước 3)

### Bước 3: Xác định chi phí KHÔNG được trừ

Một số nhóm chi phí không được trừ (tham khảo NĐ 218/2013, **cần xác minh
phiên bản hiện hành**):

| Nhóm | Ví dụ |
|------|-------|
| Không có HĐ hợp lệ | Chi phí > 20 triệu không có hóa đơn, không có chứng từ chuyển khoản |
| Phạt vi phạm | Phạt hành chính, phạt chậm nộp thuế |
| Bồi thường thiệt hại | Bồi thường do vi phạm hợp đồng |
| Tài trợ không hợp lệ | Tài trợ cho giáo dục/y tế không đúng quy định |
| Lãi vay vượt mức | Phần lãi vay vượt 3 lần vốn CSH (trong một số trường hợp) |
| CP quảng cáo tiếp khách | CP tiếp khách vượt 1 tỷ/năm → 15% phần vượt (cần xác minh) |
| Khấu hao không đúng quy định | KH TSCĐ vượt khung TT 45/2013 |
| Phần CP NLĐ không đóng BHXH | Phần lương không tham gia BHXH |
| Chi mua bảo hiểm nhân thọ | Một số trường hợp không được trừ |
| Lỗ chênh lệch tỷ giá chưa thực hiện | Phần chưa thực hiện trong một số trường hợp |

> ⚠️ Đây là danh sách tham khảo dựa trên NĐ 218/2013. **Cần đối chiếu với
> NĐ hiện hành** (có thể đã sửa đổi) và TT hướng dẫn chi tiết.

### Bước 4: Tính thuế TNDN phải nộp

```
Nếu TNCT > 0:
    Thuế TNDN = TNCT × Thuế suất áp dụng - Ưu đãi (nếu có)
Nếu TNCT ≤ 0:
    Thuế TNDN = 0 (lỗ được chuyển sang kỳ sau)
```

Trường hợp có nhiều mức thuế suất (do hoạt động ở nhiều lĩnh vực):
```
Thuế TNDN = Σ (Thu nhập theo từng mức × Thuế suất tương ứng)
```

### Bước 5: Xử lý chuyển lỗ

- Lỗ phát sinh trong kỳ tính thuế được chuyển sang các kỳ tiếp theo
- **Tối đa 5 năm** kể từ năm phát sinh lỗ
- Thời gian chuyển lỗ tính liên tục, không có năm dừng
- Lỗ chuyển đến hết thời hạn 5 năm mà chưa chuyển hết → hết hiệu lực
- Thứ tự chuyển lỗ: lỗ kỳ trước chuyển trước (FIFO)

### Bước 6: Tính ưu đãi thuế (nếu có)

Các hình thức ưu đãi:
1. **Thuế suất ưu đãi**: 10%, 15%, 17% (thay vì 20%)
2. **Miễn thuế**: 1-4 năm đầu (tùy dự án)
3. **Giảm 50% thuế**: tối đa 1-9 năm tiếp theo

Điều kiện: dự án thuộc lĩnh vực ưu đãi, địa bàn ưu đãi, hoặc DNNVV.

### Bước 7: Tính thuế tạm tính hàng quý

```
Thuế TNDN tạm tính quý = TNCT lũy kế đến cuối quý × Thuế suất
```

Quý I → Quý II (lũy kế) → Quý III (lũy kế) → Quý IV (lũy kế = cả năm)

Lưu ý: cuối năm quyết toán, nếu thuế thực tế > tạm tính → nộp thêm;
nếu thực tế < tạm tính → được khấu trừ vào kỳ sau hoặc hoàn.

### Bước 8: Hạch toán thuế TNDN

```
Nợ TK 8211    Chi phí thuế TNDN hiện hành
    Có TK 3334 Thuế TNDN phải nộp
```

Sau khi quyết toán:
- Nếu nộp thêm:
  ```
  Nợ TK 3334
      Có TK 1111/1121
  ```
- Nếu được khấu trừ (thuế tạm tính > thực tế):
  ```
  Nợ TK 3334
      Có TK 8211 (giảm CP thuế TNDN)
  ```

---

## Chi phí không được trừ — Chi tiết (NĐ 218/2013, cần xác minh hiện hành)

> ⚠️ Danh sách dưới đây mang tính tham khảo. **Một số khoản có thể đã được
> sửa đổi bổ sung**. Luôn xác minh với NĐ hiện hành trước khi áp dụng.

1. **Chi phí không có hóa đơn, chứng từ**:
   - Chi > 20 triệu/lần không có hóa đơn + chứng từ CK ngân hàng
   - Chi mua hàng hóa không có hóa đơn
   - Chi > 5 triệu/lần không có chứng từ

2. **Phạt vi phạm hành chính, vi phạm thuế**:
   - Phạt hành chính, phạt chậm nộp, phạt nộp chậm

3. **Bồi thường do vi phạm hợp đồng**:
   - Trừ khi đã tính vào giá sản phẩm

4. **Tài trợ**:
   - Tài trợ cho giáo dục, y tế, từ thiện không đúng quy định

5. **Chi phí khấu hao**:
   - Phần KH vượt khung TT 45/2013
   - KH TSCĐ không đưa vào sử dụng

6. **Chi phí tiếp khách, quảng cáo**:
   - CP tiếp khách vượt mức quy định
   - CP quảng cáo không có hóa đơn

7. **Lương, BHXH**:
   - Phần lương không tham gia BHXH (nếu pháp luật yêu cầu)
   - Lương cho chủ DN/người quản lý vượt mức quy định (trong một số TH)

8. **Lãi vay**:
   - Phần lãi vay vượt tỷ lệ quy định (liên quan đến giao dịch liên kết)

9. **Trích trước**:
   - Trích trước chi phí không đúng quy định

---

## Output Format

```json
{
  "skill": "accounting-corporate-income-tax",
  "version": "1.0.0",
  "tax_year": {
    "fiscal_year_start": "DD/MM/YYYY",
    "fiscal_year_end": "DD/MM/YYYY"
  },
  "company_info": { "name": "", "tax_code": "" },
  "step_1_taxable_income_calculation": {
    "accounting_profit_before_tax": 0,
    "adjustments_increase": 0,
    "adjustments_decrease": 0,
    "taxable_income": 0
  },
  "step_2_deductible_expenses": {
    "total_deductible": 0,
    "breakdown": []
  },
  "step_3_non_deductible_items": [
    {
      "category": "string",
      "amount": 0,
      "legal_reference": "string",
      "note": "string"
    }
  ],
  "step_4_cit_calculation": {
    "taxable_income": 0,
    "applicable_rate": 0,
    "incentive_reduction": 0,
    "cit_payable": 0
  },
  "step_5_loss_carryforward": {
    "losses_from_prior_years": [],
    "total_loss_used": 0,
    "remaining_loss_carryforward": 0
  },
  "step_6_tax_incentives": {
    "preferential_rate_applied": false,
    "tax_holiday_years_remaining": 0,
    "tax_reduction_period_remaining": 0
  },
  "step_7_quarterly_provisional_cit": [
    {
      "quarter": "Q1|Q2|Q3|Q4",
      "cumulative_taxable_income": 0,
      "cumulative_provisional_cit": 0,
      "quarter_cit_due": 0
    }
  ],
  "step_8_journal_entry": {
    "debit_account": "8211",
    "credit_account": "3334",
    "amount": 0,
    "legal_reference": "..."
  },
  "validation": {
    "taxable_income_positive": true,
    "rates_verified": true,
    "incentives_justified": true,
    "discrepancies": []
  },
  "flags": [],
  "disclaimer": "Tính toán thuế TNDN dựa trên dữ liệu user cung cấp. Kế toán trưởng và tư vấn thuế xác nhận trước khi nộp tờ khai chính thức."
}
```

---

## Anti-Hallucination Rules

### Rule 1: Không tự áp thuế suất

Luôn hỏi user về loại hình DN, lĩnh vực, địa bàn để xác định thuế suất áp
dụng. Mặc định **20%** chỉ khi user không cung cấp thông tin.

### Rule 2: Không tự đánh dấu "được trừ" / "không được trừ"

Mỗi khoản chi phí phải được đánh giá dựa trên đầy đủ thông tin:
- Có hóa đơn hợp lệ?
- Phát sinh từ hoạt động SXKD thực tế?
- Có thuộc danh mục không được trừ?

Không tự ý phân loại nếu thiếu thông tin → flag, yêu cầu user cung cấp.

### Rule 3: Không tự tính ưu đãi

Ưu đãi thuế có điều kiện cụ thể. Chỉ áp dụng khi user cung cấp:
- Giấy chứng nhận ưu đãi đầu tư
- Quyết định ưu đãi của cơ quan có thẩm quyền

Không tự đánh giá DN có được ưu đãi hay không.

### Rule 4: Trích dẫn cẩn thận

Các con số (thuế suất, mức khấu trừ) thay đổi theo thời gian. Luôn ghi rõ
"theo quy định hiện hành tại thời điểm..." và khuyến nghị xác minh.

### Rule 5: Không tự xác định chi phí không được trừ

Có hàng chục nhóm chi phí không được trừ. Không tự phân loại nếu không có
quy định rõ ràng tham chiếu. **Escalate cho tư vấn thuế** khi không chắc chắn.

---

## Escalation Rules

| Tình huống | Mức độ | Recipient |
|-----------|--------|-----------|
| DN có giao dịch liên kết phức tạp | HIGH | Tư vấn thuế chuyên transfer pricing |
| Áp dụng ưu đãi đầu tư không rõ ràng | HIGH | Kế toán trưởng + Tư vấn thuế |
| Chi phí không được trừ vượt 1 tỷ VND | HIGH | Kế toán trưởng |
| Lỗ chuyển sang kỳ sau vượt 5 năm | MEDIUM | Kế toán trưởng (kiểm tra hạn) |
| Lỗ > 50% vốn chủ sở hữu | HIGH | Kiểm toán viên |
| Hoạt động nhiều lĩnh vực, nhiều thuế suất | MEDIUM | Kế toán trưởng |
| Doanh thu > 200 tỷ VND | LOW | Kiểm tra thêm quyết toán nhóm |
| Có giao dịch với công ty nước ngoài | HIGH | Tư vấn thuế quốc tế |

---

## Legal Disclaimer

Skill này hỗ trợ tính toán thuế TNDN dự thảo dựa trên dữ liệu user cung
cấp. **Không thay thế tư vấn thuế chuyên nghiệp.** Luật Thuế TNDN và các
văn bản hướng dẫn có thể đã thay đổi sau khi skill được tạo. Kế toán trưởng
và tư vấn thuế phải xác minh:
- Luật Thuế TNDN hiện hành
- Nghị định hướng dẫn hiện hành (NĐ 218/2013 hoặc NĐ mới)
- Các thông tư hướng dẫn hiện hành
- Tờ khai quyết toán mẫu mới nhất (03/QTT-TNDN)

Tờ khai quyết toán thuế TNDN chính thức nộp cho cơ quan thuế phải được ký,
đóng dấu và nộp qua hệ thống thuế điện tử.