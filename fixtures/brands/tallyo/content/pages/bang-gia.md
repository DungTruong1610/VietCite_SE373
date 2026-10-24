---
path: /bang-gia/
title: "Bảng giá Tallyo: gói Khởi đầu, Cửa hàng, Chuỗi"
description: "Bảng giá Tallyo cho hộ kinh doanh: gói Khởi đầu, Cửa hàng và Chuỗi, trả theo tháng hoặc năm. Dùng thử 15 ngày, không cần thẻ thanh toán."
template: pricing
h1: Bảng giá Tallyo
nav: Bảng giá
eyebrow: Bảng giá
lede: "Ba gói theo quy mô cửa hàng. Gói nào cũng có hoá đơn điện tử khởi tạo từ máy tính tiền và sổ sách cho hộ kinh doanh."
order: 30
---

## Dùng thử {{ facts.trial.days }} ngày

Bạn dùng thử đủ tính năng của gói {{ plans.shop.name }} trong {{ facts.trial.days }} ngày, không cần nhập thẻ thanh toán. Hết thời gian dùng thử mà chưa chọn gói, tài khoản chuyển sang chế độ chỉ xem và dữ liệu được giữ {{ facts.trial.data_kept_days }} ngày.

## Mua thêm hoá đơn điện tử

Mỗi gói có sẵn một số lượng hoá đơn điện tử mỗi năm. Nếu cửa hàng bán nhiều hơn, bạn mua thêm:

| Gói thêm | Giá | Thời hạn dùng |
|---|---|---|
{% for a in facts.addons %}| {{ a.name }} | {{ a.price | vnd }} | {{ a.validity_months }} tháng |
{% endfor %}

## Thanh toán và hoàn tiền

- Hình thức thanh toán: {{ facts.billing.payment_methods | join(", ") }}.
- {{ facts.billing.year_discount_note }}.
- Gói năm thanh toán lần đầu được hoàn tiền trong {{ facts.billing.refund.annual_first_payment_days }} ngày. Gói tháng không hoàn tiền. Chi tiết ở [Điều khoản sử dụng](/chinh-sach/dieu-khoan-su-dung/#hoan-tien).
- Khi thay đổi giá, {{ brand.name }} thông báo trước ít nhất {{ facts.billing.price_change_notice_days }} ngày. {{ facts.billing.price_change_rule }}
