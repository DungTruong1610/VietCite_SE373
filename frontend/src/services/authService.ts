import type { AuthUser, LoginRequest, LoginResponse } from '@/types/api';
import { apiJson } from '@/services/apiClient';

export function login(credentials: LoginRequest): Promise<LoginResponse> {
  // auth: false để 401 "sai mật khẩu" không kích hoạt tự đăng xuất.
  return apiJson<LoginResponse>('/api/auth/login', {
    method: 'POST',
    json: credentials,
    auth: false,
  });
}

export function fetchCurrentUser(signal?: AbortSignal): Promise<AuthUser> {
  return apiJson<AuthUser>('/api/auth/me', { signal });
}
