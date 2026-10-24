# Ma trận phủ kiến thức K1–K8

> **Cập nhật:** 24/10/2026
> ⚠️ Barem nhắc tới K1–K8 nhưng chưa có định nghĩa chính thức. Bảng dưới là **bản suy luận** của nhóm theo lộ trình 11 buổi. Khi TA cung cấp bản chính thức, sửa bảng định nghĩa và ma trận phủ ở file này.

Quy tắc chấm: các use case nộp phải phủ đủ K1–K8, **thiếu mỗi mảng trừ 0,5 điểm**. Nhóm đặt mục tiêu mỗi K có ít nhất **hai** use case ở mức trọng tâm, để mất một use case cũng không mất K nào.

## Định nghĩa (suy luận)

| Mã | Mảng kiến thức | Buổi |
|---|---|---|
| K1 | Nền tảng LLM: prompt/context engineering, token và chi phí, prompt caching, structured output, function calling | B2, B7 |
| K2 | Agent loop và mẫu suy luận: ReAct, plan-then-execute, reflection, điều kiện dừng, phát hiện lặp, debug agent | B3 |
| K3 | Harness engineering: 12 lớp, guides/sensors, middleware, budget, grounding, handoff | B1, B4 |
| K4 | Tools và Agent Skills: thiết kế tool, SKILL.md, progressive disclosure, scripts | B4, B5 |
| K5 | RAG / knowledge harness: ingest, chunk, metadata, hybrid, rerank, grounding, citation, RAG eval | B6 |
| K6 | Memory, context management, state, workflow: LangGraph, checkpointer, resume, long-term memory, compaction, interrupt | B7, B8 |
| K7 | Verification và evaluation: golden dataset, metric, LLM-as-judge có hiệu chuẩn, trajectory eval, CI | B9 |
| K8 | Multi-agent, MCP, bảo mật, governance, observability: handoff, MCP server/client, prompt injection, permission, audit log, tracing | B10, B11 |

## Ma trận phủ

● trọng tâm · ○ có dùng

| | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 |
|---|---|---|---|---|---|---|---|---|
| [UC1 Brand](use-cases/UC1-brand-analysis.md) | ● | ○ | ○ | ● | ○ | ● | ○ | ○ |
| [UC2 Query Universe](use-cases/UC2-query-universe.md) | ● | | ○ | ○ | ○ | | ● | |
| [UC3 Research](use-cases/UC3-research-evidence.md) | ○ | ● | ● | ● | ● | ● | ● | ● |
| [UC4 Writer](use-cases/UC4-geo-writer.md) | ● | ● | ● | ● | ○ | ● | ● | |
| [UC5 Fact-check + Editor](use-cases/UC5-factcheck-editor.md) | ○ | ● | ● | ○ | ● | ○ | ● | ● |
| [UC6 Schema](use-cases/UC6-schema-markup.md) | ● | | ● | ● | | | ● | |
| [UC7 Visibility](use-cases/UC7-ai-visibility.md) | ○ | | ○ | | ● | | ● | ○ |
| [UC8 Publish](use-cases/UC8-approve-publish.md) | ○ | ○ | ● | ○ | | ● | ● | ● |

## Số use case trọng tâm mỗi K

| K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 |
|---|---|---|---|---|---|---|---|
| 4 | 3 | 5 | 4 | 3 | 4 | 7 | 3 |

Nguồn: [KE_HOACH_DO_AN.md](KE_HOACH_DO_AN.md) mục 3.2.
