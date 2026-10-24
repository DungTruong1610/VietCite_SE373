import type { DemoRunEvent, DemoRunMode, RunDoneEvent, RunErrorEvent, TraceEvent } from '@/types/api';
import { ApiError, apiRequest } from '@/services/apiClient';
import { readSseStream, type SseMessage } from '@/services/sse';

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isTraceEvent(value: unknown): value is TraceEvent {
  return (
    isObject(value) &&
    typeof value.seq === 'number' &&
    typeof value.kind === 'string' &&
    typeof value.text === 'string'
  );
}

function isRunDoneEvent(value: unknown): value is RunDoneEvent {
  return isObject(value) && typeof value.stop_reason === 'string' && isObject(value.usage);
}

function isRunErrorEvent(value: unknown): value is RunErrorEvent {
  return isObject(value) && typeof value.message === 'string';
}

/** Chuyển một sự kiện SSE thô thành sự kiện có kiểu; trả null nếu không nhận ra. */
export function toDemoRunEvent(message: SseMessage): DemoRunEvent | null {
  let payload: unknown;
  try {
    payload = JSON.parse(message.data);
  } catch {
    return null;
  }
  switch (message.event) {
    case 'trace':
      return isTraceEvent(payload) ? { type: 'trace', payload } : null;
    case 'done':
      return isRunDoneEvent(payload) ? { type: 'done', payload } : null;
    case 'error':
      return isRunErrorEvent(payload) ? { type: 'error', payload } : null;
    default:
      return null;
  }
}

export interface StreamDemoRunParams {
  mode: DemoRunMode;
  question: string;
  signal: AbortSignal;
  onEvent: (event: DemoRunEvent) => void;
}

/**
 * Gọi GET /api/runs/demo/stream (cần Bearer token) và phát từng sự kiện trace/done/error.
 * Dùng fetch + đọc stream thủ công vì EventSource không gửi được header Authorization.
 */
export async function streamDemoRun({ mode, question, signal, onEvent }: StreamDemoRunParams): Promise<void> {
  const params = new URLSearchParams({ mode, question });
  const response = await apiRequest(`/api/runs/demo/stream?${params.toString()}`, {
    headers: { Accept: 'text/event-stream' },
    signal,
  });
  if (!response.body) {
    throw new ApiError(response.status, 'Trình duyệt không đọc được luồng dữ liệu từ server.');
  }
  await readSseStream(
    response.body,
    (message) => {
      const event = toDemoRunEvent(message);
      if (event) {
        onEvent(event);
      }
    },
    signal,
  );
}
