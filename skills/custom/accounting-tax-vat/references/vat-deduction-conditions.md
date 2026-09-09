# Tham chiếu Điều kiện Khấu trừ VAT Đầu vào

**Mục đích**: Hướng dẫn chi tiết về điều kiện khấu trừ VAT đầu vào theo quy định hiện hành
**Cập nhật lần cuối**: 2026-09-09
**Miễn trừ**: Tài liệu này chỉ mang tính tham khảo. Luôn xác minh với văn bản hiện hành.

---

## Tổng quan

Để được khấu trừ **VAT đầu vào** tại Việt Nam, hóa đơn phải đáp ứng **4 điều kiện bắt buộc** đồng thời. Thiếu một điều kiện → không được khấu trừ.

**Cơ sở pháp lý**:
- Luật 48/2024/QH15 (Luật Quản lý thuế)
- Luật Thuế GTGT 2024 (sửa đổi Luật 13/2008/QH12)
- Thông tư 219/2013/TT-BTC (hướng dẫn)
- Nghị định 100/2016/NĐ-CP (sửa đổi NĐ 51/2010 về thanh toán qua ngân hàng)
- Nghị định 123/2020/NĐ-CP (hóa đơn, chứng từ)

---

## Điều kiện 1: Phương thức Thanh toán (Quan trọng)

### Quy tắc Chung

**Theo Khoản 11, Điều 1, Nghị định 100/2016/NĐ-CP** (sửa đổi Nghị định 51/2010/NĐ-CP):

> Khi mua hàng hóa, dịch vụ từ 20 triệu VND trở lên phải có chứng từ
> thanh toán qua ngân hàng.

### Ngưỡng Áp dụng

| Giá trị hóa đơn | Phương thức thanh toán | Được khấu trừ |
|------------------|------------------------|---------------|
| < 20 triệu VND | Bất kỳ (có chứng từ) | Có |
| ≥ 20 triệu VND | Tiền mặt | **KHÔNG** |
| ≥ 20 triệu VND | Chuyển khoản ngân hàng | Có |
| ≥ 20 triệu VND | Kết hợp (tiền mặt + CK) | Có cho phần có chứng từ CK |

### Chứng từ Thanh toán Hợp lệ

| Loại chứng từ | Mô tả |
|---------------|--------|
| UNC (Ủy nhiệm chi) | Ủy nhiệm chi qua ngân hàng |
| Séc chuyển khoản | Séc không dùng tiền mặt |
| Giấy nộp tiền vào NSNN | Nếu thanh toán cho cơ quan nhà nước |
| Xác nhận internet banking | Kèm sao kê ngân hàng |
| Mobile banking | Có xác nhận giao dịch |

### Yêu cầu Chứng từ Thanh toán

Chứng từ phải ghi rõ:
1. **Ngày chuyển tiền**
2. **Số tiền chuyển** (khớp hóa đơn)
3. **Tài khoản NH người bán** (phải khớp với hóa đơn)
4. **Tài khoản NH người mua**
5. **Nội dung thanh toán** (tham chiếu hóa đơn)

### Trường hợp Đặc biệt

| Trường hợp | Cách xử lý |
|-----------|-----------|
| Thanh toán nhiều lần cho 1 hóa đơn | Cần đủ chứng từ cho mỗi lần CK |
| Thanh toán trước nhiều tháng | CK đầu tiên ≥ 20 triệu → cần chứng từ |
| Tổng nhiều hóa đơn ≥ 20 triệu (cùng NCC) | Từng hóa đơn riêng biệt, mỗi cái < 20 triệu được miễn |
| Thanh toán qua bên thứ ba | Không được khấu trừ (trừ trường hợp ủy thác) |
| Hàng hóa/dịch vụ nhập khẩu | Áp dụng quy định riêng về hải quan |

### Ví dụ Minh họa

```
Trường hợp 1: Hợp lệ
  Hóa đơn: 25.000.000 VND
  Thanh toán: CK 25.000.000 VND qua Vietcombank
  UNC: Có
  → Được khấu trừ

Trường hợp 2: Không hợp lệ
  Hóa đơn: 25.000.000 VND
  Thanh toán: Tiền mặt
  UNC: Không có
  → KHÔNG được khấu trừ

Trường hợp 3: Kết hợp
  Hóa đơn: 25.000.000 VND
  Thanh toán: 
    - Tiền mặt: 5.000.000
    - CK NH: 20.000.000
  UNC: Có (cho 20 triệu)
  → Được khấu trừ cho phần 20 triệu có CK
  → Phần 5 triệu tiền mặt: KHÔNG được khấu trừ
  → Tỷ lệ khấu trừ: 20/25 = 80%
```

---

## Điều kiện 2: Mục đích Kinh doanh

### Quy tắc Chung

Hàng hóa/dịch vụ mua vào phải **phục vụ hoạt động sản xuất kinh doanh chịu VAT** của doanh nghiệp.

### Phân loại

| Hoạt động | Được khấu trừ |
|-----------|---------------|
| Sản xuất hàng hóa chịu VAT | Có |
| Cung cấp dịch vụ chịu VAT | Có |
| Bán hàng hóa chịu VAT | Có |
| Xuất khẩu | Có |
| Hoạt động không chịu VAT | Không |
| Hoạt động miễn thuế | Không |
| Hoạt động tài chính, chuyển nhượng vốn | Không |

### Trường hợp Hỗn hợp (Có cả chịu và không chịu VAT)

**Theo Điều 10, Thông tư 219/2013/TT-BTC**:

Phải phân bổ VAT đầu vào theo tỷ lệ doanh thu:

```
VAT đầu vào được khấu trừ = Tổng VAT đầu vào × Tỷ lệ doanh thu chịu VAT / Tổng doanh thu
```

| Doanh thu chịu VAT | Doanh thu không chịu VAT | Tỷ lệ khấu trừ |
|--------------------|--------------------------|-----------------|
| 100% | 0% | 100% |
| 80% | 20% | 80% |
| 50% | 50% | 50% |
| 0% | 100% | 0% |

### Ví dụ Phân bổ

```
DN có:
  - Doanh thu bán hàng hóa (chịu VAT 8%): 800 triệu
  - Doanh thu cho thuê nhà (không chịu VAT): 200 triệu
  - Tổng doanh thu: 1 tỷ VND
  - VAT đầu vào phát sinh: 50 triệu VND

Tỷ lệ doanh thu chịu VAT = 800 / 1.000 = 80%
VAT đầu vào được khấu trừ = 50 triệu × 80% = 40 triệu VND
VAT đầu vào không được khấu trừ = 10 triệu VND (hạch toán vào chi phí)
```

---

## Điều kiện 3: Chứng từ Hợp lệ

### Yêu cầu Chứng từ

| Loại chứng từ | Yêu cầu |
|---------------|---------|
| Hóa đơn điện tử (HĐĐT) | Có mã CQT (cho B2B) |
| Hóa đơn giấy | Chỉ trong trường hợp đặc biệt (hiếm) |
| Đầy đủ trường bắt buộc | Theo Điều 10, NĐ 123/2020 |
| Ngày hóa đơn | Trong kỳ khai thuế hoặc kỳ trước liền kề |
| Tình trạng hóa đơn | Không bị hủy, thay thế, điều chỉnh sai |

### Hóa đơn Hợp lệ theo Nghị định 123/2020/NĐ-CP

Hóa đơn phải có:

**Trường bắt buộc**:
- Ký hiệu serial + số hóa đơn
- Ngày phát hành
- Tên, MST, địa chỉ người bán
- Tên, MST, địa chỉ người mua (cho B2B)
- Danh sách hàng hóa (tên, SL, đơn giá, thành tiền)
- Thuế suất + số thuế VAT
- Tổng thanh toán

### Hóa đơn Không Hợp lệ (Một số Trường hợp)

| Lỗi | Hậu quả |
|-----|---------|
| Thiếu MST người bán/mua | Không được khấu trừ |
| MST không tồn tại | Không được khấu trừ |
| Hóa đơn bị hủy | Không được khấu trừ |
| Hóa đơn đã thay thế | Hóa đơn cũ không được khấu trừ |
| Sai số tiền VAT | Có thể bị từ chối |
| Không có mã CQT (cho B2B) | Không được khấu trừ |
| Ngày hóa đơn không hợp lệ | Có thể bị từ chối |

---

## Điều kiện 4: Hàng hóa/Dịch vụ Thực tế Nhận được

### Quy tắc Chung

Hàng hóa/dịch vụ phải **thực sự được giao/cung cấp** và **sử dụng** cho hoạt động SXKD.

### Yêu cầu Chứng minh

| Bằng chứng | Mô tả |
|------------|--------|
| Biên bản giao hàng | Có chữ ký hai bên |
| Phiếu xuất kho | Từ người bán |
| Hợp đồng | Cho dịch vụ dài hạn |
| Nghiệm thu | Cho xây dựng, lắp đặt |
| Hóa đơn vận chuyển | Cho hàng hóa vận chuyển |

### Trường hợp Đặc biệt

| Trường hợp | Cách xử lý |
|-----------|-----------|
| Hàng hóa hư hỏng, mất mát | Không được khấu trừ VAT phần hư hỏng |
| Hàng thiếu không rõ nguyên nhân | Phải giảm trừ VAT đầu vào |
| Dịch vụ không sử dụng | Không được khấu trừ |
| Hàng hóa sử dụng sai mục đích | Phải giảm trừ VAT đã khấu trừ |

---

## Trường hợp KHÔNG Được Khấu trừ

Theo Điều 10, Nghị định 174/2025/NĐ-CP và các văn bản liên quan:

| Trường hợp | Hướng dẫn |
|-----------|-----------|
| Hàng hóa/dịch vụ cho hoạt động không chịu VAT | Hạch toán vào chi phí (bao gồm VAT) |
| Hàng hóa/dịch vụ cho hoạt động miễn thuế | Hạch toán vào chi phí (bao gồm VAT) |
| Chi phí không có hóa đơn hợp lệ | Hạch toán vào chi phí |
| Hóa đơn không hợp lệ | Hạch toán vào chi phí |
| Hàng thiếu không rõ nguyên nhân | Phải giảm trừ VAT đầu vào |
| VAT vượt mức khấu trừ cho ô tô | Theo quy định cụ thể |
| Tiền thuê nhà/điện/nước cho cá nhân | Hạch toán chi phí cá nhân |
| Chi phí quà tặng, hỗ trợ không SXKD | Hạch toán chi phí không được trừ |
| Phạt hành chính, tiền phạt | Không được khấu trừ |
| Chi phí tiếp khách vượt mức | Theo quy định cụ thể |

---

## Bảng Kiểm tra Xác minh

### Checklist cho Mỗi Hóa đơn Đầu vào

```
□ Hóa đơn đúng mẫu (Điều 10, NĐ 123/2020)
□ Hóa đơn có mã CQT (cho B2B)
□ MST người bán hợp lệ (10 số DN, 13 số CN)
□ MST người mua đúng DN đang kê khai
□ Đủ trường bắt buộc
□ Tính toán VAT đúng
□ Hàng hóa/dịch vụ thực tế nhận được
□ Mục đích: phục vụ SXKD chịu VAT
□ Phương thức thanh toán phù hợp:
   □ Nếu < 20 triệu: có chứng từ (tiền mặt/biên nhận OK)
   □ Nếu ≥ 20 triệu: CÓ chứng từ NH (UNC/séc CK)
□ Chứng từ thanh toán khớp hóa đơn
□ Ngày hóa đơn trong kỳ hoặc kỳ trước liền kề
□ Không bị hủy/thay thế/điều chỉnh sai
□ Hạch toán đúng TK 1331 (hoặc 133 theo TT 133)
```

### Xử lý Khi Một Trường Không Đạt

| Trường hợp | Xử lý |
|-----------|--------|
| Thiếu chứng từ NH (≥ 20 triệu) | Không khấu trừ, hạch toán vào chi phí |
| Hóa đơn không hợp lệ | Yêu cầu phát hành lại; nếu không được, không khấu trừ |
| Sai MST | Yêu cầu sửa hóa đơn; nếu không được, không khấu trừ |
| Hàng hóa sử dụng sai mục đích | Giảm trừ VAT đã khấu trừ |
| Hàng thiếu không rõ nguyên nhân | Giảm trừ VAT tương ứng |

---

## Ví dụ Tổng hợp

### Tình huống: Mua Hàng hóa cho SXKD

```
Hóa đơn: 50.000.000 VND (bao gồm VAT 8%)
  - Tiền hàng: 46.296.296 VND
  - VAT: 3.703.704 VND
Thanh toán: CK NH 50.000.000 VND
UNC: Có
Mục đích: Nguyên vật liệu SXKD
Hóa đơn: Có mã CQT, đủ trường bắt buộc

Kiểm tra:
  □ Điều kiện 1 (Thanh toán): ≥ 20 triệu, có UNC → Đạt
  □ Điều kiện 2 (Mục đích): SXKD → Đạt
  □ Điều kiện 3 (Chứng từ): Hợp lệ → Đạt
  □ Điều kiện 4 (Thực tế): Nhận được → Đạt

→ Được khấu trừ 3.703.704 VND
→ Bút toán:
  Nợ TK 152 (NVL): 46.296.296
  Nợ TK 1331 (VAT đầu vào): 3.703.704
    Có TK 1121 (Tiền gửi NH): 50.000.000
```

### Tình huống: Mua Hàng hóa nhưng Thiếu Chứng từ NH

```
Hóa đơn: 30.000.000 VND
Thanh toán: Tiền mặt 30.000.000 VND
UNC: Không có
Mục đích: SXKD

Kiểm tra:
  □ Điều kiện 1 (Thanh toán): ≥ 20 triệu, KHÔNG có UNC → KHÔNG đạt
  □ Điều kiện 2 (Mục đích): Đạt
  □ Điều kiện 3 (Chứng từ): Đạt
  □ Điều kiện 4 (Thực tế): Đạt

→ KHÔNG được khấu trừ
→ Hạch toán vào chi phí:
  Nợ TK 152 (NVL): 30.000.000 (bao gồm VAT)
    Có TK 1111 (Tiền mặt): 30.000.000
```

---

## Lỗi Thường Gặp

### Lỗi 1: Thanh toán Tiền mặt cho Hóa đơn ≥ 20 triệu

**Nguyên nhân**: Người mua thanh toán tiền mặt nhưng không có chứng từ NH.

**Hậu quả**: 
- Không được khấu trừ VAT
- Có thể bị phạt (nếu cơ quan thuế phát hiện)

**Cách tránh**:
- Luôn CK ngân hàng cho hóa đơn ≥ 20 triệu
- Nếu cần thanh toán tiền mặt, tách thành nhiều hóa đơn < 20 triệu (không khuyến khích)
- Lưu chứng từ NH cẩn thận

### Lỗi 2: Chứng từ NH Không Khớp Hóa đơn

**Nguyên nhân**: TK ngân hàng trên UNC khác với TK trên hóa đơn.

**Hậu quả**:
- Không được khấu trừ (có thể bị thách thức)
- Nghi ngờ thanh toán cho đối tượng khác

**Cách tránh**:
- TK trên hóa đơn và UNC phải khớp
- Nếu khác, cần giải trình (bên liên quan, ủy thác, ...)

### Lỗi 3: Phân bổ Sai Tỷ lệ

**Nguyên nhân**: DN có cả hoạt động chịu/không chịu VAT nhưng phân bổ sai.

**Hậu quả**:
- Khấu trừ quá mức → phải nộp bù + phạt
- Khấu trừ thiếu → không tận dụng ưu đãi

**Cách tránh**:
- Tính toán tỷ lệ mỗi năm (hoặc khi thay đổi lớn)
- Lưu hồ sơ tính toán
- Tư vấn thuế khi phức tạp

### Lỗi 4: Hóa đơn Trễ hoặc Hóa đơn Cũ

**Nguyên nhân**: Nhận hóa đơn sau nhiều tháng nhưng muốn khấu trừ.

**Hậu quả**:
- Phải kê khai bổ sung
- Có thể bị phạt (nếu qua hạn)

**Cách tránh**:
- Kiểm tra hóa đơn hàng tháng
- Kê khai trong kỳ gần nhất có thể

---

## Yêu cầu Lưu trữ Chứng từ

| Chứng từ | Thời gian lưu | Cơ sở pháp lý |
|----------|---------------|----------------|
| Hóa đơn đầu vào | 10 năm | Luật Kế toán 88/2015/QH13, Điều 15 |
| Chứng từ thanh toán NH | 10 năm | Luật Kế toán 88/2015/QH13 |
| Bảng kê hóa đơn | 10 năm | Luật Kế toán |
| Tờ khai thuế VAT | 10 năm | Luật Kế toán |
| Sổ sách kế toán liên quan | 10 năm | Luật Kế toán |

---

## Tài liệu Pháp luật Tham chiếu

### Quy định Chính

1. **Luật 48/2024/QH15** (21/11/2024) - Luật Quản lý thuế
   - Quy định chung về khấu trừ thuế

2. **Luật Thuế GTGT 2024** - Sửa đổi Luật 13/2008/QH12
   - Có hiệu lực từ 01/07/2025

3. **Nghị định 174/2025/NĐ-CP** (01/01/2025)
   - Giảm thuế suất VAT
   - Trường hợp không được khấu trừ (Điều 10)

4. **Nghị định 123/2020/NĐ-CP** (19/10/2020)
   - Yêu cầu về hóa đơn, chứng từ

### Quy định Hỗ trợ

5. **Thông tư 219/2013/TT-BTC** (31/12/2013)
   - Điều 10: Phân bổ VAT đầu vào
   - Điều 14: Điều kiện khấu trừ

6. **Thông tư 78/2021/TT-BTC** (17/08/2021)
   - Thủ tục quản lý thuế

7. **Nghị định 100/2016/NĐ-CP** (01/07/2016)
   - Sửa đổi NĐ 51/2010
   - Khoản 11, Điều 1: Yêu cầu CK NH cho hóa đơn ≥ 20 triệu

8. **Luật Kế toán 88/2015/QH13**
   - Điều 15: Thời hạn lưu trữ chứng từ (10 năm)

---

## Miễn trừ

**Tài liệu tham chiếu này chỉ cung cấp thông tin.**

Thông tin trong tài liệu phản ánh các quy định được biết đến công khai tính
đến ngày tạo skill. Pháp luật và quy định có thể thay đổi. Luôn xác minh với
công báo chính thức mới nhất và tham khảo tư vấn viên thuế có chứng chỉ để
có hướng dẫn chính thức.

Tài liệu này KHÔNG cấu thành tư vấn pháp lý hay thuế. Tác giả và cộng tác
viên không chịu trách nhiệm về bất kỳ quyết định nào được đưa ra dựa trên
thông tin này.

**Để có hướng dẫn chính thức**:
- Tổng cục Thuế: https://gdt.gov.vn
- Bộ Tài chính: https://mof.gov.vn

---

*Cập nhật lần cuối: 2026-09-09*