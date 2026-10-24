import type { ApiErrorBody } from '@/types/api';
import { getToken } from '@/services/tokenStorage';

/** Lỗi HTTP từ backend, giữ status và thông điệp `detail` để hiển thị cho người dùng. */
export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

type UnauthorizedHandler = () => void;
let unauthorizedHandler: UnauthorizedHandler | null = null;

/** AuthContext đăng ký hàm này để tự đăng xuất khi token hết hạn (401 trên API cần đăng nhập). */
export function setUnauthorizedHandler(handler: UnauthorizedHandler | null): void {
  unauthorizedHandler = handler;
}

export interface ApiRequestOptions extends Omit<RequestInit, 'body'> {
  /** Thân JSON; được stringify và gắn Content-Type tự động. */
  json?: unknown;
  /** Gắn header `Authorization: Bearer <token>` (mặc định: có). */
  auth?: boolean;
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  return (
    typeof value === 'object' &&
    value !== null &&
    'detail' in value &&
    typeof (value as { detail: unknown }).detail === 'string'
  );
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();
    if (isApiErrorBody(body)) {
      return body.detail;
    }
  } catch {
    // Thân không phải JSON: dùng thông điệp mặc định bên dưới.
  }
  return `Yêu cầu thất bại (HTTP ${response.status}).`;
}

/**
 * Gửi request tới backend và trả về Response thô khi thành công (2xx).
 * Dùng trực tiếp cho luồng SSE; các API JSON thường dùng `apiJson`.
 */
export async function apiRequest(path: string, options: ApiRequestOptions = {}): Promise<Response> {
  const { json, auth = true, headers, ...init } = options;
  const finalHeaders = new Headers(headers);

  if (json !== undefined) {
    finalHeaders.set('Content-Type', 'application/json');
  }
  if (auth) {
    const token = getToken();
    if (token) {
      finalHeaders.set('Authorization', `Bearer ${token}`);
    }
  }

  let response: Response;
  try {
    response = await fetch(path, {
      ...init,
      headers: finalHeaders,
      body: json === undefined ? undefined : JSON.stringify(json),
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw error;
    }
    throw new ApiError(0, 'Không kết nối được tới backend. Kiểm tra server ở cổng 8000.');
  }

  if (!response.ok) {
    const message = await readErrorMessage(response);
    if (response.status === 401 && auth && unauthorizedHandler) {
      unauthorizedHandler();
    }
    throw new ApiError(response.status, message);
  }
  return response;
}

/** Gọi API trả JSON. Kiểu `T` là interface trong `@/types/api`. */
export async function apiJson<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const response = await apiRequest(path, options);
  return (await response.json()) as T;
}
