# ADR 0002: Dùng thư viện UI nội bộ `@cnma/react-ui` cho frontend

- **Trạng thái:** Đã chấp nhận (thay phần thư viện component trong ADR 0001)
- **Ngày:** 24/10/2026
- **Người quyết định:** TV1, sau khi xác nhận được phép dùng gói

## Bối cảnh

ADR 0001 chọn shadcn/ui cho frontend. Một thành viên làm ở công ty có thư viện component React riêng (`@cnma/react-ui`, Radix UI + Tailwind v4, giao diện theo Fiori) và được phép dùng nó trong đồ án. Gói không có trên npm công khai (`npm view @cnma/react-ui` trả 404); bản build có sẵn dưới dạng file `cnma-react-ui-1.1.4.tgz`. Repo đồ án là **public**.

## Quyết định

1. Frontend dùng `@cnma/react-ui` làm thư viện component chính, khai báo bằng đường dẫn file: `"@cnma/react-ui": "file:../packages/cnma-react-ui-1.1.4.tgz"`.
2. **File `.tgz` không commit** (`packages/*.tgz` trong `.gitignore`). TV1 gửi trực tiếp cho thành viên; `scripts/check-ui-package.mjs` kiểm tra file có mặt và đúng SHA-256.
3. **Backend giữ nguyên Python FastAPI, không dùng SAP CAP.** Gói UI chạy với bất kỳ backend nào; thêm CAP chỉ sinh thêm một backend.
4. Frontend tự khai báo các phụ thuộc gói dùng mà không khai báo: `@radix-ui/react-aspect-ratio`, `radix-ui`, `recharts` (+ `react-is`); ghim `react-i18next` ^16.5 và `i18next` ^25.
5. CI trên GitHub không có gói nên **bỏ qua build frontend khi thiếu file** và ghi rõ trong log. Build và test frontend (Playwright) chạy ở máy thành viên trước khi merge.

## Hệ quả

- **Tốt:** giao diện đồng nhất, nhiều component dựng sẵn (349 export, có `DataTable`, `FilterBar`), giảm công Phase 8; thành viên đã quen thư viện.
- **Đổi lại:**
  - Thành viên mới phải xin file trước khi chạy frontend.
  - CI không kiểm được frontend; phải kỷ luật build ở máy trước khi mở PR.
  - Phụ thuộc vào một bản build cố định (1.1.4); muốn nâng cấp phải xin bản mới và đổi SHA-256 trong script.
- **Ràng buộc:** không đưa file `.tgz`, mã nguồn của gói hay `.npmrc` trỏ tới feed nội bộ vào repo.

## Phương án đã cân nhắc

- **shadcn/ui (ADR 0001):** công khai, CI build được, nhưng phải tự dựng nhiều component. Thay bằng gói nội bộ.
- **`@ui5/webcomponents-react`:** giao diện Fiori chuẩn, công khai, nhưng nhóm không quen và khác với thư viện công ty.
- **Commit `.tgz` vào repo (cách của repo 8D cũ):** tiện nhất cho CI, nhưng phát tán thư viện nội bộ lên repo public. Loại.
- **Frontend trên nền SAP CAP TypeScript:** không cần cho việc dùng gói, thêm một backend thứ hai. Loại.
