/** Kiểu dữ liệu của các API backend (FastAPI) mà frontend Phase 1 dùng. */

export type UserRole = 'editor' | 'approver';

export interface AuthUser {
  username: string;
  role: UserRole;
}

export interface LoginRequest {
  username: string;
  password: string;
}

/** POST /api/auth/login → 200 */
export interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
  user: AuthUser;
}

/** Thân lỗi chuẩn của FastAPI (401, 503, ...). */
export interface ApiErrorBody {
  detail: string;
}

/** GET /api/health */
export interface HealthResponse {
  status: 'ok';
  version: string;
  features: HealthFeatures;
  offline: boolean;
}

export interface HealthFeatures {
  deepseek: boolean;
  jina: boolean;
  gemini: boolean;
}

export type DemoRunMode = 'mock' | 'live';

/** Các loại bước trong trace. Backend có thể thêm loại mới nên vẫn nhận chuỗi bất kỳ. */
export type TraceKind =
  | 'human'
  | 'ai'
  | 'tool'
  | 'gate'
  | 'approval'
  | 'harness'
  | 'stop'
  | (string & {});

/** SSE `event: trace` */
export interface TraceEvent {
  run_id: string;
  span_id: string;
  seq: number;
  agent: string;
  node: string;
  kind: TraceKind;
  text: string;
  data: Record<string, unknown>;
  ts: string;
}

export interface RunUsage {
  model_calls: number;
  tool_calls: number;
  tokens_in: number;
  tokens_out: number;
  cached_tokens: number;
  cost_usd: number;
}

/** SSE `event: done` */
export interface RunDoneEvent {
  run_id: string;
  stop_reason: string;
  answer: string | null;
  usage: RunUsage;
  trace_file: string | null;
}

/** SSE `event: error` */
export interface RunErrorEvent {
  message: string;
}

/** Sự kiện của luồng chạy demo sau khi đã parse JSON. */
export type DemoRunEvent =
  | { type: 'trace'; payload: TraceEvent }
  | { type: 'done'; payload: RunDoneEvent }
  | { type: 'error'; payload: RunErrorEvent };
