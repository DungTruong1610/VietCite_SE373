import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import type { AuthUser, LoginRequest } from '@/types/api';
import { fetchCurrentUser, login as loginRequest } from '@/services/authService';
import { setUnauthorizedHandler } from '@/services/apiClient';
import { clearToken, getToken, setToken } from '@/services/tokenStorage';

export type AuthStatus = 'checking' | 'authenticated' | 'anonymous';

export interface AuthContextValue {
  status: AuthStatus;
  user: AuthUser | null;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [status, setStatus] = useState<AuthStatus>(() => (getToken() ? 'checking' : 'anonymous'));

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
    setStatus('anonymous');
  }, []);

  // Token hết hạn hoặc bị thu hồi: bất kỳ API nào trả 401 sẽ đưa người dùng về trang đăng nhập.
  useEffect(() => {
    setUnauthorizedHandler(logout);
    return () => setUnauthorizedHandler(null);
  }, [logout]);

  // Có token cũ trong sessionStorage: hỏi /api/auth/me để xác nhận còn hiệu lực.
  useEffect(() => {
    if (!getToken()) {
      return;
    }
    const controller = new AbortController();
    fetchCurrentUser(controller.signal)
      .then((currentUser) => {
        setUser(currentUser);
        setStatus('authenticated');
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') {
          return;
        }
        clearToken();
        setUser(null);
        setStatus('anonymous');
      });
    return () => controller.abort();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    const response = await loginRequest(credentials);
    setToken(response.access_token);
    setUser(response.user);
    setStatus('authenticated');
  }, []);

  const value = useMemo<AuthContextValue>(() => ({ status, user, login, logout }), [status, user, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth phải được dùng bên trong <AuthProvider>.');
  }
  return context;
}
