/**
 * Giữ access token trong bộ nhớ, đồng thời lưu vào sessionStorage để F5 không mất phiên.
 * sessionStorage có thể bị chặn (chế độ riêng tư, chính sách trình duyệt) nên mọi truy cập đều bọc try/catch.
 */
const STORAGE_KEY = 'vietcite.accessToken';

let memoryToken: string | null = null;
let loadedFromStorage = false;

export function getToken(): string | null {
  if (!loadedFromStorage) {
    loadedFromStorage = true;
    try {
      memoryToken = window.sessionStorage.getItem(STORAGE_KEY);
    } catch {
      memoryToken = null;
    }
  }
  return memoryToken;
}

export function setToken(token: string): void {
  memoryToken = token;
  loadedFromStorage = true;
  try {
    window.sessionStorage.setItem(STORAGE_KEY, token);
  } catch {
    // Không lưu được thì vẫn dùng token trong bộ nhớ.
  }
}

export function clearToken(): void {
  memoryToken = null;
  loadedFromStorage = true;
  try {
    window.sessionStorage.removeItem(STORAGE_KEY);
  } catch {
    // Bỏ qua: không có gì để xoá.
  }
}
