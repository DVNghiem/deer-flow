---
name: inventory-fifo-allocation
description: >
  Phân bổ tồn kho theo phương pháp FIFO (nhập trước xuất trước) theo
  TT 99/2025/TT-BTC, TT 200/2014/TT-BTC và TT 133/2016/TT-BTC. Trigger khi
  user cần: tính giá vốn xuất kho, phân bổ lô hàng cho đơn hàng, kiểm tra
  hạn sử dụng / hạn dùng, đối chiếu tồn kho sổ sách với tồn kho thực tế
  theo FIFO, hoặc quyết định lô hàng nào được xuất trước.
version: 1.1.0
domain: vietnam-accounting
regime: [tt99, tt200, tt133]
tags:
  - accounting
  - vietnam
  - inventory
  - fifo
  - cost-allocation
  - warehouse
author: DeerFlow Community
created: 2025-07-06
updated: 2026-09-09
legal_basis:
  - Thông tư 99/2025/TT-BTC
  - Thông tư 200/2014/TT-BTC
  - Thông tư 133/2016/TT-BTC
  - Luật Kế toán 88/2015/QH13
---

# Skill Phân bổ FIFO Tồn kho

## Mục đích

Phân bổ tồn kho theo phương pháp **FIFO (First In First Out - Nhập trước,
Xuất trước)** cho doanh nghiệp Việt Nam. Hỗ trợ:

1. **Tính giá vốn xuất kho** theo phương pháp FIFO
2. **Phân bổ lô hàng** cho đơn hàng / yêu cầu xuất
3. **Kiểm tra hạn sử dụng / hạn dùng (HSD)** để quyết định lô xuất trước
4. **Đối chiếu tồn kho sổ sách với thực tế** theo FIFO
5. **Quyết định lô hàng xuất trước** dựa trên nhiều tiêu chí

## Khi nào sử dụng

- Tính giá vốn hàng bán theo FIFO (bảng kê xuất kho)
- Phân bổ hàng tồn kho cho đơn hàng cụ thể
- Kiểm tra hàng sắp hết hạn (FEFO - First Expired First Out)
- Đối chiếu tồn kho giữa sổ sách và kho vật lý (theo FIFO logic)
- Xử lý nhập trước nhưng chưa xuất (kiểm tra hàng tồn lâu)

## Khi nào KHÔNG sử dụng

- **Phương pháp giá khác** (bình quân gia quyền, LIFO, ...) — skill này
  chỉ hỗ trợ FIFO
- **Kiểm kê kho và xử lý chênh lệch** (thừa/thiếu) — dùng
  `accounting-stocktake`
- **Đánh giá lại tồn kho** (revaluation) — không thuộc phạm vi skill này
- **Quản lý kho vật lý (WMS)** — skill chỉ xử lý logic FIFO trên dữ liệu

---

## Đầu vào Bắt buộc

| Đầu vào | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `fifo_method` | enum | Có | `"fifo"` (nhập trước xuất trước) hoặc `"fefo"` (hết hạn trước xuất trước) |
| `inventory_lots` | array | Có | Danh sách lô hàng nhập kho |
| `output_requests` | array | Tùy chọn | Yêu cầu xuất kho (nếu có) |
| `allocation_strategy` | enum | Tùy chọn | `"fifo_only"`, `"fefo_only"`, `"combined"` |

### Schema Đầu vào

```typescript
interface FifoAllocationInput {
  fifo_method: "fifo" | "fefo";
  inventory_lots: InventoryLot[];
  output_requests?: OutputRequest[];
  allocation_strategy?: "fifo_only" | "fefo_only" | "combined";
}

interface InventoryLot {
  lot_id: string;                    // Mã lô (unique)
  item_code: string;                  // Mã hàng hóa
  item_name?: string;                 // Tên hàng
  received_date: string;              // Ngày nhập (YYYY-MM-DD)
  expiry_date?: string;               // Hạn sử dụng (nếu có)
  quantity: number;                   // Số lượng nhập
  remaining_quantity?: number;        // SL còn lại (nếu đã xuất một phần)
  unit_cost: number;                  // Giá vốn / đơn vị (VND)
  total_cost?: number;                // Tổng giá trị lô
  supplier?: string;                  // Mã NCC
  warehouse_location?: string;        // Vị trí kho
  notes?: string;
}

interface OutputRequest {
  request_id: string;
  item_code: string;
  quantity: number;
  requested_date?: string;
  priority?: "high" | "medium" | "low";
  customer_reference?: string;
}
```

---

## Phương pháp FIFO & FEFO

### FIFO - First In First Out (Nhập trước, Xuất trước)

**Nguyên tắc**: Hàng hóa nhập kho trước sẽ được xuất trước. Khi xuất kho,
căn cứ vào **ngày nhập** để xác định lô hàng.

**Căn cứ pháp lý**:
- Thông tư 200/2014/TT-BTC, Phụ lục 02 — Hướng dẫn TK 152, 153, 155, 156
- Thông tư 133/2016/TT-BTC — Tương tự cho DNVVN
- Thông tư 99/2025/TT-BTC — Chế độ kế toán DN mới (có hiệu lực 01/01/2026)

### FEFO - First Expired First Out (Hết hạn trước, Xuất trước)

**Nguyên tắc**: Ưu tiên xuất lô hàng có **hạn sử dụng gần nhất** trước.
FEFO thường được dùng kết hợp với FIFO cho hàng hóa có hạn dùng (thực phẩm,
dược phẩm, hóa chất).

### So sánh FIFO và FEFO

| Tiêu chí | FIFO | FEFO |
|---------|------|------|
| Căn cứ | Ngày nhập | Hạn sử dụng |
| Áp dụng cho | Mọi hàng hóa | Hàng có HSD |
| Ưu tiên | Lô nhập cũ nhất | Lô sắp hết hạn nhất |
| Phù hợp | Hàng không HSD | Thực phẩm, dược phẩm, hóa chất |

### Combined (Kết hợp)

Khi cả ngày nhập và hạn dùng đều quan trọng:
- Ưu tiên theo HSD trước (FEFO)
- Nếu HSD bằng nhau → theo FIFO

---

## Quy trình Phân bổ Từng bước

### Bước 1: Chuẩn bị dữ liệu lô hàng

1. Lấy tất cả lô hàng còn tồn cho mã hàng hóa
2. Sắp xếp theo:
   - FIFO: `received_date` tăng dần (nhập trước → trước)
   - FEFO: `expiry_date` tăng dần (hết hạn trước → trước)
   - Combined: `expiry_date` trước, nếu null thì `received_date`
3. Tính `remaining_quantity` cho mỗi lô:
   ```
   remaining = quantity - Σ(quantity đã xuất)
   ```

### Bước 2: Validate dữ liệu đầu vào

| Trường | Quy tắc |
|--------|---------|
| `lot_id` | Bắt buộc, duy nhất |
| `received_date` | Bắt buộc, định dạng YYYY-MM-DD |
| `quantity` | > 0 |
| `unit_cost` | > 0 |
| `remaining_quantity` | ≤ `quantity` |

### Bước 3: Phân bổ theo FIFO/FEFO

**Thuật toán**:

```python
def allocate_fifo(lots, request_qty, strategy="fifo"):
    # Sắp xếp lô hàng
    if strategy == "fifo":
        sorted_lots = sorted(lots, key=lambda l: l["received_date"])
    elif strategy == "fefo":
        sorted_lots = sorted(
            lots,
            key=lambda l: (l["expiry_date"] or "9999-12-31", l["received_date"])
        )

    allocations = []
    remaining = request_qty

    for lot in sorted_lots:
        if remaining <= 0:
            break

        available = lot["remaining_quantity"]
        if available <= 0:
            continue

        allocate_qty = min(remaining, available)
        allocations.append({
            "lot_id": lot["lot_id"],
            "received_date": lot["received_date"],
            "expiry_date": lot.get("expiry_date"),
            "quantity": allocate_qty,
            "unit_cost": lot["unit_cost"],
            "total_cost": allocate_qty * lot["unit_cost"]
        })
        remaining -= allocate_qty

    if remaining > 0:
        raise InsufficientInventoryError(
            f"Không đủ tồn kho. Thiếu {remaining} đơn vị."
        )

    return allocations
```

### Bước 4: Tính giá vốn

Với mỗi yêu cầu xuất:

```
Tổng giá vốn = Σ(quantity × unit_cost) của tất cả lô được phân bổ
Giá vốn đơn vị (bình quân) = Tổng giá vốn / Tổng số lượng
```

### Bước 5: Sinh kết quả

Trả về:
- Danh sách phân bổ chi tiết (từng lô)
- Tổng giá vốn
- Lô còn tồn sau phân bổ
- Cảnh báo (nếu có)

---

## Xử lý Các Trường hợp Đặc biệt

### 1. Không đủ tồn kho

**Hành động**: Trả lỗi `insufficient_inventory` với số lượng thiếu. KHÔNG
tự động điều chỉnh giá vốn.

```
{
  "status": "insufficient_inventory",
  "requested_quantity": 100,
  "available_quantity": 75,
  "shortage": 25,
  "action_required": "Bổ sung hàng hoặc điều chỉnh yêu cầu xuất"
}
```

### 2. Lô có cùng ngày nhập

Nếu nhiều lô cùng `received_date`:
- Ưu tiên theo `lot_id` (thường là thứ tự nhập)
- Hoặc ưu tiên lô có `unit_cost` thấp hơn (tùy chính sách DN)
- **Cần cấu hình rõ** trong `allocation_strategy`

### 3. Lô không có hạn sử dụng (FEFO)

Nếu `expiry_date = null` và dùng FEFO:
- Ưu tiên lô có HSD trước
- Sau đó xếp lô không có HSD theo FIFO (ngày nhập)
- Hoặc bỏ qua lô không có HSD (cần xác nhận từ user)

### 4. Cảnh báo hàng sắp hết hạn

Với FEFO, nếu hàng còn tồn < 30 ngày trước HSD → flag cảnh báo:

```json
{
  "warning": "near_expiry",
  "lot_id": "LOT-2024-001",
  "expiry_date": "2026-10-15",
  "days_remaining": 36,
  "remaining_quantity": 50,
  "recommendation": "Ưu tiên xuất lô này trước khi hết hạn"
}
```

### 5. Lô hàng âm (dữ liệu sai)

Nếu `remaining_quantity < 0` → flag lỗi dữ liệu, dừng xử lý.

---

## Bút toán Kế toán Liên quan

Khi xuất kho theo FIFO, bút toán:

```
Nợ TK 632    Giá vốn hàng bán (giá FIFO)
    Có TK 152/153/155/156   Hàng tồn kho (giá FIFO)
```

Nếu có nhiều lô, có thể tách thành nhiều bút toán (một cho mỗi lô) hoặc
một bút toán tổng hợp với thuyết minh.

**Ví dụ**:
- Lô A: 50 đơn vị × 10.000 VND = 500.000 VND
- Lô B: 30 đơn vị × 12.000 VND = 360.000 VND
- Tổng: 80 đơn vị, giá vốn 860.000 VND

```
Nợ TK 632          860.000
    Có TK 152         860.000
```

Với thuyết minh: "Xuất kho FIFO: Lô A 50 đơn vị × 10.000 = 500.000; Lô B
30 đơn vị × 12.000 = 360.000"

---

## Ví dụ Minh họa

### Dữ liệu

```json
{
  "fifo_method": "fifo",
  "inventory_lots": [
    {
      "lot_id": "LOT-001",
      "item_code": "SP-A",
      "received_date": "2025-09-01",
      "quantity": 100,
      "unit_cost": 10000,
      "remaining_quantity": 100
    },
    {
      "lot_id": "LOT-002",
      "item_code": "SP-A",
      "received_date": "2025-09-15",
      "quantity": 150,
      "unit_cost": 11000,
      "remaining_quantity": 150
    },
    {
      "lot_id": "LOT-003",
      "item_code": "SP-A",
      "received_date": "2025-10-01",
      "quantity": 80,
      "unit_cost": 12000,
      "remaining_quantity": 80
    }
  ],
  "output_requests": [
    {
      "request_id": "REQ-001",
      "item_code": "SP-A",
      "quantity": 180
    }
  ]
}
```

### Kết quả

```json
{
  "allocations": [
    {
      "lot_id": "LOT-001",
      "received_date": "2025-09-01",
      "quantity": 100,
      "unit_cost": 10000,
      "total_cost": 1000000
    },
    {
      "lot_id": "LOT-002",
      "received_date": "2025-09-15",
      "quantity": 80,
      "unit_cost": 11000,
      "total_cost": 880000
    }
  ],
  "total_quantity": 180,
  "total_cost": 1880000,
  "average_unit_cost": 10444.44,
  "lots_remaining": [
    { "lot_id": "LOT-002", "remaining": 70 },
    { "lot_id": "LOT-003", "remaining": 80 }
  ],
  "journal_entry": {
    "debit_account": "632",
    "debit_amount": 1880000,
    "credit_account": "152",
    "credit_amount": 1880000,
    "description": "Xuất kho FIFO cho REQ-001"
  }
}
```

---

## Script Tham chiếu

Xem [script/allocation_engine.py](script/allocation_engine.py) để có
implementation Python đầy đủ cho thuật toán FIFO/FEFO.

### Sử dụng nhanh

```python
from allocation_engine import FifoAllocator, FifoStrategy

allocator = FifoAllocator(strategy=FifoStrategy.FIFO)
result = allocator.allocate(
    lots=inventory_lots,
    item_code="SP-A",
    quantity=180
)

print(f"Tổng giá vốn: {result.total_cost:,} VND")
for alloc in result.allocations:
    print(f"  Lô {alloc.lot_id}: {alloc.quantity} × {alloc.unit_cost:,} = {alloc.total_cost:,}")
```

---

## Anti-Hallucination Rules

### Rule 1: Không tự tính giá vốn khi thiếu dữ liệu

Nếu thiếu `unit_cost` hoặc `quantity` → flag lỗi, yêu cầu bổ sung.

### Rule 2: Không tự ý thay đổi chiến lược phân bổ

Nếu user yêu cầu FIFO mà có nhiều lô cùng ngày → hỏi ý kiến user trước
khi áp tiêu chí phụ.

### Rule 3: Không tự xử lý khi không đủ tồn kho

Flag shortage, KHÔNG tự động lấy hàng từ lô khác / tăng giá vốn / điều
chỉnh.

### Rule 4: Không tự ý cập nhật `remaining_quantity`

Skill chỉ tính toán phân bổ. Việc cập nhật sổ sách phải do kế toán kho
hoặc hệ thống ERP.

### Rule 5: Không bịa giá vốn

Giá vốn phải từ lô hàng thực tế. KHÔNG lấy giá thị trường / ước lượng /
số liệu ngoài dữ liệu.

### Rule 6: Khi HSD không có sẵn, không tự suy ra

Nếu `expiry_date = null` và user yêu cầu FEFO → flag, hỏi user có nên
dùng FIFO thay thế không.

---

## Output Format

```json
{
  "skill": "inventory-fifo-allocation",
  "version": "1.1.0",
  "fifo_method": "fifo|fefo",
  "allocation_strategy": "fifo_only|fefo_only|combined",
  "allocations": [
    {
      "request_id": "",
      "item_code": "",
      "lot_id": "",
      "received_date": "YYYY-MM-DD",
      "expiry_date": "YYYY-MM-DD",
      "quantity": 0,
      "unit_cost": 0,
      "total_cost": 0,
      "remaining_after_allocation": 0
    }
  ],
  "summary": {
    "total_requested": 0,
    "total_allocated": 0,
    "total_cost": 0,
    "average_unit_cost": 0,
    "lots_used": 0,
    "lots_remaining": 0
  },
  "shortage": {
    "has_shortage": false,
    "shortage_quantity": 0,
    "reason": ""
  },
  "warnings": [
    {
      "type": "near_expiry|negative_quantity|missing_data|tied_received_date",
      "lot_id": "",
      "description": "",
      "recommendation": ""
    }
  ],
  "journal_entries": [
    {
      "lines": [
        { "account_code": "632", "debit": 0, "credit": 0, "description": "" },
        { "account_code": "152", "debit": 0, "credit": 0, "description": "" }
      ],
      "legal_reference": ""
    }
  ],
  "flags": [],
  "disclaimer": "Bản phân bổ FIFO dựa trên dữ liệu user cung cấp. Kế toán kho xác nhận trước khi hạch toán."
}
```

---

## Escalation Rules

| Tình huống | Mức độ | Người nhận |
|-----------|--------|-----------|
| Thiếu hàng > 10% yêu cầu | HIGH | Kế toán kho + Kinh doanh |
| Lô sắp hết HSD (< 30 ngày) còn tồn nhiều | MEDIUM | Kế toán kho + Marketing |
| Lô có số lượng âm | CRITICAL | Kế toán kho + KTNB |
| Lô cùng ngày nhập cần quyết định | MEDIUM | Kế toán trưởng |
| Sai lệch giá vốn > 5% | HIGH | Kế toán trưởng |
| Giá trị xuất > 1 tỷ VND | HIGH | Kế toán trưởng + Giám đốc |

---

## Legal Disclaimer

Skill này hỗ trợ tính toán phân bổ FIFO/FEFO cho tồn kho. **Không thay thế
kế toán kho** trong việc quản lý vật lý và cập nhật sổ sách.

Tuân thủ:
- Thông tư 200/2014/TT-BTC (và TT 99/2025 từ 01/01/2026) cho DN
- Thông tư 133/2016/TT-BTC cho DNVVN
- Luật Kế toán 88/2015/QH13 về nguyên tắc kế toán, chứng từ

> ⚠️ **Cần xác minh**: Một số quy định cụ thể về phương pháp tính giá xuất
> kho có thể đã được sửa đổi bởi Thông tư 99/2025. Tra cứu văn bản hiện
> hành trước khi áp dụng cho DN theo chế độ kế toán mới.

Kết quả phân bổ là bản dự thảo. Cần:
- Xác nhận của kế toán kho về số liệu tồn kho
- Đối chiếu với thẻ kho, sổ kho vật lý
- Phê duyệt bút toán trước khi ghi sổ

---

*Cập nhật lần cuối: 2026-09-09*
*Phiên bản skill: 1.1.0*