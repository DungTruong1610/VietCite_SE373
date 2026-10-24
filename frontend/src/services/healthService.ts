import type { HealthResponse } from '@/types/api';
import { apiJson } from '@/services/apiClient';

export function fetchHealth(signal?: AbortSignal): Promise<HealthResponse> {
  return apiJson<HealthResponse>('/api/health', { auth: false, signal });
}
