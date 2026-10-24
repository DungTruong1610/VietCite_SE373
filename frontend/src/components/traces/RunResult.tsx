import { Badge, Card, CardContent, CardDescription, CardHeader, CardTitle } from '@cnma/react-ui';
import type { RunDoneEvent, RunUsage } from '@/types/api';

interface UsageField {
  key: keyof RunUsage;
  label: string;
  format: (value: number) => string;
}

const integerFormat = new Intl.NumberFormat('vi-VN');
const usdFormat = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 4,
  maximumFractionDigits: 6,
});

const USAGE_FIELDS: UsageField[] = [
  { key: 'model_calls', label: 'Lượt gọi model', format: (v) => integerFormat.format(v) },
  { key: 'tool_calls', label: 'Lượt gọi tool', format: (v) => integerFormat.format(v) },
  { key: 'tokens_in', label: 'Token vào', format: (v) => integerFormat.format(v) },
  { key: 'tokens_out', label: 'Token ra', format: (v) => integerFormat.format(v) },
  { key: 'cached_tokens', label: 'Token cache', format: (v) => integerFormat.format(v) },
  { key: 'cost_usd', label: 'Chi phí', format: (v) => usdFormat.format(v) },
];

interface RunResultProps {
  result: RunDoneEvent;
}

/** Kết quả cuối của một lần chạy: câu trả lời, lý do dừng và mức sử dụng. */
export function RunResult({ result }: RunResultProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex flex-wrap items-center gap-2">
          Kết quả
          <Badge variant="informativeTeal" hasBorder>
            dừng: {result.stop_reason}
          </Badge>
        </CardTitle>
        <CardDescription className="font-mono text-xs">run_id: {result.run_id}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="mb-1 text-sm font-medium text-muted-foreground">Câu trả lời</div>
          <p className="rounded-md border border-border bg-background p-3 text-sm whitespace-pre-wrap">
            {result.answer ?? '(Agent không trả lời.)'}
          </p>
        </div>

        <dl className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {USAGE_FIELDS.map((field) => (
            <div key={field.key} className="rounded-md border border-border p-3">
              <dt className="text-xs text-muted-foreground">{field.label}</dt>
              <dd className="mt-1 text-lg font-semibold">{field.format(result.usage[field.key])}</dd>
            </div>
          ))}
        </dl>

        {result.trace_file ? (
          <p className="text-xs text-muted-foreground">
            File trace: <span className="font-mono">{result.trace_file}</span>
          </p>
        ) : null}
      </CardContent>
    </Card>
  );
}
