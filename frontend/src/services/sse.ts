/**
 * Parser Server-Sent Events tối giản.
 *
 * EventSource không gửi được header Authorization nên frontend đọc stream bằng `fetch`
 * rồi tự tách sự kiện. Theo chuẩn SSE (WHATWG HTML, mục "event stream"):
 * - dòng kết thúc bằng CRLF, LF hoặc CR;
 * - `event:` đặt tên sự kiện, `data:` nối dữ liệu (nhiều dòng data ghép bằng "\n");
 * - dòng bắt đầu bằng `:` là chú thích, bỏ qua;
 * - một dòng trống kết thúc một sự kiện.
 */

export interface SseMessage {
  /** Tên sự kiện; mặc định "message" nếu server không gửi `event:`. */
  event: string;
  data: string;
  id?: string;
}

export interface SseParser {
  /** Nạp thêm một đoạn văn bản (có thể cắt ngang giữa dòng hoặc giữa CRLF). */
  feed(chunk: string): void;
  /** Gọi khi stream kết thúc: xử lý phần còn lại và phát sự kiện cuối nếu còn dữ liệu. */
  flush(): void;
}

const DEFAULT_EVENT = 'message';

export function createSseParser(onMessage: (message: SseMessage) => void): SseParser {
  let buffer = '';
  let eventName = '';
  let dataLines: string[] = [];
  let lastId: string | undefined;

  const dispatch = (): void => {
    if (dataLines.length > 0) {
      onMessage({ event: eventName || DEFAULT_EVENT, data: dataLines.join('\n'), id: lastId });
    }
    eventName = '';
    dataLines = [];
  };

  const processLine = (line: string): void => {
    if (line === '') {
      dispatch();
      return;
    }
    if (line.startsWith(':')) {
      return;
    }
    const colon = line.indexOf(':');
    const field = colon === -1 ? line : line.slice(0, colon);
    let value = colon === -1 ? '' : line.slice(colon + 1);
    if (value.startsWith(' ')) {
      value = value.slice(1);
    }
    switch (field) {
      case 'event':
        eventName = value;
        break;
      case 'data':
        dataLines.push(value);
        break;
      case 'id':
        lastId = value;
        break;
      default:
        // `retry` và trường lạ: không dùng.
        break;
    }
  };

  const drain = (final: boolean): void => {
    for (;;) {
      const crIndex = buffer.indexOf('\r');
      const lfIndex = buffer.indexOf('\n');
      let end: number;
      if (crIndex === -1) {
        end = lfIndex;
      } else if (lfIndex === -1) {
        end = crIndex;
      } else {
        end = Math.min(crIndex, lfIndex);
      }
      if (end === -1) {
        break;
      }
      // CR ở cuối buffer có thể là nửa đầu của CRLF: chờ đoạn tiếp theo.
      if (buffer[end] === '\r' && end === buffer.length - 1 && !final) {
        break;
      }
      const terminatorLength = buffer[end] === '\r' && buffer[end + 1] === '\n' ? 2 : 1;
      const line = buffer.slice(0, end);
      buffer = buffer.slice(end + terminatorLength);
      processLine(line);
    }
  };

  return {
    feed(chunk: string): void {
      buffer += chunk;
      drain(false);
    },
    flush(): void {
      drain(true);
      if (buffer !== '') {
        processLine(buffer);
        buffer = '';
      }
      // Chuẩn SSE bỏ sự kiện dở dang khi hết stream; ở đây vẫn phát để không mất `done`
      // nếu server quên dòng trống cuối cùng.
      dispatch();
    },
  };
}

/**
 * Đọc toàn bộ body của một response SSE, gọi `onMessage` cho từng sự kiện.
 * Dừng khi stream kết thúc hoặc khi `signal` bị huỷ (ném AbortError).
 */
export async function readSseStream(
  body: ReadableStream<Uint8Array>,
  onMessage: (message: SseMessage) => void,
  signal?: AbortSignal,
): Promise<void> {
  const reader = body.getReader();
  const decoder = new TextDecoder('utf-8');
  const parser = createSseParser(onMessage);

  const onAbort = (): void => {
    void reader.cancel().catch(() => undefined);
  };
  signal?.addEventListener('abort', onAbort, { once: true });

  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      parser.feed(decoder.decode(value, { stream: true }));
    }
    if (signal?.aborted) {
      throw new DOMException('Đã huỷ', 'AbortError');
    }
    parser.feed(decoder.decode());
    parser.flush();
  } finally {
    signal?.removeEventListener('abort', onAbort);
    reader.releaseLock();
  }
}
