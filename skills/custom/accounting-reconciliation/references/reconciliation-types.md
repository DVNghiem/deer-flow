# Tham chiếu Các Loại Đối chiếu

**Mục đích**: Hướng dẫn chi tiết về các loại đối chiếu sổ sách kế toán Việt Nam
**Cập nhật lần cuối**: 2026-09-09
**Miễn trừ**: Tài liệu này chỉ mang tính tham khảo. Luôn xác minh với văn bản hiện hành.

---

## Tổng quan

Tài liệu này cung cấp hướng dẫn chi tiết cho **6 loại đối chiếu** phổ biến
trong kế toán doanh nghiệp Việt Nam:

1. Đối chiếu Ngân hàng (TK 1121/1122)
2. Đối chiếu Công nợ Phải trả (TK 331)
3. Đối chiếu Công nợ Phải thu (TK 131)
4. Đối chiếu Tồn kho (TK 151/152/153/154/155/156)
5. Đối chiếu Tài sản cố định (TK 211/213/214/241)
6. Đối chiếu Liên công ty (Intercompany)

**Cơ sở pháp lý**:
- Thông tư 200/2014/TT-BTC (Chế độ kế toán DN)
- Thông tư 99/2025/TT-BTC (Chế độ kế toán mới, có hiệu lực 01/01/2026)
- Thông tư 133/2016/TT-BTC (Chế độ kế toán DNVVN)
- Luật Kế toán 88/2015/QH13

---

## 1. Đối chiếu Ngân hàng (TK 1121/1122)

### Mục tiêu

Đối chiếu sổ tiền gửi ngân hàng (TK 1121 VND, TK 1122 ngoại tệ) với sao kê
ngân hàng để xác nhận:
- Số dư thực tế tại ngân hàng
- Các giao dịch đã phát sinh nhưng chưa ghi nhận
- Phí ngân hàng, lãi tiền gửi
- Chênh lệch tỷ giá (với TK 1122)

### Tài khoản Liên quan

| TK | Tên | Loại tiền |
|----|-----|-----------|
| 1121 | Tiền gửi ngân hàng (VND) | Việt Nam Đồng |
| 1122 | Tiền gửi ngân hàng (ngoại tệ) | USD, EUR, JPY, ... |
| 1123 | Tiền đang chuyển (chuyển tiền chưa đến NH) | VND |
| 1128 | Tiền gửi ngân hàng (khác) | VND |

### Chứng từ Cần Chuẩn bị

| Chứng từ | Mô tả |
|----------|--------|
| Sổ tiền (Cash Book) | Sổ kế toán nội bộ theo dõi biến động TK 1121 |
| Sao kê ngân hàng | Do ngân hàng cung cấp (cuối kỳ) |
| UNC / Séc / Giấy nộp tiền | Chứng từ gốc cho mỗi giao dịch |
| Bảng sao kê trực tuyến | Từ internet banking (nếu có) |
| Hợp đồng tín dụng | Cho TK có thế chấp, bảo lãnh |

### Quy trình Đối chiếu

#### Bước 1: Lấy số liệu

1. Lấy số dư sổ cái TK 1121/1122 tại ngày đối chiếu
2. Lấy số dư sao kê ngân hàng cùng ngày
3. Tính chênh lệch ban đầu

#### Bước 2: Khớp giao dịch

Khớp từng giao dịch theo:
- **Số tham chiếu** (số UNC, số séc)
- **Số tiền** (cho phép sai lệch trong tolerance)
- **Ngày giao dịch**
- **Nội dung** (memo/description)

#### Bước 3: Phân loại giao dịch chưa khớp

| Loại | Mô tả |
|------|--------|
| **Outstanding cheques** | Séc đã ký, đã ghi sổ nhưng chưa đến NH |
| **Deposits in transit** | Tiền đã gửi vào NH nhưng chưa ghi sổ |
| **Phí NH chưa ghi** | Phí NH chưa được ghi nhận trong sổ |
| **Lãi NH chưa ghi** | Lãi tiền gửi chưa ghi nhận |
| **Chênh lệch tỷ giá** | Cho TK 1122 (ngoại tệ) |
| **Ghi nhầm** | Nhầm TK, nhầm số tiền |

#### Bước 4: Lập Bảng Đối chiếu Ngân hàng

```
Số dư sổ tiền nội bộ (TK 1121):                XXX
Cộng: Thu từ NH chưa ghi sổ                    + A
Trừ: Chi từ sổ tiền chưa thanh toán            - B
Cộng: Lãi NH chưa ghi nhận                     + C
Trừ: Phí NH chưa ghi nhận                      - D
+/- Điều chỉnh sai lệch                        ± E
                                             ------
Số dư theo sao kê NH:                          YYY (phải khớp)
```

#### Bước 5: Xử lý Chênh lệch

| Tình huống | Xử lý |
|-----------|--------|
| Séc chưa thanh toán | Ghi vào "Chi chưa thanh toán"; theo dõi |
| Tiền trong đường | Ghi vào "Thu chưa ghi"; theo dõi |
| Phí NH | Ghi nhận: Nợ TK 642 / Có TK 1121 |
| Lãi NH | Ghi nhận: Nợ TK 1121 / Có TK 515 |
| Sai TK | Điều chỉnh bút toán |

### Bút toán Điều chỉnh Thường Gặp

**Phí ngân hàng**:
```
Nợ TK 642      Chi phí quản lý doanh nghiệp
    Có TK 1121     Tiền gửi ngân hàng (giảm)
```

**Lãi tiền gửi**:
```
Nợ TK 1121      Tiền gửi ngân hàng (tăng)
    Có TK 515      Doanh thu hoạt động tài chính
```

**Chênh lệch tỷ giá (TK 1122)**:
```
Nợ/Có TK 1122    Tiền gửi (ngoại tệ)
    Có/Nợ TK 4131    Chênh lệch tỷ giá đã thực hiện
    Có/Nợ TK 4132    Chênh lệch tỷ giá chưa thực hiện
```

**Tiền đang chuyển (TK 1123)**:
```
Nợ TK 1123       Tiền đang chuyển
    Có TK 1121        Tiền gửi ngân hàng (trước khi chuyển)

Khi NH xác nhận:
Nợ TK 1121 (NH đích)
    Có TK 1123         Tiền đang chuyển
```

### Tần suất Đối chiếu

| Loại TK | Tần suất khuyến nghị |
|---------|----------------------|
| TK 1121 (VND) - tài khoản chính | Hàng ngày hoặc mỗi khi có giao dịch lớn |
| TK 1121 - tài khoản phụ | Hàng tuần / hàng tháng |
| TK 1122 (ngoại tệ) | Hàng tháng (kèm đánh giá lại tỷ giá) |
| TK 1123 (tiền đang chuyển) | Theo dõi liên tục |

### Lưu ý Đặc biệt

- **Nghỉ lễ, cuối tuần**: Giao dịch có thể chậm 1-2 ngày
- **Số dư âm**: Báo hiệu thấu chi → kiểm tra hạn mức
- **Séc quá hạn (> 6 tháng)**: Cần xử lý theo TT 200 hoặc 99

---

## 2. Đối chiếu Công nợ Phải trả (TK 331)

### Mục tiêu

Xác nhận số dư TK 331 với từng nhà cung cấp tại ngày đối chiếu:
- Số dư phải trả đúng thực tế
- Phát hiện giao dịch ghi thiếu/ghi thừa
- Xác nhận các khoản nợ đến hạn, quá hạn
- Phục vụ quản lý dòng tiền

### Tài khoản Liên quan

| TK | Tên | Mô tả |
|----|-----|-------|
| 331 | Phải trả cho người bán | Tổng hợp |
| 3311 | Phải trả cho người bán (ngắn hạn) | < 12 tháng |
| 3312 | Phải trả cho người bán (dài hạn) | > 12 tháng |
| 3318 | Phải trả khác | Các khoản phải trả khác |

### Chứng từ Cần Chuẩn bị

| Chứng từ | Mô tả |
|----------|--------|
| Sổ chi tiết TK 331 theo NCC | Từ hệ thống kế toán |
| Bảng sao kê công nợ của NCC | Confirmation letter / Statement |
| Hợp đồng mua hàng | Hợp đồng đang có hiệu lực |
| Hóa đơn mua vào chưa thanh toán | Danh sách hóa đơn |
| Biên bản đối chiếu công nợ | Có chữ ký hai bên |

### Quy trình Đối chiếu

#### Bước 1: Lập sổ chi tiết theo NCC

Cho mỗi NCC, lập bảng:

| Ngày | Số CT | Diễn giải | Nợ (giảm) | Có (tăng) | Số dư |
|------|--------|-----------|-----------|-----------|--------|
| 01/01 | | Số dư đầu kỳ | | | 100.000.000 |
| 15/01 | UNC-001 | Thanh toán | 50.000.000 | | 50.000.000 |
| 20/01 | HĐ-1234 | Mua hàng | | 30.000.000 | 80.000.000 |

#### Bước 2: Yêu cầu xác nhận công nợ

Gửi thư xác nhận công nợ cho mỗi NCC (ưu tiên NCC có số dư lớn):
- Mẫu thư xác nhận
- Bảng kê chi tiết công nợ
- Yêu cầu xác nhận trong 15-30 ngày

#### Bước 3: Đối chiếu với bên ngoài

So sánh số dư nội bộ với bên ngoài:

| Số dư theo DN | Số dư theo NCC | Chênh lệch |
|---------------|----------------|------------|
| 100.000.000 | 100.000.000 | 0 |
| 100.000.000 | 95.000.000 | 5.000.000 |

#### Bước 4: Phân tích chênh lệch

| Nguyên nhân | Cách xử lý |
|-----------|-----------|
| Hàng chưa nhận nhưng đã ghi nợ | Điều chỉnh giảm |
| Hàng nhận chưa có hóa đơn | Ghi nhận bổ sung (hàng về, chưa có HĐ) |
| HĐ cuối tháng chưa nhận | Đợi HĐ; theo dõi |
| NCC ghi thiếu | Gửi bảng đối chiếu yêu cầu kiểm tra lại |
| Chênh lệch tỷ giá | Đánh giá lại |

#### Bước 5: Lập bảng đối chiếu chính thức

Bảng đối chiếu có chữ ký của cả hai bên:
- Cột bên trong (theo sổ sách DN)
- Cột bên ngoài (theo NCC)
- Cột chênh lệch
- Cột xác nhận

### Lập báo cáo Tuổi nợ AP (Aging Report)

| Nhóm tuổi nợ | Mô tả | Ngày |
|---------------|--------|------|
| Chưa đến hạn | < ngày đến hạn | T+0 đến T+30 |
| Đến hạn | Đang trong hạn thanh toán | T+30 đến T+60 |
| Quá hạn 1-30 ngày | | T+60 đến T+90 |
| Quá hạn 31-60 ngày | | T+90 đến T+120 |
| Quá hạn 61-90 ngày | | T+120 đến T+150 |
| Quá hạn > 90 ngày | Cần xử lý đặc biệt | > T+150 |

### Bút toán Điều chỉnh

**Hàng về trước, hóa đơn đến sau**:
```
Nợ TK 151      Hàng mua đang đi đường
    Có TK 331       Phải trả người bán (tạm ứng)

Khi có hóa đơn:
Nợ TK 152/153/155/156 (NVL/CC/TP/HH)
Nợ TK 1331 (VAT đầu vào)
    Có TK 151       Hàng mua đang đi đường
    Có TK 331       Phải trả người bán
```

**Chiết khấu thanh toán nhận được**:
```
Nợ TK 331       Phải trả người bán (giảm)
    Có TK 515       Doanh thu hoạt động tài chính
    Có TK 711       Thu nhập khác
```

---

## 3. Đối chiếu Công nợ Phải thu (TK 131)

### Mục tiêu

Xác nhận số dư TK 131 với từng khách hàng:
- Số dư phải thu đúng thực tế
- Phát hiện nợ khó đòi
- Trích lập dự phòng nợ phải thu khó đòi
- Hỗ trợ quản lý dòng tiền thu

### Tài khoản Liên quan

| TK | Tên | Mô tả |
|----|-----|-------|
| 131 | Phải thu khách hàng | Tổng hợp |
| 1311 | Phải thu khách hàng (ngắn hạn) | < 12 tháng |
| 1312 | Phải thu khách hàng (dài hạn) | > 12 tháng |
| 1318 | Phải thu khác | Các khoản phải thu khác |
| 2293 | Dự phòng phải thu khó đòi | Dự phòng |

### Quy trình Đối chiếu

#### Bước 1: Lập sổ chi tiết theo khách hàng

Tương tự AP, lập sổ chi tiết cho mỗi khách hàng.

#### Bước 2: Gửi xác nhận công nợ

| Nhóm KH | Tần suất gửi xác nhận |
|---------|----------------------|
| KH chiến lược (số dư lớn) | Mỗi tháng |
| KH thường xuyên | Mỗi quý |
| KH ít giao dịch | Mỗi năm (cuối năm) |

#### Bước 3: Phân tích tuổi nợ AR

| Nhóm tuổi nợ | Mô tả | Xử lý |
|---------------|--------|--------|
| < 30 ngày | Bình thường | Tiếp tục theo dõi |
| 30-60 ngày | Cần nhắc | Gửi email nhắc nợ |
| 60-90 ngày | Quá hạn nhẹ | Gọi điện nhắc |
| 90-180 ngày | Quá hạn nặng | Escalate lên quản lý |
| > 180 ngày | Nghi ngờ khó đòi | Cân nhắc trích lập DPPTKĐ |

#### Bước 4: Trích lập Dự phòng Nợ phải thu Khó đòi

Theo Thông tư 48/2019/TT-BTC (cho DN đã áp dụng TT 200):

| Thời gian quá hạn | Mức trích dự phòng |
|--------------------|---------------------|
| Từ 6 tháng đến dưới 1 năm | 30% |
| Từ 1 năm đến dưới 2 năm | 50% |
| Từ 2 năm đến dưới 3 năm | 70% |
| Từ 3 năm trở lên | 100% |

**Bút toán trích lập**:
```
Nợ TK 642      Chi phí quản lý doanh nghiệp
    Có TK 2293    Dự phòng phải thu khó đòi
```

**Khi xác định là nợ khó đòi**:
```
Nợ TK 2293     Dự phòng phải thu khó đòi
Nợ TK 811      Chi phí khác (nếu thiếu dự phòng)
    Có TK 131       Phải thu khách hàng
```

### Báo cáo Xác nhận Công nợ

Mẫu thư xác nhận công nợ:

```
Kính gửi: [Tên khách hàng]
Đề: Yêu cầu xác nhận số dư công nợ tại ngày 31/12/2025

Kính thưa Quý Công ty,

Theo quy định kế toán, chúng tôi trân trọng đề nghị Quý Công ty xác nhận
số dư công nợ phải thu tại ngày 31/12/2025 như sau:

Theo sổ sách của chúng tôi: X.XXX.XXX.XXX VNĐ (bằng chữ: ...)

Đề nghị Quý Công ty kiểm tra và xác nhận bằng văn bản trong vòng 15 ngày.
Nếu có chênh lệch, vui lòng nêu rõ.

Trân trọng,
[Chữ ký Kế toán trưởng]
```

---

## 4. Đối chiếu Tồn kho (TK 151/152/153/154/155/156)

### Mục tiêu

Đối chiếu số liệu tồn kho giữa:
- Sổ cái kế toán (TK 151-156)
- Sổ chi tiết vật tư/thành phẩm (theo mã hàng)
- Thẻ kho (theo kho vật lý)
- Kiểm kê thực tế (nếu có)

### Tài khoản Liên quan

| TK | Tên | Loại hàng hóa |
|----|-----|---------------|
| 151 | Hàng mua đang đi đường | Hàng chưa về kho |
| 152 | Nguyên vật liệu | NVL cho SX |
| 153 | Công cụ, dụng cụ | CCDC < tiêu chuẩn TSCĐ |
| 154 | Chi phí SXKD dở dang | CPSX dở dang |
| 155 | Thành phẩm | TP từ SX |
| 156 | Hàng hóa | HH mua về để bán |

### Quy trình Đối chiếu

#### Bước 1: Lấy số liệu tồn kho

| Nguồn | Chứng từ |
|--------|----------|
| Sổ cái | Sổ cái TK 151-156 |
| Sổ chi tiết | Sổ chi tiết NVL/TP/HH theo mã |
| Thẻ kho | Thẻ kho từng mặt hàng |
| Kho vật lý | Kiểm kê thực tế |

#### Bước 2: So sánh

So sánh tồn kho cuối kỳ giữa:
- Sổ sách kế toán (TK tổng hợp)
- Sổ chi tiết (theo mã hàng)
- Thẻ kho (theo lô/vị trí)
- Kiểm kê thực tế (nếu có)

#### Bước 3: Phân tích chênh lệch

| Loại chênh lệch | Nguyên nhân | Xử lý |
|------------------|------------|--------|
| Sổ cái ≠ Sổ chi tiết | Lỗi ghi sổ, nhầm TK | Điều chỉnh |
| Sổ chi tiết ≠ Thẻ kho | Lỗi nhập/xuất kho | Điều chỉnh thẻ kho |
| Sổ sách ≠ Kiểm kê | Thừa/thiếu do nhiều nguyên nhân | Dùng skill `accounting-stocktake` |

#### Bước 4: Nguyên nhân Chênh lệch Thường Gặp

| Nguyên nhân | Mô tả |
|------------|--------|
| Xuất kho không ghi sổ | NVL đã dùng nhưng chưa ghi giảm tồn |
| Nhập kho không ghi sổ | Hàng đã về nhưng chưa ghi nhận |
| Chuyển kho chưa ghi | Hàng chuyển từ kho A → kho B chưa cập nhật |
| Hàng hỏng, mất | Cần xử lý riêng |
| Sai số đo lường | Đơn vị tính không thống nhất |
| Lỗi nhập/xuất giá | Sai đơn giá, sai số lượng |

### Phương pháp Tính Giá Tồn kho

Theo TT 200/2014/TT-BTC (và TT 99/2025 từ 01/01/2026):

| Phương pháp | Mô tả | TK áp dụng |
|-------------|--------|------------|
| **Bình quân gia quyền cuối kỳ** | Tính lại giá bình quân mỗi cuối kỳ | TK 152, 153, 155, 156 |
| **Bình quân gia quyền liên hoàn** | Tính lại sau mỗi lần nhập | TK 152, 153, 155, 156 |
| **Nhập trước, xuất trước (FIFO)** | Xuất theo thứ tự nhập | TK 152, 153, 155, 156 |
| **Thực tế đích danh** | Theo lô hàng cụ thể | Hàng hóa có giá trị lớn |

> ⚠️ **Lưu ý**: Phương pháp giá xuất kho phải **nhất quán** giữa các kỳ.
> Thay đổi phương pháp phải giải trình trong thuyết minh BCTC.

### Xử lý Chênh lệch Kiểm kê

**Thừa kho**:
```
Nguyên nhân chưa rõ:
  Nợ TK 152/153/155/156
      Có TK 711         Thu nhập khác

Nguyên nhân rõ (NCC giao thừa):
  Nợ TK 152/153/155/156
      Có TK 331         Phải trả người bán
```

**Thiếu kho**:
```
Nguyên nhân chưa rõ (gian lận, hư hỏng):
  Nợ TK 1381 (phải thu khác - cá nhân)
  Nợ TK 632 (giá vốn hàng bán - nếu cho xuất)
  Nợ TK 811 (chi phí khác - hư hỏng)
      Có TK 152/153/155/156

Nguyên nhân rõ (hao hụt tự nhiên):
  Nợ TK 632 (COGS)
      Có TK 152/153/155/156
```

### Tần suất Đối chiếu

| Loại kiểm kê | Tần suất |
|---------------|----------|
| Đối chiếu sổ sách ↔ thẻ kho | Hàng tháng |
| Kiểm kê định kỳ | Hàng quý |
| Kiểm kê cuối năm (bắt buộc) | Hàng năm (trước khi lập BCTC) |
| Kiểm kê đột xuất | Khi có nghi ngờ |

---

## 5. Đối chiếu Tài sản Cố định (TK 211/213/214/241)

### Mục tiêu

Đối chiếu danh sách tài sản cố định (TSCĐ) giữa:
- Sổ cái TK 211 (TSCĐ hữu hình)
- Sổ cái TK 213 (TSCĐ vô hình)
- Sổ cái TK 214 (Hao mòn TSCĐ)
- Sổ cái TK 241 (XDCB dở dang)
- Sổ chi tiết TSCĐ / Thẻ TSCĐ
- Thực tế tại các bộ phận sử dụng

### Tài khoản Liên quan

| TK | Tên | Mô tả |
|----|-----|-------|
| 211 | TSCĐ hữu hình | Nhà cửa, máy móc, thiết bị |
| 2111 | Nhà cửa, vật kiến trúc | |
| 2112 | Máy móc, thiết bị | |
| 2113 | Phương tiện vận tải | |
| 2114 | Thiết bị, dụng cụ quản lý | |
| 2115 | Cây lâu năm, súc vật làm việc | |
| 2118 | TSCĐ khác | |
| 212 | TSCĐ thuê tài chính | |
| 213 | TSCĐ vô hình | Bằng phát minh, thương hiệu, phần mềm |
| 214 | Hao mòn TSCĐ | Khấu hao lũy kế |
| 241 | XDCB dở dang | Công trình chưa hoàn thành |

### Quy trình Đối chiếu

#### Bước 1: Lập danh sách TSCĐ

Từ sổ chi tiết TSCĐ:

| Mã TSCĐ | Tên TSCĐ | Ngày mua | Nguyên giá | Đã khấu hao | Còn lại | Vị trí | Người QL |
|---------|---------|----------|-----------|-------------|---------|--------|----------|
| TS001 | Máy CNC | 2022-03-15 | 500.000.000 | 150.000.000 | 350.000.000 | Xưởng A | Nguyễn Văn A |

#### Bước 2: Đối chiếu với Sổ cái

| Nguồn | Tổng nguyên giá | Tổng đã KH | Tổng còn lại |
|--------|------------------|-----------|--------------|
| Sổ cái TK 211 | X | | |
| Sổ chi tiết TSCĐ | Y | | |
| Chênh lệch | X - Y | | |

#### Bước 3: Đối chiếu với Thực tế

Kiểm tra:
- TSCĐ có còn tồn tại không
- Vị trí có đúng không
- Tình trạng sử dụng
- Có TSCĐ mới phát sinh chưa ghi nhận không

#### Bước 4: Phân tích Chênh lệch

| Chênh lệch | Nguyên nhân | Xử lý |
|-----------|------------|--------|
| Sổ sách > Thực tế | TSCĐ đã thanh lý nhưng chưa ghi giảm | Ghi giảm TSCĐ |
| Thực tế > Sổ sách | TSCĐ chưa ghi nhận | Ghi tăng TSCĐ |
| Sai vị trí | Di chuyển không cập nhật | Cập nhật |
| Sai người QL | Thay đổi nhân sự | Cập nhật |

### Bảng Khấu Hao TSCĐ

Theo Thông tư 45/2013/TT-BTC:

| Nhóm TSCĐ | Thời gian sử dụng (năm) |
|-----------|--------------------------|
| Nhà cửa, vật kiến trúc | 5 - 25 |
| Máy móc, thiết bị | 3 - 10 |
| Phương tiện vận tải | 6 - 10 |
| Thiết bị VP | 3 - 5 |
| TSCĐ vô hình | Theo quy định riêng |

### Xử lý Khi Phát Hiện Sai Lệch

**TSCĐ thừa (chưa ghi nhận)**:
```
Nợ TK 211      TSCĐ hữu hình (nguyên giá)
    Có TK 711       Thu nhập khác (nếu chưa rõ nguồn)
    Có TK 411       Vốn đầu tư CSH (nếu rõ nguồn vốn)
    Có TK 154/241   Chi phí dở dang (nếu đang thi công)
```

**TSCĐ thiếu (đã mất, không rõ)**:
```
Nợ TK 214      Hao mòn (giá trị còn lại)
Nợ TK 811      Chi phí khác (nếu thiếu)
    Có TK 211       TSCĐ hữu hình (nguyên giá)
```

**TSCĐ thanh lý**:
```
Nợ TK 214      Hao mòn lũy kế
Nợ TK 111/112  Tiền thu thanh lý
Nợ/Có TK 811/711  Lỗ/lãi thanh lý
    Có TK 211       TSCĐ hữu hình (nguyên giá)
```

---

## 6. Đối chiếu Liên công ty (Intercompany)

### Mục tiêu

Đối chiếu các giao dịch giữa các công ty trong cùng tập đoàn / công ty mẹ - con:
- Bán hàng / mua hàng liên công ty
- Cho vay / vay giữa các công ty
- Phân bổ chi phí quản lý tập đoàn
- Cổ tức, phân chia lợi nhuận
- Loại trừ khi lập BCTC hợp nhất

### Tài khoản Liên quan

| TK | Tên | Mô tả |
|----|-----|-------|
| 1368 | Phải thu khác (bên liên quan) | Công ty con, công ty liên kết |
| 3368 | Phải trả khác (bên liên quan) | Công ty con, công ty liên kết |
| 1283 | Đầu tư góp vốn vào công ty con | |
| 1281 | Đầu tư vào công ty liên doanh | |
| 1282 | Đầu tư vào công ty liên kết | |

### Phạm vi Giao dịch Liên công ty

| Loại giao dịch | Ví dụ |
|----------------|-------|
| Bán hàng | Cty mẹ bán NVL cho cty con |
| Mua hàng | Cty con bán TP cho cty mẹ |
| Dịch vụ | Cty mẹ cung cấp dịch vụ cho cty con |
| Cho vay | Cty mẹ cho cty con vay vốn |
| Vay | Cty con vay cty mẹ |
| Phân bổ chi phí | Chi phí QLDN tập đoàn phân bổ |
| Cổ tức | Cổ tức từ cty con về cty mẹ |
| Phí quản lý | Phí QLDN tập đoàn |
| Chuyển nhượng vốn | Mua bán cổ phần giữa các công ty |

### Quy trình Đối chiếu

#### Bước 1: Lập sổ chi tiết theo từng công ty liên quan

| Công ty liên quan | Mối quan hệ | Số dư TK 1368 | Số dư TK 3368 |
|-------------------|-------------|---------------|----------------|
| Công ty A | Công ty con | 100 triệu (nợ) | 0 |
| Công ty B | Công ty con | 0 | 50 triệu (có) |
| Công ty C | Liên kết | 30 triệu (nợ) | 0 |

#### Bước 2: Gửi xác nhận công nợ liên công ty

Mẫu tương tự AR/AP, nhưng:
- Có ghi rõ "giao dịch liên công ty"
- Yêu cầu Kế toán trưởng ký
- Thường xuyên hơn (hàng quý)

#### Bước 3: Phân tích Chênh lệch

| Nguyên nhân | Cách xử lý |
|-----------|-----------|
| Ghi nhận sai thời điểm | Điều chỉnh về cùng kỳ |
| Chênh lệch tỷ giá | Đánh giá lại |
| Phân bổ chi phí chưa khớp | Tính lại theo phương pháp thống nhất |
| Chuyển tiền chưa đến | Theo dõi (in-transit) |
| Ghi nhầm bên | Điều chỉnh sang đúng bên liên quan |

### Loại trừ Khi Lập BCTC Hợp nhất

**Các giao dịch cần loại trừ**:

| Loại | Loại trừ |
|------|----------|
| Bán hàng liên công ty | Loại trừ doanh thu + giá vốn |
| Cho vay liên công ty | Loại trừ nợ phải thu + phải trả |
| Lãi cho vay | Loại trừ doanh thu tài chính + chi phí tài chính |
| Cổ tức | Loại trừ (ghi nhận từ lợi nhuận sau thuế của công ty con) |
| Đầu tư góp vốn | Loại trừ khoản đầu tư với vốn CSH |

**Ví dụ loại trừ bán hàng liên công ty**:

```
Cty mẹ bán cho Cty con: 100 triệu (giá bán)
Giá vốn Cty mẹ: 60 triệu
Lợi nhuận gộp: 40 triệu

Bút toán loại trừ:
Nợ TK 511       Doanh thu bán hàng (100 triệu)
    Có TK 632       Giá vốn hàng bán (60 triệu)
    Có TK 157        Hàng gửi bán (40 triệu - hàng chưa xuất đến Cty con)
    hoặc Có TK 632   (nếu Cty con đã bán tiếp)
```

### Giá giao dịch Liên công ty (Transfer Pricing)

**Yêu cầu**: Giao dịch liên công ty phải tuân thủ nguyên tắc **"Giao dịch độc lập so sánh được"** (Arm's Length Principle) theo:
- Nghị định 132/2020/NĐ-CP (quản lý thuế đối với DN có giao dịch liên kết)
- Thông tư 103/2014/TT-BTC (hoặc văn bản mới hơn)
- Nghị định 126/2020/NĐ-CP

| Phương pháp xác định giá | Mô tả |
|---------------------------|--------|
| So sánh giá độc lập (CUP) | So với giao dịch của bên độc lập |
| Giá bán lại (RPM) | Giá bán lại - Biên lợi nhuận hợp lý |
| Giá vốn cộng lãi (Cost Plus) | Giá vốn + % lợi nhuận gross |
| Phân chia lợi nhuận (PSM) | Phân chia theo công sức đóng góp |
| Lợi nhuận ròng (TNMM) | Lợi nhuận ròng so với doanh thu/tài sản |

**Hồ sơ xác định giá giao dịch liên kết**:

| Loại hồ sơ | Mô tả |
|------------|--------|
| Hồ sơ quốc gia | Báo cáo lợi nhuận liên công ty |
| Hồ sơ toàn cầu | Tổng quan DN đa quốc gia |
| Hồ sơ từng quốc gia | Chi tiết cho từng quốc gia |

---

## Bảng Tóm tắt Nhanh - Mã Phân loại Chênh lệch

Dùng các mã sau để phân loại chênh lệch trong bảng đối chiếu:

| Mã | Loại | Mô tả |
|----|-------|--------|
| TIMING_TEMPORARY | Chênh lệch thời gian (tạm thời) | Giao dịch chưa đến hạn ghi nhận |
| TIMING_PERMANENT | Chênh lệch thời gian (vĩnh viễn) | Đã quá hạn, cần điều chỉnh |
| AMOUNT_VARIANCE | Chênh lệch số tiền | Sai số, làm tròn |
| IN_TRANSIT | Đang chuyển | Tiền/HH đang trên đường |
| OUTSTANDING | Chưa thanh toán | Séc, UNC chưa xử lý |
| REC_ERROR | Lỗi ghi sổ | Nhầm TK, nhầm số |
| DUPLICATE | Ghi trùng | Ghi 2 lần |
| MISSING_INT | Thiếu bên trong | Chưa ghi sổ nội bộ |
| MISSING_EXT | Thiếu bên ngoài | Bên ngoài chưa ghi nhận |
| FX_DIFF | Chênh lệch tỷ giá | Cho TK ngoại tệ |
| EXPIRED | Hết hạn | Séc quá hạn, nợ xấu |
| UNIDENTIFIED | Không xác định | Cần điều tra |

---

## Yêu cầu Lưu trữ Chứng từ

Theo Luật Kế toán 88/2015/QH13, Điều 15:

| Loại chứng từ | Thời hạn lưu trữ |
|---------------|------------------|
| Chứng từ kế toán | 10 năm |
| Sổ kế toán | 10 năm |
| Báo cáo tài chính | 10 năm |
| Bảng đối chiếu | 10 năm |
| Thư xác nhận công nợ | 10 năm |
| Biên bản kiểm kê | 10 năm |
| Tài liệu kiểm toán | 10 năm |

> ⚠️ **Lưu ý**: Một số chứng từ có thể cần lưu trữ **vĩnh viễn** (ví dụ:
> tài liệu thành lập DN, tài liệu pháp lý quan trọng).

---

## Tài liệu Tham chiếu

### Quy định Chính

1. **Thông tư 200/2014/TT-BTC** (22/12/2014)
   - Chế độ kế toán DN (đang áp dụng)

2. **Thông tư 99/2025/TT-BTC** (Có hiệu lực 01/01/2026)
   - Chế độ kế toán DN mới

3. **Thông tư 133/2016/TT-BTC** (26/08/2016)
   - Chế độ kế toán DNVVN

4. **Luật Kế toán 88/2015/QH13** (20/11/2015)
   - Điều 15: Thời hạn lưu trữ chứng từ
   - Nguyên tắc kế toán

### Quy định Liên quan

5. **Thông tư 45/2013/TT-BTC** - Hướng dẫn chế độ QLTSCĐ
6. **Thông tư 48/2019/TT-BTC** - Trích lập dự phòng nợ phải thu
7. **Nghị định 132/2020/NĐ-CP** - Quản lý thuế giao dịch liên kết
8. **Thông tư 103/2014/TT-BTC** - Hướng dẫn transfer pricing

---

## Miễn trừ

**Tài liệu tham chiếu này chỉ cung cấp thông tin.**

Thông tin trong tài liệu phản ánh các quy định được biết đến công khai tính
đến ngày tạo skill. Pháp luật và quy định có thể thay đổi. Luôn xác minh với
công báo chính thức mới nhất và tham khảo tư vấn viên thuế / kế toán có
chứng chỉ để có hướng dẫn chính thức.

Tài liệu này KHÔNG cấu thành tư vấn pháp lý hay tài chính. Tác giả và cộng
tác viên không chịu trách nhiệm về bất kỳ quyết định nào được đưa ra dựa trên
thông tin này.

**Để có hướng dẫn chính thức**:
- Bộ Tài chính: https://mof.gov.vn
- Tổng cục Thuế: https://gdt.gov.vn
- Hiệp hội Kế toán Việt Nam (VAA): https://vaa.vn

---

*Cập nhật lần cuối: 2026-09-09*