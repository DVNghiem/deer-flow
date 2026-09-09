# Tham chiếu Lỗi Hóa đơn Phổ biến

**Mục đích**: Nhận diện, phân loại và khắc phục các lỗi hóa đơn phổ biến
trong quá trình rà soát kế toán
**Cơ sở pháp lý**: Nghị định 123/2020/NĐ-CP, Thông tư 219/2013/TT-BTC
**Cập nhật lần cuối**: 2026-09-09
**Miễn trừ**: Tài liệu này chỉ mang tính tham khảo. Tham khảo văn bản hiện
hành và tư vấn thuế để có hướng dẫn chính thức.

---

## Khung Phân loại Lỗi

Lỗi được phân loại theo mức độ nghiêm trọng và ảnh hưởng đến:
- Tính đủ điều kiện khấu trừ VAT đầu vào
- Rủi ro kiểm toán của cơ quan thuế
- Tính chính xác của báo cáo tài chính

### Mức độ Nghiêm trọng

| Mức độ | Ảnh hưởng | Hành động yêu cầu |
|--------|-----------|---------------------|
| **Critical** | VAT đầu vào có thể không được khấu trừ; rủi ro phạt nặng | Sửa ngay hoặc escalate |
| **High** | Hóa đơn có thể bị từ chối; cờ kiểm toán | Yêu cầu phát hành lại hoặc bổ sung chứng từ |
| **Medium** | Vấn đề tuân thủ nhỏ | Ghi nhận và theo dõi |
| **Low** | Thông tin; không cần hành động ngay | Ghi vào ghi chú rà soát |

---

## Phần 1: Lỗi Nghiêm trọng (Critical)

### 1.1 Thiếu Chứng từ Chuyển khoản (≥ 20 triệu VND)

**Cơ sở pháp lý**: Điều 14, Thông tư 219/2013/TT-BTC

**Mô tả**:
Hóa đơn có tổng ≥ 20.000.000 VND nhưng không có chứng từ chuyển khoản
ngân hàng.

**Tiêu chí phát hiện**:
- `total_amount >= 20000000`
- `payment_method == 'cash'`
- `has_bank_transfer_proof == false`

**Ảnh hưởng**:
- VAT đầu vào không được khấu trừ (theo Điều 14 TT 219/2013/TT-BTC)
- Có thể bị cơ quan thuế điều tra
- Chi phí có thể không được trừ

**Hành động khắc phục**:

| Tình huống | Hành động |
|-----------|-----------|
| Thực tế đã thanh toán CK | Yêu cầu phát hành lại với CK NH hoặc lấy chứng từ thay thế |
| CK đã thực hiện nhưng thiếu chứng từ | Yêu cầu sao kê ngân hàng |
| Thanh toán < 20 triệu khi cộng nhiều hóa đơn | Tách hóa đơn; mỗi cái < 20 triệu riêng |
| Thanh toán kết hợp tiền mặt và CK | Ghi nhận riêng phần CK; tiền mặt ≤ 20 triệu |

**Ví dụ minh họa**:
```
Hóa đơn: 45.000.000 VND
Thanh toán: Tiền mặt
Thiếu chứng từ NH → Lỗi Critical

Các phương án khắc phục:
1. Lấy chứng từ chuyển khoản (nếu thực tế đã CK)
2. Yêu cầu xuất lại hóa đơn với phương thức thanh toán đúng
3. Ghi nhận lý do kinh doanh cho thanh toán tiền mặt (hiếm có ngoại lệ)
```

### 1.2 Hóa đơn ghi Ngày Tương lai

**Cơ sở pháp lý**: Điều 9, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Hóa đơn có ngày phát hành trong tương lai so với ngày hiện tại.

**Tiêu chí phát hiện**:
- `invoice_date > current_date`

**Ảnh hưởng**:
- Không tuân thủ yêu cầu thời điểm của NĐ 123/2020/NĐ-CP
- Có thể là dấu hiệu giao dịch ảo
- Không dùng để khấu trừ VAT đến khi đến ngày
- Rủi ro kiểm toán cao

**Hành động khắc phục**:
- Không xử lý; trả lại người phát hành để sửa
- Nếu nhận được với ngày tương lai, chờ đến ngày đó rồi xác minh lại
- Ghi nhận "Nhận sớm; không thể xử lý đến ngày [ngày]"

### 1.3 Lỗi Tính toán Số thuế

**Cơ sở pháp lý**: Điều 10, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Số thuế VAT không bằng giá tính thuế × thuế suất áp dụng.

**Tiêu chí phát hiện**:
- `calculated_vat != declared_vat`
- Trong đó: `calculated_vat = subtotal × vat_rate`

**Ví dụ minh họa**:
```
Tiền hàng: 10.000.000 VND
Thuế suất: 8%
VAT khai báo: 850.000 VND  ← SAI
VAT đúng: 800.000 VND

Mức độ: Critical
Ảnh hưởng: Hóa đơn có thể bị từ chối; yêu cầu phát hành lại
```

**Hành động khắc phục**:
- Yêu cầu phát hành lại với tính toán VAT chính xác
- Nếu nhận như vậy, escalate xem xét thủ công
- Ghi nhận chênh lệch cho kiểm toán

### 1.4 Thiếu Tất cả Trường Bắt buộc

**Mô tả**:
Hóa đơn thiếu thông tin cần thiết để xác định các bên hoặc xác minh giao dịch.

**Tiêu chí phát hiện**:
- Thiếu MST người bán VÀ tên người bán
- Thiếu hoàn toàn thông tin người mua
- Thiếu cả ngày VÀ số hóa đơn

**Ảnh hưởng**:
- Không thể xác định các bên giao dịch
- Không thể đối chiếu với hồ sơ thuế
- Hóa đơn không hợp lệ cho bất kỳ mục đích thuế nào

**Hành động khắc phục**:
- Từ chối hóa đơn; yêu cầu phát hành lại đầy đủ
- Escalate nếu phát hiện mẫu hình từ NCC

---

## Phần 2: Lỗi Mức độ Cao (High)

### 2.1 Thiếu Trường Bắt buộc

**Cơ sở pháp lý**: Điều 10, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Hóa đơn thiếu một hoặc nhiều trường bắt buộc theo Điều 10.

**Trường bắt buộc hay bị thiếu**:

| Trường | Tần suất | Mức độ |
|--------|----------|--------|
| MST người bán | Phổ biến | High |
| MST người mua | Phổ biến | High |
| Ngày hóa đơn | Ít phổ biến | High |
| Đơn giá | Ít phổ biến | High |
| Phân tích thuế | Trung bình | Medium |
| Phương thức thanh toán | Phổ biến cho < 20 triệu | Low-Medium |

**Ảnh hưởng**:
- Tùy trường: không tuân thủ một phần hoặc toàn bộ
- Cơ quan thuế có thể từ chối khi kiểm toán
- Khấu trừ VAT đầu vào có thể bị thách thức

**Hành động khắc phục**:
- Yêu cầu người bán phát hành lại với đủ trường
- Nếu NCC không sẵn lòng, ghi nhận lý do và escalate
- Đối với hóa đơn nội bộ: áp dụng validate trước khi phát hành

### 2.2 MST Không hợp lệ

**Cơ sở pháp lý**: Hệ thống Đăng ký MST (TNCN/TNDN)

**Mô tả**:
MST không đúng định dạng tiêu chuẩn Việt Nam.

**Định dạng hợp lệ**:

| Loại đối tượng | Định dạng | Ví dụ |
|-----------------|-----------|-------|
| Doanh nghiệp | 10 số | 0123456789 |
| Cá nhân | 13 ký tự (K + 12 số) | K123456789012 |
| Nước ngoài | Tùy thỏa thuận | Theo hiệp định |

**Tiêu chí phát hiện**:
- Không phải 10 số (tổ chức)
- Không phải 13 ký tự bắt đầu bằng K (cá nhân)
- Chứa ký tự không phải số (trừ tiền tố K)
- Checksum không hợp lệ

**Ảnh hưởng**:
- Không thể xác minh người bán/người mua tồn tại
- Không thể đối chiếu với hồ sơ thuế
- Có thể là đối tượng ảo

**Hành động khắc phục**:
- Yêu cầu người phát hành làm rõ
- Xác minh với giấy đăng ký kinh doanh
- Nếu xác minh fail, escalate cho thẩm tra

### 2.3 Thuế suất Không Khớp

**Cơ sở pháp lý**: Điều 9, Luật 48/2024/QH15; Nghị định 174/2025/NĐ-CP

**Mô tả**:
Thuế suất VAT áp dụng không khớp với yêu cầu theo nhóm hàng hóa/dịch vụ.

**Các trường hợp không khớp phổ biến**:

| Loại hàng | Thuế suất đúng | Thuế suất áp sai |
|-----------|----------------|------------------|
| Hàng tiêu chuẩn | 8% | 5% (thấp) hoặc 10% (cao) |
| Hàng thiết yếu | 5% | 8% (cao) |
| Xuất khẩu | 0% | 8% (cao) |

**Tiêu chí phát hiện**:
- Mô tả sản phẩm chỉ nhóm có thuế suất riêng
- Áp sai thuế suất so với nhóm khai báo
- Sau 2025: áp 10% (phải là 8%)

**Ảnh hưởng**:
- Tính thuế sai (nộp thừa/thiếu)
- Có thể trigger kiểm toán
- Cần sửa chữa và có thể yêu cầu hoàn thuế

**Hành động khắc phục**:
- Xác định thuế suất đúng theo nhóm sản phẩm
- Yêu cầu sửa hóa đơn
- Nếu thu quá: hoàn trả
- Nếu thu thiếu: nộp bù + có thể phạt

### 2.4 Phát hành Hóa đơn Trễ

**Cơ sở pháp lý**: Điều 9, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Hóa đơn được phát hành đáng kể sau khi giao hàng hoặc hoàn thành dịch vụ.

**Phân loại rủi ro**:

| Độ trễ | Mức độ | Mức rủi ro |
|--------|--------|-----------|
| 1-7 ngày | Low | Tối thiểu |
| 8-30 ngày | Medium | Trung bình |
| 31-90 ngày | High | Đáng kể |
| > 90 ngày | Critical | Rất cao |

**Ảnh hưởng**:
- Có thể chỉ ra giao dịch không xảy ra như khai
- Không tuân thủ yêu cầu thời điểm
- Cơ quan thuế soi xét kỹ

**Hành động khắc phục**:
- Yêu cầu giải trình bằng văn bản từ người phát hành
- Ghi nhận lý do kinh doanh cho việc trễ
- Với > 90 ngày: escalate BGĐ xem xét
- Cân nhắc từ chối và yêu cầu hóa đơn mới

### 2.5 Người bán và Người mua Cùng MST

**Cơ sở pháp lý**: Nguyên tắc thuế tổng quát; Thông tư 219/2013/TT-BTC

**Mô tả**:
Hóa đơn được phát hành khi MST người bán bằng MST người mua.

**Tiêu chí phát hiện**:
- `seller_info.tax_code == buyer_info.tax_code`

**Ảnh hưởng**:
- Giao dịch nội bộ không nên sinh chi phí được trừ
- Có thể là lỗi hồ sơ
- Có thể là gian lận nếu coi là giao dịch bên ngoài

**Hành động khắc phục**:
- Xác minh giao dịch có thực sự liên công ty không
- Nếu liên công ty: coi là chuyển nội bộ, không phải chi phí
- Nếu lỗi: yêu cầu sửa hóa đơn
- Escalate điều tra nếu không giải thích được

### 2.6 Sai Lệch Số tiền Hóa đơn

**Cơ sở pháp lý**: Điều 10, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Tổng khai báo không khớp với tổng các dòng.

**Các biến thể**:
- Tổng dòng ≠ subtotal khai báo
- Subtotal + VAT ≠ tổng khai báo
- Sai lệch do làm tròn

**Tiêu chí phát hiện**:
- `SUM(line_items.total) != tax_breakdown.subtotal_ex_vat`
- `subtotal + total_vat != total_amount`

**Ảnh hưởng**:
- Cho thấy lỗi tính toán
- Hóa đơn có thể bị từ chối
- Cần sửa chữa

**Ví dụ minh họa**:
```
Tổng các dòng: 9.950.000 VND
Subtotal khai báo: 10.000.000 VND
Chênh lệch: 50.000 VND

Mức độ: High
Hành động: Yêu cầu sửa hóa đơn
```

---

## Phần 3: Lỗi Mức độ Trung bình (Medium)

### 3.1 Thiếu Phương thức Thanh toán

**Cơ sở pháp lý**: Điều 10, Nghị định 123/2020/NĐ-CP; Điều 14, TT 219/2013/TT-BTC

**Mô tả**:
Hóa đơn không ghi phương thức thanh toán, đặc biệt quan trọng cho số
tiền ≥ 20 triệu VND.

**Ảnh hưởng**:
- Không thể xác minh tuân thủ yêu cầu CK NH
- Ít nghiêm trọng cho số nhỏ; quan trọng cho số lớn

**Hành động khắc phục**:
- Yêu cầu làm rõ
- Nếu ≥ 20 triệu: yêu cầu xác nhận phương thức + chứng từ

### 3.2 Tài khoản Ngân hàng Không Nhất quán

**Cơ sở pháp lý**: Điều 14, Thông tư 219/2013/TT-BTC

**Mô tả**:
Tài khoản ngân hàng trên hóa đơn khác với chứng từ CK thực tế.

**Ảnh hưởng**:
- Có thể là thanh toán cho đối tượng khác
- Gây nghi ngờ tính hợp lệ
- Khấu trừ VAT đầu vào có thể bị thách thức

**Hành động khắc phục**:
- Xác minh tài khoản CK thực tế
- Ghi nhận nếu liên quan công ty con / bên liên quan
- Escalate nếu không giải thích được

### 3.3 Lệch Dãy Số Hóa đơn

**Cơ sở pháp lý**: Nghị định 123/2020/NĐ-CP

**Mô tả**:
Lỗ hổng trong đánh số hóa đơn hoặc bất thường về dãy.

**Ảnh hưởng**:
- Có thể chỉ ra hóa đơn bị thiếu
- Trigger điều tra của cơ quan thuế
- Cần ghi nhận hóa đơn "voided"

**Hành động khắc phục**:
- Yêu cầu sổ hóa đơn voided
- Ghi nhận mọi lỗ hổng với giải thích
- Nếu lỗ hổng không giải thích được: escalate

### 3.4 Hóa đơn Điều chỉnh Thiếu Tham chiếu Gốc

**Cơ sở pháp lý**: Điều 11, Nghị định 123/2020/NĐ-CP

**Mô tả**:
Hóa đơn loại E (điều chỉnh) không tham chiếu hóa đơn C gốc.

**Ảnh hưởng**:
- Không thể xác minh tính hợp lệ của điều chỉnh
- Có thể là điều chỉnh trái phép
- Phá vỡ audit trail

**Hành động khắc phục**:
- Yêu cầu tham chiếu hóa đơn gốc
- Đối chiếu điều chỉnh với hóa đơn gốc
- Nếu từ chối: escalate

---

## Phần 4: Lỗi Mức độ Thấp (Low)

### 4.1 Vấn đề Định dạng Nhỏ

**Mô tả**:
Sai lệch định dạng không nghiêm trọng, không ảnh hưởng tuân thủ.

**Ví dụ**:
- Biến thể định dạng số ĐT
- Địa chỉ viết tắt khác nhau
- Khoảng cách tên công ty không nhất quán

**Ảnh hưởng**:
- Tối thiểu
- Có thể chỉ sự bất cẩn khi nhập liệu

**Hành động khắc phục**:
- Ghi nhận nếu cần tham chiếu tương lai
- Không cần hành động ngay
- Theo dõi mẫu hình

### 4.2 Chênh lệch Làm tròn

**Cơ sở pháp lý**: Thông lệ kế toán tiêu chuẩn

**Mô tả**:
Chênh lệch làm tròn nhỏ do phương pháp tính.

**Ví dụ minh họa**:
```
Đơn giá: 33.333,33 VND
Số lượng: 3
Tổng dòng: 99.999,99 VND

Có thể làm tròn thành 100.000 VND
Chênh lệch: 0,01 VND
```

**Ảnh hưởng**:
- Tối thiểu
- Tiêu chuẩn trong thương mại

**Hành động khắc phục**:
- Nếu tổng chênh lệch < 100 VND: ghi nhận và tiếp tục
- Nếu > 100 VND: yêu cầu làm rõ

### 4.3 Thiếu Trường Tùy chọn

**Mô tả**:
Trường tùy chọn (email, ĐT, tên liên hệ) không có thông tin.

**Ảnh hưởng**:
- Không ảnh hưởng tuân thủ
- Có thể gây khó cho liên lạc sau

**Hành động khắc phục**:
- Không yêu cầu
- Ghi nhận cho mục đích liên lạc tương lai

---

## Phần 5: Phát hiện Mẫu hình Rủi ro

### 5.1 Mẫu hình Khối lượng

| Mẫu hình | Mô tả | Rủi ro |
|---------|-------|--------|
| Cùng ngày hàng loạt | Nhiều hóa đơn cùng NCC, cùng ngày | Low-Medium |
| Số tiền tròn | Tất cả hóa đơn là số tròn | Medium |
| Cuối tuần/ngày lễ | Hóa đơn ghi ngày lễ | Medium |
| Cluster dãy số | Hóa đơn liên tiếp đều có cờ | Low |
| Cluster số tiền | Tất cả hóa đơn vừa dưới ngưỡng | Medium-High |

### 5.2 Mẫu hình NCC

| Mẫu hình | Mô tả | Rủi ro |
|---------|-------|--------|
| NCC mới | NCC mới đăng ký | Medium-High |
| Giao dịch đơn lẻ | Chỉ một hóa đơn từ NCC | Low |
| Bên liên quan | NCC là công ty con / công ty liên kết | Medium |
| Bất thường MST | Nhiều MST cho cùng tên | High |

### 5.3 Mẫu hình Thời điểm

| Mẫu hình | Mô tả | Rủi ro |
|---------|-------|--------|
| Tăng đột biến cuối quý | Khối lượng bất thường cuối quý | Medium |
| Tăng cuối năm | Khối lượng cao trong tháng 12 | Low |
| Sau hạn chót | Hóa đơn ngay trước hạn nộp tờ khai | Medium |

---

## Phần 6: Quy trình Khắc phục

### Quy trình cho Lỗi Critical/High

```
1. XÁC ĐỊNH
   └─> Đánh dấu lỗi với mức độ nghiêm trọng

2. ĐÁNH GIÁ
   ├─> Xác định có thể phát hành lại không
   ├─> Đánh giá ảnh hưởng đến vị thế thuế
   └─> Ước lượng công sức khắc phục

3. LIÊN HỆ
   ├─> Thông báo cho người phát hành về lỗi
   ├─> Cung cấp yêu cầu sửa cụ thể
   └─> Đặt hạn phản hồi

4. GIẢI QUYẾT
   ├─> Nhận hóa đơn đã sửa
   ├─> Xác minh sửa đổi
   └─> Cập nhật hồ sơ

5. GHI NHẬN
   ├─> Ghi lại lỗi ban đầu
   ├─> Ghi lại sửa đổi
   └─> Lưu cho audit trail

6. ESCALATE (nếu chưa giải quyết)
   └─> Thông báo BGĐ
   └─> Cân nhắc loại bỏ NCC
```

### Trigger Escalate

| Trigger | Escalate đến |
|---------|--------------|
| Bị từ chối phát hành lại | Trưởng phòng Tài chính |
| > 30 ngày chưa giải quyết | Giám đốc Tài chính |
| Mẫu hình lỗi từ NCC | Mua hàng + Giám đốc Tài chính |
| Nghi ngờ gian lận | Giám đốc Tài chính + Pháp chế |
| Số tiền > 100 triệu VND có lỗi | Giám đốc Tài chính + CFO |

---

## Phần 7: Thống kê Lỗi Tham chiếu

### Tần suất Lỗi Phổ biến (Dữ liệu minh họa)

Dựa trên kinh nghiệm rà soát kế toán:

| Loại lỗi | Tần suất | % Tổng số |
|----------|----------|-----------|
| Thiếu chứng từ NH | 15% | Phổ biến nhất critical |
| Thiếu trường bắt buộc | 12% | Phổ biến |
| Lỗi tính toán | 5% | Ít phổ biến |
| MST không hợp lệ | 3% | Ít phổ biến |
| Vấn đề thời điểm | 8% | Phổ biến |
| Khác | 57% | Đa dạng |

---

## Checklist Tóm tắt

### Trước khi Đánh dấu Lỗi

- [ ] Xác minh dữ liệu đầu vào chính xác
- [ ] Kiểm tra lỗi nhập liệu phía mình
- [ ] Xác nhận cách hiểu yêu cầu
- [ ] Kiểm tra ngoại lệ đã biết

### Khi Đánh dấu Lỗi

- [ ] Gán mức độ nghiêm trọng đúng
- [ ] Cung cấp khuyến nghị cụ thể
- [ ] Tham chiếu quy định áp dụng
- [ ] Bao gồm phát biểu ảnh hưởng
- [ ] Đặt hành động yêu cầu

### Khi Escalate

- [ ] Ghi nhận mọi nỗ lực giải quyết
- [ ] Cung cấp đầy đủ chứng từ
- [ ] Nêu ảnh hưởng kinh doanh
- [ ] Khuyến nghị tiêu chí quyết định

---

## Miễn trừ

**Tài liệu tham chiếu này chỉ cung cấp thông tin.**

Phân loại lỗi và mức độ nghiêm trọng trong tài liệu này đại diện cho hướng
dẫn chung dựa trên các quy định được biết đến công khai. Cách diễn giải
quy định có thể thay đổi. Luôn tham khảo văn bản hiện hành và chuyên gia
thuế có chứng chỉ để có hướng dẫn chính thức cho tình huống cụ thể.

Tài liệu này KHÔNG cấu thành tư vấn pháp lý hay thuế. Tác giả và cộng tác
viên không chịu trách nhiệm về bất kỳ quyết định nào được đưa ra dựa trên
thông tin này.

**Để có hướng dẫn chính thức**:
- Tổng cục Thuế: https://gdt.gov.vn
- Bộ Tài chính: https://mof.gov.vn
- Tư vấn viên thuế được cấp phép tại Việt Nam

---

*Cập nhật lần cuối: 2026-09-09*