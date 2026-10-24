import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

/**
 * @cnma/react-ui 1.1.4 chọn bảng màu qua thuộc tính `data-sap-theme` trên <html>.
 * Thư viện chỉ có hai theme sáng (màu thương hiệu Conarum và SAP Horizon), chưa có token cho dark mode,
 * nên app cho phép chuyển giữa hai theme này.
 */
export type AppTheme = 'proconarumv2@' | 'sap_horizon';

export const THEME_LABELS: Record<AppTheme, string> = {
  'proconarumv2@': 'Conarum (đỏ)',
  sap_horizon: 'SAP Horizon (xanh)',
};

const STORAGE_KEY = 'vietcite.theme';
const DEFAULT_THEME: AppTheme = 'proconarumv2@';

function isAppTheme(value: string | null): value is AppTheme {
  return value === 'proconarumv2@' || value === 'sap_horizon';
}

function readStoredTheme(): AppTheme {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return isAppTheme(stored) ? stored : DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
}

export interface ThemeContextValue {
  theme: AppTheme;
  setTheme: (theme: AppTheme) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [theme, setTheme] = useState<AppTheme>(readStoredTheme);

  useEffect(() => {
    document.documentElement.setAttribute('data-sap-theme', theme);
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // Không lưu được lựa chọn: lần sau dùng theme mặc định.
    }
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme((current) => (current === 'sap_horizon' ? 'proconarumv2@' : 'sap_horizon'));
  }, []);

  const value = useMemo<ThemeContextValue>(() => ({ theme, setTheme, toggleTheme }), [theme, toggleTheme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme phải được dùng bên trong <ThemeProvider>.');
  }
  return context;
}
