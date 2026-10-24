---
path: /chinh-sach/bao-mat/
title: Chính sách bảo mật của Tallyo
description: "Tallyo thu thập dữ liệu gì, dùng vào việc gì, lưu ở đâu và bạn có quyền gì với dữ liệu bán hàng và thông tin khách hàng của cửa hàng mình."
template: doc
h1: Chính sách bảo mật
eyebrow: Chính sách
lede: Dữ liệu bán hàng là của bạn. Trang này nói rõ Tallyo giữ dữ liệu gì, dùng làm gì và giữ trong bao lâu.
order: 80
toc: true
cta: false
laws: [91/2025/QH15, 356/2025/NĐ-CP, 152/2025/TT-BTC]
---

<div class="note">{{ icon("info", 20) }}<div><p>Đây là chính sách mẫu của một công ty giả lập, viết cho đồ án SE373 (UIT). Văn bản không có giá trị pháp lý. Các văn bản pháp luật nhắc trên trang là thật và đã được đối chiếu nguồn chính thống ngày {{ facts.legal_facts.verified_on | date_vi }}.</p></div></div>

## Căn cứ

Chính sách này được viết theo {{ law(facts.legal_refs.privacy_law) }} (có hiệu lực từ {{ lawref(facts.legal_refs.privacy_law).effective_date | date_vi }}) và {{ law(facts.legal_refs.privacy_decree) }} hướng dẫn luật này.

## Dữ liệu Tallyo thu thập

- **Thông tin tài khoản:** tên cửa hàng, tên chủ hộ, email, số điện thoại, mã số thuế của hộ kinh doanh.
- **Dữ liệu bán hàng:** mặt hàng, đơn hàng, hoá đơn, tồn kho, sổ doanh thu và chi phí.
- **Thông tin khách mua hàng** mà cửa hàng nhập khi lập hoá đơn, ví dụ tên công ty và mã số thuế của khách.
- **Nhật ký sử dụng:** thời điểm đăng nhập, thiết bị, thao tác huỷ đơn và giảm giá, để phục vụ phân quyền nhân viên.

## Tallyo dùng dữ liệu vào việc gì

- Vận hành phần mềm: tính tiền, lập hoá đơn, lập sổ, báo cáo.
- Hỗ trợ khi bạn gửi yêu cầu cho đội hỗ trợ.
- Gửi thông báo về tài khoản, thanh toán và thay đổi giá.

{{ brand.name }} không bán dữ liệu và không dùng dữ liệu bán hàng của bạn để quảng cáo.

## Chia sẻ dữ liệu với bên thứ ba

Dữ liệu hoá đơn được chuyển cho tổ chức cung cấp dịch vụ hoá đơn điện tử mà bạn chọn, để lập hoá đơn theo quy định. Ngoài trường hợp này và trường hợp cơ quan nhà nước có thẩm quyền yêu cầu theo pháp luật, {{ brand.name }} không chia sẻ dữ liệu của bạn.

## Lưu trữ ở đâu và bao lâu

Dữ liệu lưu tại {{ facts.privacy.data_location }}. Sau khi bạn ngừng sử dụng, {{ brand.name }} giữ hoá đơn và sổ sách thêm {{ facts.privacy.retention_after_cancel_years }} năm rồi xoá. Mốc này bằng thời hạn lưu tài liệu kế toán tối thiểu của hộ kinh doanh theo {{ law(facts.legal_refs.books) }}. Thời hạn lưu hoá đơn theo pháp luật về thuế; bạn nên tải bản sao về máy trước khi ngừng.

## Quyền của bạn

Bạn có các quyền của chủ thể dữ liệu theo {{ law(facts.legal_refs.privacy_law) }}. Theo chính sách của {{ brand.name }}, bạn có thể yêu cầu xem, chỉnh sửa hoặc xoá dữ liệu cá nhân của mình, trừ phần dữ liệu mà pháp luật yêu cầu phải lưu. Gửi yêu cầu tới [{{ brand.contact.support_email }}](mailto:{{ brand.contact.support_email }}).

## Liên hệ về dữ liệu

Mọi câu hỏi về dữ liệu cá nhân, gửi email tới [{{ brand.contact.support_email }}](mailto:{{ brand.contact.support_email }}), {{ brand.contact.support_hours }}.
