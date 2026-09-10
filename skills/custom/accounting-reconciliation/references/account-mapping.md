# Mapping Tài khoản — TT 99/2025 ↔ TT 200/2014 ↔ TT 133/2016

> Ánh xạ tài khoản kế toán thường dùng trong đối chiếu sổ sách.
> Tham chiếu chính: Thông tư 99/2025/TT-BTC (hiệu lực 01/01/2026).

## Tài khoản thường dùng trong đối chiếu

| Nội dung | TT 99/2025 | TT 200/2014 | TT 133/2016 |
|----------|-----------|-------------|-------------|
| Tiền mặt | 1111 | 1111 | 111 |
| Tiền gửi NH VND | 1121 | 1121 | 112 |
| Tiền gửi NH ngoại tệ | 1122 | 1122 | 112 |
| Phải thu khách hàng | 131 | 131 | 131 |
| Trả trước người bán | 132 | 132 | 132 |
| Tạm ứng | 141 | 141 | 141 |
| Phải trả người bán | 331 | 331 | 331 |
| Người mua trả tiền trước | 131 (ghi Có) | 131 (ghi Có) | 131 (ghi Có) |
| Phải trả NLĐ | 334 | 334 | 334 |
| BHXH/BHYT/BHTN phải nộp | 338 | 338 | 338 |
| NVL | 152 | 152 | 152 |
| CCDC | 153 | 153 | 153 |
| Thành phẩm | 155 | 155 | 155 |
| Hàng hóa | 156 | 156 | 156 |
| TSCĐ hữu hình | 211 | 211 | 211 |
| Hao mòn TSCĐ | 2141 | 2141 | 2141 |
| XDCB dở dang | 241 | 241 | 241 |
| VAT đầu vào | 1331 | 133 | 133 |
| VAT đầu ra | 33311 | 3331 | 3331 |
| Thuế TNDN | 8211 | 8211 | 821 |
| Doanh thu | 511 | 511 | 511 |
| Giá vốn | 632 | 632 | 632 |
| CP bán hàng | 6411 | 641 | 642 |
| CP QLDN | 6421 | 642 | 642 |
| CP khác | 811 | 811 | 811 |
| LNST chưa PP | 421 | 421 | 421 |

## Quy tắc đối chiếu khi hỗn hợp chế độ

Khi đối chiếu dữ liệu từ nhiều kỳ (một số kỳ dùng TT 200, một số dùng TT 99):

1. **Cùng số 3 chữ số đầu**: ánh xạ trực tiếp (VD: 1111 ↔ 1111, 1121 ↔ 1121).
2. **Khác số 3 chữ số**:
   - TK TT 200 dạng rút gọn (3 chữ số) → map sang TT 99 dạng 4 chữ số
   - VD: TT 200 "133" ↔ TT 99 "1331"
3. **TT 133 ↔ TT 99/200**:
   - TT 133 rút gọn nhiều TK
   - VD: TT 133 "111" có thể tương ứng TT 99 "1111" (TM) hoặc "113" (vàng)
     tùy nội dung giao dịch

## Trường hợp không thể ánh xạ tự động

Khi không chắc chắn, **không tự động map** — flag trong output:
```
FLAG: Account code {code} from {regime} cannot be confidently mapped to
{other_regime}. Manual review required.
```

## Xác minh trước khi áp dụng

Bảng trên dựa trên hiểu biết chung về cấu trúc ba chế độ kế toán. Trước khi
áp dụng vào sổ sách chính thức, kế toán trưởng cần đối chiếu với:
- Bản PDF chính thức TT 99/2025/TT-BTC trên Cổng thông tin Bộ Tài chính
- Hệ thống TK đang dùng trong phần mềm kế toán của doanh nghiệp