import { describe, expect, it } from 'vitest';
import { createSseParser, readSseStream, type SseMessage } from './sse';

function parseAll(chunks: string[]): SseMessage[] {
  const messages: SseMessage[] = [];
  const parser = createSseParser((message) => messages.push(message));
  chunks.forEach((chunk) => parser.feed(chunk));
  parser.flush();
  return messages;
}

describe('createSseParser', () => {
  it('tách sự kiện có tên và data, ngăn bằng dòng trống (LF)', () => {
    const messages = parseAll(['event: trace\ndata: {"seq":1}\n\nevent: done\ndata: {"ok":true}\n\n']);
    expect(messages).toEqual([
      { event: 'trace', data: '{"seq":1}', id: undefined },
      { event: 'done', data: '{"ok":true}', id: undefined },
    ]);
  });

  it('xử lý CRLF kể cả khi CR và LF nằm ở hai chunk khác nhau', () => {
    const messages = parseAll(['event: trace\r', '\ndata: a\r\n\r', '\n']);
    expect(messages).toEqual([{ event: 'trace', data: 'a', id: undefined }]);
  });

  it('ghép nhiều dòng data, bỏ chú thích, mặc định tên "message"', () => {
    const messages = parseAll([': keep-alive\n', 'data: dòng 1\ndata: dòng 2\n\n']);
    expect(messages).toEqual([{ event: 'message', data: 'dòng 1\ndòng 2', id: undefined }]);
  });

  it('chịu được chunk cắt ngang giữa dòng', () => {
    const messages = parseAll(['eve', 'nt: err', 'or\nda', 'ta: {"message":"x"}', '\n', '\n']);
    expect(messages).toEqual([{ event: 'error', data: '{"message":"x"}', id: undefined }]);
  });

  it('phát sự kiện cuối khi stream hết mà thiếu dòng trống', () => {
    const messages = parseAll(['event: done\ndata: {}']);
    expect(messages).toEqual([{ event: 'done', data: '{}', id: undefined }]);
  });

  it('bỏ qua khối không có data', () => {
    expect(parseAll(['event: trace\n\n'])).toEqual([]);
  });
});

describe('readSseStream', () => {
  it('giải mã UTF-8 bị cắt giữa ký tự nhiều byte', async () => {
    const bytes = new TextEncoder().encode('event: trace\r\ndata: Tallyo có gì?\r\n\r\n');
    const splitAt = bytes.indexOf(0xc3) + 1; // cắt giữa 2 byte của "ó"
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(bytes.slice(0, splitAt));
        controller.enqueue(bytes.slice(splitAt));
        controller.close();
      },
    });
    const messages: SseMessage[] = [];
    await readSseStream(body, (message) => messages.push(message));
    expect(messages).toEqual([{ event: 'trace', data: 'Tallyo có gì?', id: undefined }]);
  });
});
