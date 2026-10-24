# VietCite Studio: frontend

React 19 + Vite + TypeScript (strict) + Tailwind CSS v4. Component lấy từ thư viện nội bộ `@cnma/react-ui` 1.1.4.

Phase 1 mới là khung: đăng nhập, layout (header + sidebar) với 8 màn hình, trang **Tổng quan** (gọi `/api/health`) và trang **Traces & Eval** (chạy agent demo, xem trace trực tiếp qua SSE). Các màn hình còn lại chỉ ghi phase sẽ xây chúng.

## Cài đặt

Cần Node 22 trở lên và npm 10 trở lên.

1. Xin TV1 file `cnma-react-ui-1.1.4.tgz`, đặt vào `../packages/` (file này **không** commit).
2. Kiểm tra gói đúng bản:

   ```bash
   node ../scripts/check-ui-package.mjs
   ```

3. Cài thư viện (file `.npmrc` trong thư mục này chỉ bật `legacy-peer-deps`):

   ```bash
   npm install
   ```

## Chạy khi phát triển

```bash
npm run dev
```

Mở http://localhost:5173. Mọi request `/api/*` được Vite chuyển sang backend ở `http://localhost:8000`, nên phải chạy backend trước (xem `../backend`). Tài khoản đăng nhập do backend cấu hình; nếu backend chưa cấu hình, trang đăng nhập hiện thông báo lỗi 503 của server.

## Kiểm tra và build

```bash
npm run typecheck   # tsc, không sinh file
npm test            # vitest: test parser SSE
npm run build       # tsc -b && vite build, kết quả ở dist/
npm run preview     # xem bản build
```

## Cấu trúc

```
src/
  main.tsx, App.tsx       # khởi tạo provider, khai báo route
  config/navigation.ts    # 8 màn hình trên sidebar
  contexts/               # AuthContext (token, user), ThemeContext
  services/               # apiClient (gắn Bearer token), auth, health, runs, sse
  hooks/useDemoRun.ts     # chạy agent demo, gom sự kiện SSE, huỷ bằng AbortController
  components/             # layout, auth, common, traces
  pages/                  # Login, Tổng quan, Traces & Eval, trang chờ
  types/api.ts            # interface cho mọi response của backend
```

## Ghi chú

- Token giữ trong bộ nhớ và `sessionStorage` (đóng tab là mất). API nào trả 401 thì app tự đăng xuất.
- Luồng trace dùng `fetch` và tự parse Server-Sent Events (`src/services/sse.ts`), vì `EventSource` không gửi được header `Authorization`.
- Giao diện: thư viện chỉ có theme sáng, gồm hai bảng màu Conarum (đỏ) và SAP Horizon (xanh), chọn qua `data-sap-theme`. Nút trên header chuyển giữa hai bảng màu này. Thư viện chưa có dark mode.
