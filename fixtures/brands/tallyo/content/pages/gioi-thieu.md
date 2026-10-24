---
path: /gioi-thieu/
title: Về Tallyo
description: "Tallyo được thành lập năm 2023 tại TP. Hồ Chí Minh để giúp hộ kinh doanh bán hàng và kê khai đúng quy định mà không cần biết kế toán."
template: doc
h1: Về Tallyo
eyebrow: Công ty
lede: "{{ brand.mission }}"
order: 60
---

## Tallyo bắt đầu từ một tiệm tạp hoá

Năm {{ brand.founded_year }}, nhóm sáng lập của {{ brand.name }} ngồi cả buổi tối ở một tiệm tạp hoá quen tại {{ brand.city }} để giúp chủ tiệm cộng sổ cuối tháng. Sổ ghi tay, tin nhắn chuyển khoản và hoá đơn nhập hàng nằm ở ba nơi khác nhau. Chủ tiệm bán giỏi nhưng phần giấy tờ thì mất gần một ngày mỗi tháng.

{{ brand.name }} ra đời từ buổi tối đó, với một mục tiêu: phần ghi chép và giấy tờ phải tự động xong ngay khi bán hàng xong.

## Điều Tallyo tin

- Chủ cửa hàng nhỏ không cần học kế toán để kê khai đúng. Phần mềm phải làm phần việc ghi chép thay họ.
- Mỗi tính năng phải dùng được trên một chiếc điện thoại phổ thông, ở quầy đông khách.
- Nói rõ giá, nói rõ giới hạn của từng gói, không để khách bất ngờ khi nhận hoá đơn.

## Tallyo hôm nay

Tính đến ngày {{ brand.customers.as_of | date_vi }}, {{ brand.customers.wording }} đang dùng {{ brand.name }}. Đội ngũ có {{ brand.team_size }} người, làm việc tại {{ brand.city }}. Đội hỗ trợ trả lời {{ brand.contact.support_hours }}.

## Thông tin công ty

| Hạng mục | Thông tin |
|---|---|
| Tên công ty | {{ brand.legal_name }} |
| Năm thành lập | {{ brand.founded_year }} |
| Trụ sở | {{ brand.city }} |
| Email hỗ trợ | {{ brand.contact.support_email }} |
| Email tư vấn | {{ brand.contact.sales_email }} |

<div class="note">{{ icon("info", 20) }}<div><p><strong>Đây là công ty giả lập.</strong> {{ brand.name }}, {{ brand.legal_name }} và mọi số liệu trên trang này được tạo ra cho đồ án SE373 (UIT). Không có pháp nhân thật mang tên này đứng sau website.</p></div></div>
