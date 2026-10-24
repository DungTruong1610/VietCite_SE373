import { useState, type FormEvent } from 'react';
import {
  Alert,
  AlertDescription,
  AlertTitle,
  Badge,
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Field,
  FieldDescription,
  FieldLabel,
  Input,
  NativeSelect,
  Spinner,
} from '@cnma/react-ui';
import { CircleAlert, Play, Square } from 'lucide-react';
import type { DemoRunMode } from '@/types/api';
import { useDemoRun, type DemoRunStatus } from '@/hooks/useDemoRun';
import { TraceTimeline } from '@/components/traces/TraceTimeline';
import { RunResult } from '@/components/traces/RunResult';

/** Agent demo chỉ có tool máy tính, nên câu hỏi mặc định là một bài toán cần tính. */
export const DEFAULT_DEMO_QUESTION =
  'Một shop bán 2.400.000đ mỗi ngày. 30 ngày thì doanh thu bao nhiêu, và 1,5% của số đó là bao nhiêu?';

const MODE_OPTIONS: ReadonlyArray<{ value: DemoRunMode; label: string }> = [
  { value: 'mock', label: 'mock: model giả, chạy offline' },
  { value: 'live', label: 'live: gọi model thật' },
];

const STATUS_LABELS: Record<DemoRunStatus, string> = {
  idle: 'chưa chạy',
  running: 'đang chạy',
  done: 'hoàn tất',
  error: 'lỗi',
  cancelled: 'đã huỷ',
};

function isDemoRunMode(value: string): value is DemoRunMode {
  return value === 'mock' || value === 'live';
}

export function DemoRunPanel() {
  const [mode, setMode] = useState<DemoRunMode>('mock');
  const [question, setQuestion] = useState(DEFAULT_DEMO_QUESTION);
  const run = useDemoRun();
  const running = run.status === 'running';

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!running && question.trim() !== '') {
      run.start(mode, question.trim());
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Chạy agent demo</CardTitle>
          <CardDescription>
            Agent demo có một tool máy tính. Mỗi bước (người hỏi, model, tool, gate, dừng) hiện ra ngay khi
            backend phát sự kiện.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-[14rem_1fr_auto] md:items-end">
            <Field>
              <FieldLabel htmlFor="demo-mode">Chế độ</FieldLabel>
              <NativeSelect
                id="demo-mode"
                value={mode}
                disabled={running}
                onChange={(event) => {
                  if (isDemoRunMode(event.target.value)) {
                    setMode(event.target.value);
                  }
                }}
              >
                {MODE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </NativeSelect>
            </Field>
            <Field>
              <FieldLabel htmlFor="demo-question">Câu hỏi</FieldLabel>
              <Input
                id="demo-question"
                value={question}
                disabled={running}
                onChange={(event) => setQuestion(event.target.value)}
              />
            </Field>
            <div className="flex gap-2">
              {running ? (
                <Button type="button" variant="outline" onClick={run.cancel}>
                  <Square className="size-4" />
                  Huỷ
                </Button>
              ) : (
                <Button type="submit" disabled={question.trim() === ''}>
                  <Play className="size-4" />
                  Chạy
                </Button>
              )}
            </div>
          </form>
          {mode === 'live' ? (
            <FieldDescription className="mt-2">
              Chế độ live cần backend có khoá API; nếu chưa cấu hình, backend sẽ trả lỗi.
            </FieldDescription>
          ) : null}
        </CardContent>
      </Card>

      {run.status === 'error' && run.error ? (
        <Alert variant="destructive">
          <CircleAlert />
          <AlertTitle>Lần chạy gặp lỗi</AlertTitle>
          <AlertDescription>{run.error}</AlertDescription>
        </Alert>
      ) : null}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Dòng thời gian
            <Badge variant={running ? 'info' : 'secondary'}>{STATUS_LABELS[run.status]}</Badge>
            {running ? <Spinner size="sm" /> : null}
          </CardTitle>
          <CardDescription>{run.traces.length} bước</CardDescription>
        </CardHeader>
        <CardContent>
          <TraceTimeline traces={run.traces} running={running} />
        </CardContent>
      </Card>

      {run.result ? <RunResult result={run.result} /> : null}
    </div>
  );
}
