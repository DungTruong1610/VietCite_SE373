---
path: /tinh-nang/ban-hang-tai-quay/
parent: /tinh-nang/
title: Bán hàng tại quầy và quản lý kho với Tallyo
description: "Tính tiền bằng mã vạch, nhận tiền qua mã VietQR, in hoá đơn ra máy in nhiệt và theo dõi tồn kho trên điện thoại. Tallyo vẫn bán được khi mất mạng."
template: doc
h1: Bán hàng tại quầy và quản lý kho
eyebrow: Tính năng
lede: Màn hình tính tiền của Tallyo làm cho những quầy đông khách lúc tan tầm. Mọi đơn bán đều trừ kho và vào sổ ngay.
icon: scan-barcode
order: 22
toc: true
---

Tallyo chạy trên điện thoại Android, iPhone, máy tính bảng và trình duyệt. Bạn không cần mua máy bán hàng riêng: một chiếc điện thoại và máy in nhiệt đang có thường là đủ để bắt đầu.

## Tính tiền nhanh bằng mã vạch hoặc chạm chọn món

Với tiệm tạp hoá, bạn quét mã vạch in sẵn trên sản phẩm bằng camera điện thoại hoặc máy quét. Với quán cà phê, bạn chạm chọn món trên màn hình, thêm ghi chú như "ít đá" hay "mang đi".

- Tìm mặt hàng theo tên, mã vạch hoặc mã bạn tự đặt.
- Giảm giá theo đơn hoặc theo món; mỗi lần giảm giá ghi tên nhân viên thực hiện.
- Tách đơn, gộp đơn và lưu đơn tạm khi khách chưa thanh toán.

## Nhận tiền qua mã VietQR

Khi khách chọn chuyển khoản, Tallyo hiện mã VietQR có sẵn số tiền của đơn. Khách quét bằng ứng dụng ngân hàng, bạn không phải đọc số tài khoản hay số tiền. Đơn vẫn ghi nhận cả tiền mặt và thẻ, để cuối ngày bạn đối chiếu theo từng hình thức thanh toán.

## Máy in và máy quét dùng được

{{ brand.name }} không bán phần cứng. Bạn dùng thiết bị phổ thông đang có trên thị trường:

| Thiết bị | Tallyo hỗ trợ |
|---|---|
| Máy in hoá đơn | {{ facts.compatibility.printers | join(", ") }} |
| Kết nối máy in | {{ facts.compatibility.printer_connections | join(", ") }} |
| Máy quét mã vạch | {{ facts.compatibility.scanners | join(", ") }} |
| Thiết bị chạy Tallyo | {{ facts.compatibility.platforms | join(", ") }} |

## Quản lý kho

Tính năng quản lý kho có trong gói {{ plans.shop.name }} và gói {{ plans.chain.name }}.

- **Nhập hàng:** quét mã vạch từng thùng hoặc tải phiếu nhập từ file Excel.
- **Cảnh báo sắp hết:** đặt mức tồn tối thiểu cho từng mặt hàng, Tallyo nhắc khi chạm mức.
- **Kiểm kho bằng điện thoại:** đi dọc kệ quét mã, Tallyo so số đếm với số trên sổ và ghi lại chênh lệch.

## Bán khi mất mạng

{{ facts.compatibility.offline_mode }} Khi có mạng lại, Tallyo đồng bộ đơn hàng và kho theo đúng thứ tự thời gian bán.

## Tallyo có bán máy in không?

Không. {{ brand.name }} chỉ cung cấp phần mềm. Nếu bạn đang có máy in nhiệt khổ 58 mm hoặc 80 mm, hãy thử kết nối trong thời gian dùng thử {{ facts.trial.days }} ngày trước khi mua thiết bị mới.
