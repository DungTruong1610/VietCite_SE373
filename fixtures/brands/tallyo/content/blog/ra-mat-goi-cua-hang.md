---
path: /blog/ra-mat-goi-cua-hang/
parent: /blog/
title: Tallyo ra mắt gói Cửa hàng cho tiệm có nhân viên
description: "Tallyo ra mắt gói Cửa hàng dành cho tiệm có nhân viên và cần quản lý kho, với giá ra mắt cho hộ kinh doanh đăng ký trong năm 2025."
template: doc
h1: Tallyo ra mắt gói Cửa hàng cho tiệm có nhân viên
eyebrow: Tin sản phẩm
summary: Gói mới cho tiệm có nhân viên và cần quản lý kho, kèm giá ra mắt năm 2025.
published: 2025-03-01
order: 92
---

{% set launch = plans.shop.plan.price_history[0] %}
Từ hôm nay, {{ brand.name }} có thêm gói **{{ plans.shop.name }}** dành cho những tiệm đã có nhân viên đứng quầy và cần biết chính xác hàng trong kho còn bao nhiêu.

## Gói Cửa hàng có gì

- {{ plans.shop.staff_accounts }} tài khoản nhân viên, mỗi người một mật khẩu riêng.
- Quản lý kho: nhập hàng, cảnh báo sắp hết, kiểm kho bằng điện thoại.
- {{ plans.shop.einvoice_per_year | number_vi }} hoá đơn điện tử mỗi năm.
- Gom đơn online về chung một kho với đơn bán tại quầy.

## Giá ra mắt

Gói {{ plans.shop.name }} có giá **{{ launch.price_month | vnd }} mỗi tháng**, hoặc {{ launch.price_year | vnd }} nếu trả theo năm. Gói {{ plans.start.name }} giữ nguyên giá {{ plans.start.plan.price_history[0].price_month | vnd }} mỗi tháng.

## Ai nên chuyển sang gói Cửa hàng

Nếu tiệm của bạn có từ hai người đứng quầy trở lên, hoặc bạn thường xuyên hết hàng mà không biết trước, gói {{ plans.shop.name }} sẽ giúp bạn nhiều hơn gói {{ plans.start.name }}. Bạn có thể đổi gói bất cứ lúc nào trong phần Cài đặt.
