import { useCallback, useEffect, useRef, useState } from 'react';
import type { DemoRunEvent, DemoRunMode, RunDoneEvent, TraceEvent } from '@/types/api';
import { streamDemoRun } from '@/services/runsService';

export type DemoRunStatus = 'idle' | 'running' | 'done' | 'error' | 'cancelled';

export interface DemoRunState {
  status: DemoRunStatus;
  traces: TraceEvent[];
  result: RunDoneEvent | null;
  error: string | null;
}

export interface UseDemoRunResult extends DemoRunState {
  start: (mode: DemoRunMode, question: string) => void;
  cancel: () => void;
}

const INITIAL_STATE: DemoRunState = { status: 'idle', traces: [], result: null, error: null };

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

function applyEvent(state: DemoRunState, event: DemoRunEvent): DemoRunState {
  switch (event.type) {
    case 'trace':
      return { ...state, traces: [...state.traces, event.payload] };
    case 'done':
      return { ...state, status: 'done', result: event.payload };
    case 'error':
      return { ...state, status: 'error', error: event.payload.message };
  }
}

/** Chạy agent demo qua SSE và gom các sự kiện thành state cho giao diện. Huỷ được bằng AbortController. */
export function useDemoRun(): UseDemoRunResult {
  const [state, setState] = useState<DemoRunState>(INITIAL_STATE);
  const controllerRef = useRef<AbortController | null>(null);

  const cancel = useCallback(() => {
    controllerRef.current?.abort();
  }, []);

  const start = useCallback((mode: DemoRunMode, question: string) => {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setState({ ...INITIAL_STATE, status: 'running' });

    const isCurrent = () => controllerRef.current === controller;

    streamDemoRun({
      mode,
      question,
      signal: controller.signal,
      onEvent: (event) => {
        if (isCurrent()) {
          setState((current) => applyEvent(current, event));
        }
      },
    })
      .then(() => {
        if (!isCurrent()) {
          return;
        }
        // Stream đóng mà không có `done` hay `error`: coi là lỗi để người dùng biết.
        setState((current) =>
          current.status === 'running'
            ? { ...current, status: 'error', error: 'Kết nối đóng trước khi agent chạy xong.' }
            : current,
        );
      })
      .catch((error: unknown) => {
        if (!isCurrent()) {
          return;
        }
        if (isAbortError(error)) {
          setState((current) => ({ ...current, status: 'cancelled' }));
          return;
        }
        const message = error instanceof Error ? error.message : 'Lỗi không xác định khi chạy agent.';
        setState((current) => ({ ...current, status: 'error', error: message }));
      })
      .finally(() => {
        if (isCurrent()) {
          controllerRef.current = null;
        }
      });
  }, []);

  // Rời trang khi đang chạy: huỷ request để không giữ kết nối.
  useEffect(() => () => controllerRef.current?.abort(), []);

  return { ...state, start, cancel };
}
