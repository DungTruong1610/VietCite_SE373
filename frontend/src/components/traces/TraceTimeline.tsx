import { useEffect, useRef } from 'react';
import { Badge, type BadgeProps } from '@cnma/react-ui';
import type { TraceEvent, TraceKind } from '@/types/api';

type BadgeVariant = NonNullable<BadgeProps['variant']>;

const KIND_VARIANTS: Record<string, BadgeVariant> = {
  human: 'informativeBlue',
  ai: 'subColor1',
  tool: 'informativeTeal',
  gate: 'attention',
  approval: 'warning',
  harness: 'obsoleted',
  stop: 'negative',
};

function kindVariant(kind: TraceKind): BadgeVariant {
  return KIND_VARIANTS[kind] ?? 'outline';
}

interface TraceTimelineProps {
  traces: TraceEvent[];
  running: boolean;
}

/** Dòng thời gian các bước của agent, cập nhật trực tiếp khi sự kiện `trace` tới. */
export function TraceTimeline({ traces, running }: TraceTimelineProps) {
  const endRef = useRef<HTMLLIElement>(null);

  useEffect(() => {
    if (running) {
      endRef.current?.scrollIntoView({ block: 'nearest' });
    }
  }, [traces.length, running]);

  if (traces.length === 0) {
    return (
      <p className="py-6 text-center text-sm text-muted-foreground">
        {running ? 'Đang chờ bước đầu tiên của agent…' : 'Chưa có bước nào. Bấm "Chạy" để bắt đầu.'}
      </p>
    );
  }

  return (
    <ol className="max-h-[28rem] space-y-2 overflow-auto pr-1" aria-live="polite">
      {traces.map((trace) => (
        <li
          key={`${trace.span_id}-${trace.seq}`}
          className="grid grid-cols-[3rem_6rem_1fr] items-start gap-3 rounded-md border border-border bg-card px-3 py-2"
        >
          <span className="font-mono text-xs text-muted-foreground">#{trace.seq}</span>
          <Badge variant={kindVariant(trace.kind)} hasBorder className="justify-center">
            {trace.kind}
          </Badge>
          <div className="min-w-0">
            <div className="font-mono text-xs text-muted-foreground">
              {trace.agent ? `${trace.agent} · ` : ''}
              {trace.node}
            </div>
            <div className="text-sm whitespace-pre-wrap break-words text-foreground">{trace.text}</div>
          </div>
        </li>
      ))}
      <li ref={endRef} aria-hidden className="h-0" />
    </ol>
  );
}
