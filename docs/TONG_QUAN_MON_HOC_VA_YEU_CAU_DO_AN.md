# Tổng quan môn SE373 và yêu cầu đồ án cuối kỳ

> **Mục đích tài liệu:** ghi lại cách hiểu chung của nhóm về môn học và về đồ án cuối kỳ, làm điểm tựa cho mọi quyết định trong [KE_HOACH_DO_AN.md](../KE_HOACH_DO_AN.md).
> **Nguồn:** slide Buổi 1, 2, 3, 4, 6, 7 (thư mục `slide/`), trang tương tác `code-mode-explainer.html` của Buổi 7, bài làm Buổi 1–4, ảnh đề tài và ảnh barem chấm đồ án.
> **Cập nhật:** 24/10/2026

---

## 1. Thông tin môn học

| Mục | Nội dung |
|---|---|
| Mã và tên môn | SE373, Kỹ thuật xây dựng hệ thống Agentic AI (Khoa Công nghệ Phần mềm, UIT) |
| Giảng viên lý thuyết | TS. Đỗ Trọng Hợp, ThS. Ngô Ngọc Đăng Khoa, ThS. Phạm Hoàng Hải |
| Giảng viên thực hành | Bùi Cao Doanh, Dương Nguyễn Phương Nam, Nguyễn Hiếu Nghĩa, Nguyễn Ngọc Quí, Nguyễn Thị Hoàng Anh, Quan Chí Khánh An |
| Bản chất môn | **Môn kỹ thuật hệ thống**, không phải môn viết prompt, không phải môn giới thiệu LangChain, không phải môn dạy dùng ChatGPT. Model được gọi như một dịch vụ ngoài, không huấn luyện model. |
| Câu hỏi trung tâm | Làm sao xây một hệ thống **đáng tin cậy** từ một thành phần **không tất định, không đáng tin cậy** (LLM)? |

### 1.1. Chuẩn đầu ra (G1–G6)

| Mã | Mục tiêu |
|---|---|
| G1 | Kiến thức nền tảng về LLM, AI agent và các thành phần của hệ thống Agentic AI |
| G2 | Phân tích yêu cầu và thiết kế kiến trúc theo tư tưởng **agent = model + harness** |
| G3 | Xây dựng và tích hợp agent với công cụ, dữ liệu, bộ nhớ, truy xuất tri thức |
| G4 | Thiết kế workflow: trạng thái, điều phối, phối hợp nhiều agent, tích hợp MCP |
| G5 | Kiểm thử, đánh giá, quan sát và cải tiến độ tin cậy |
| G6 | Thái độ có trách nhiệm trong thiết kế và sử dụng hệ thống Agentic AI |

### 1.2. Cơ cấu điểm môn

| Thành phần | Tỷ trọng | Hình thức |
|---|---|---|
| Quá trình | 10% | Quiz trên lớp, bài tập, thảo luận tình huống; chấm qua QR mỗi buổi |
| Thực hành | 40% | 6 bài lab (TH1–TH6), nộp qua GitHub, có CI checklist chấm tự động |
| **Đồ án cuối kỳ** | **50%** | Nhóm 5 SV, ba vòng: **checklist repo → video demo → vấn đáp** |

### 1.3. Các trường hợp rớt môn hoặc mất điểm nặng
- Vắng quá **3 buổi lý thuyết** (tính tổng, không cần liên tiếp).
- Không dự đủ buổi thực hành, buổi demo tiến độ và buổi vấn đáp đồ án (cả ba bắt buộc).
- Nộp muộn hoặc sai quy định thì bị xem là không nộp.
- Gian lận học thuật, **kể cả nộp sản phẩm do AI tạo mà không hiểu và không kiểm chứng**.
- **Commit API key vào repository**, kể cả đã xoá ở commit sau ("Git không quên").
- Đóng góp không tương xứng: điểm cá nhân được điều chỉnh theo commit history và vấn đáp.

### 1.4. Quy tắc dùng AI (ba điều kiện cùng lúc)
1. **Minh bạch:** báo cáo ghi rõ dùng công cụ nào, cho phần việc nào.
2. **Kiểm chứng:** bắt buộc kiểm chứng output của AI; có trích dẫn thì phải mở nguồn đối chiếu; trích dẫn đủ mã nguồn, tài liệu, prompt, dữ liệu, tool, skill, MCP server.
3. **Giải thích được:** khi vấn đáp, thầy chỉ một hàm bất kỳ trong repo và hỏi "giải thích dòng này". Câu trả lời *"Cái đó AI viết, em không rõ"* bị coi là gian lận.

---

## 2. Nội dung môn học

### 2.1. Lộ trình 11 buổi và 6 bài thực hành

| Buổi | Nội dung | Lớp harness chính | Lab |
|---|---|---|---|
| 1 | Tổng quan LLM và Agentic AI | khung tổng thể | TH1 |
| 2 | Nền tảng LLM cho agent | context | TH1 |
| 3 | Agent fundamentals (agent loop) | | TH2 |
| 4 | Harness engineering, Prompt → Reusable Skills | cả 12 lớp | TH5 |
| 5 | Tool use và Agent Skills | tools, skills, permission | TH2 |
| 6 | RAG, knowledge harness | retrieval | TH3 |
| 7 (21/10) | Memory, context engineering, prompt caching | memory, state, context | TH4 |
| 8 | Workflow orchestration (LangGraph) | workflow, state | TH4 |
| 9 | Verification và evaluation | verification | TH5 |
| 10 | Multi-agent và MCP | handoff, tools | TH6 |
| 11 | Security, governance, observability | permission, logging, human approval | TH6 |

Các bài thực hành: TH1 môi trường và LLM API · TH2 agent loop và skill · TH3 RAG · TH4 memory/state/workflow · TH5 agent-readable repo và verification · TH6 multi-agent, MCP, an toàn.

### 2.2. Buổi 1: Tổng quan và phân loại hệ thống AI
- Bản đồ khái niệm AI ⊃ GenAI ⊃ LLM. Cơ chế lõi của LLM là đoán token tiếp theo.
- **Bốn nấc tiến hoá:** completion → chat → tool use → agent. Quyền quyết định chuyển dần từ code sang model, đổi tính dự đoán lấy sự linh hoạt.
- **Bốn dạng ứng dụng:** Chatbot, RAG app, Workflow, Agentic. Agent *có thể* dùng RAG như một tool, nhưng một RAG app *không phải* agent.
- **Ba tiêu chí phân loại (bắt buộc trả lời khi bảo vệ đồ án):**
  1. **Ai quyết định bước tiếp theo?** Đọc code mà biết bước kế thì là workflow; chỉ lúc chạy mới biết thì là agent.
  2. **Ai giữ trạng thái?** Biến, DB, node graph thì hệ thống giữ; lịch sử hội thoại thì model giữ (rủi ro khi context đầy).
  3. **Ai dừng vòng lặp?** Hết bước trong code thì workflow; model nói "xong rồi" thì agent. Agent **bắt buộc** có rào chắn dừng cứng (số vòng, token, thời gian).
- **Ưu tiên workflow:** chỉ thêm độ phức tạp khi nó cải thiện kết quả một cách chứng minh được. Agent tốn khoảng 4× token so với chat, multi-agent khoảng 15×. Agent khó dự đoán và khó test hơn. Chỉ dùng agent khi không thể định sẵn các bước.
- **Agent = Model + Harness.** Model cấp năng lực, harness cấp độ tin cậy. Sinh viên không huấn luyện model; giá trị nằm ở việc xây harness.
- **Ba sự cố minh hoạ thiếu harness:** Cursor bịa chính sách (thiếu retrieval, verification, human approval); Air Canada bị toà bắt chịu trách nhiệm cho lời chatbot (output của agent là phát ngôn chính thức của tổ chức); GitHub MCP bị prompt injection qua issue công khai (thiếu permission, tools, context, logging). Đổi sang model thông minh hơn cũng không giải quyết được các vụ này.

### 2.3. 12 lớp harness

| Nhóm | Lớp | Chặn được gì |
|---|---|---|
| Đầu vào | 1. context | Model bị nhiễu, chi phí phình |
| | 2. tools | Không làm được gì, hoặc làm được thứ không nên làm |
| | 3. skills | Cùng một tác vụ nhưng thiếu nhất quán |
| | 4. retrieval | Ảo giác do thiếu dữ liệu, suy luận từ dữ liệu lỗi thời |
| Trạng thái và quy trình | 5. memory | Hỏi lại thông tin đã biết, nhớ dữ liệu cần xoá |
| | 6. state | Mất tiến trình khi phiên đứt, không resume được |
| | 7. workflow | Quy trình rối loạn, không khôi phục được |
| | 8. verification | Báo hoàn thành khi task vẫn lỗi |
| An toàn và con người | 9. permission | Leo thang đặc quyền, phá hoại dữ liệu |
| | 10. logging | Mất dấu vết điều tra, phải tin lời agent tự khai |
| | 11. human approval | Thao tác không hoàn tác được bị kích hoạt tự động |
| | 12. handoff | Đứt gãy thông tin giữa các agent, với con người, qua các phiên |

### 2.4. Buổi 2: Nền tảng LLM-powered app
- LLM API gồm request (model, messages, generation parameters, schema hoặc tool) và response (output, finish reason, tool call, usage). Các role của message: system/developer, user, assistant, tool.
- **Token:** tiếng Việt tốn token hơn tiếng Anh (1,6–2,5× tuỳ tokenizer). Không ước tính token bằng `len(text.split())`.
- **Context window:** lost in the middle, context rot. Chi phí nhiều bước tăng vì mỗi bước gửi lại toàn bộ context. Prompt caching giảm chi phí nhưng không làm model hiểu tốt hơn.
- **Prompt engineering và context engineering:** cấu trúc prompt (role, context, yêu cầu, input, ràng buộc, các bước, output, ví dụ), thẻ XML, zero/one/few-shot, Chain of Thought, prompt template có version.
- **Structured output:** JSON Schema (enum, required, `additionalProperties: false`), Pydantic, constrained output. Schema phải có trạng thái hợp lệ cho trường hợp thiếu dữ liệu. **Schema kiểm tra cấu trúc, không kiểm tra tính đúng đắn của nội dung.**
- **Function calling:** model chỉ *đề xuất* lời gọi; **application thực thi và validate**. Đúng kiểu không đồng nghĩa đúng ý nghĩa.
- Một lần function call chưa phải agent; cần thêm vòng lặp và điều kiện dừng.

### 2.5. Buổi 3: Agent fundamentals
- **agent = goal + tools + loop + termination.** Goal mô tả trạng thái cần đạt, không phải danh sách bước. Thiếu termination là lỗi tốn kém nhất.
- **Vòng lặp 5 chặng:** dựng ngữ cảnh → model đề xuất tool → harness gọi tool → ghi kết quả → xét điều kiện dừng. Chỉ chặng 2 thuộc về model, bốn chặng còn lại là code của mình.
- Observation nên là dữ liệu có cấu trúc (JSON), không phải HTML thô. Chi phí lịch sử tăng xấp xỉ theo bình phương số vòng.
- **Ngân sách cứng:** số bước, token, thời gian, tiền.
- **Mẫu suy luận và khi nào dùng:**

| Mẫu | Chọn khi | Rủi ro chính |
|---|---|---|
| ReAct | Không đoán được số bước | Lặp vô hạn, trôi mục tiêu |
| Plan-then-execute | Cần duyệt trước | Kế hoạch lỗi thời |
| Lai (ReAct + Plan) | Tác vụ dài, môi trường biến động | Khó debug hơn |
| Reflection | Có tín hiệu kiểm chứng bên ngoài | Nhân đôi chi phí |

- "Có tool chưa chắc agent dùng tool": cần system prompt và harness ép dùng.
- **5 điều kiện dừng:** đạt mục tiêu · hết ngân sách · phát hiện lặp · bế tắc · cần con người. Checklist chạy sau mỗi vòng theo thứ tự: kiểm quyền *trước* khi thực thi tool; tiêu chí hoàn thành, lặp, bế tắc, rồi **ngân sách kiểm cuối cùng** (đặt ngân sách lên đầu thì mọi lỗi đều báo về "hết ngân sách" và mất khả năng chẩn đoán).
- **Sensor computational** (test, linter, validator: tất định, không tốn token) được ưu tiên hơn **sensor inferential** (LLM chấm LLM).
- **Tiêu chí hoàn thành phải khách quan, kiểm bằng code** (vị từ code, schema hợp lệ, kiểm chứng chéo bằng cách đọc lại, người duyệt), không tin model tự tuyên bố.
- **Phát hiện lặp là code tự viết:** trùng (tool, args), trùng observation, không tiến triển qua N vòng.
- **Debug agent 4 bước:** tái hiện → khoanh vùng vòng sai đầu tiên → phân loại lỗi → đặt kiểm tra. **Bốn failure mode:** lặp không tiến bộ · bịa đặt · quên yêu cầu ban đầu · tin dữ liệu sai. Hai lỗi cuối cho log "sạch" nên khó thấy.
- **Handoff tốt:** trạng thái (kể cả tác dụng phụ đã xảy ra), những gì đã thử, một câu hỏi cụ thể mà người nhận trả lời được trong 30 giây.
- API chuẩn: `create_agent` của LangChain 1.x, middleware (`ModelCallLimitMiddleware`…), LangGraph.

### 2.6. Buổi 4: Từ prompt engineering tới reusable skills
- Cloud agent (sandbox của vendor) và local agent (chạy trên máy, toàn quyền file và lệnh).
- Thêm một ít hướng dẫn giúp model rẻ đạt kết quả gần model đắt và giúp các lần chạy nhất quán.
- **Skill** = `SKILL.md` (frontmatter `name`, `description`) + `references/` + `scripts/` + `examples/`. Prompt phải gõ lại mỗi lần; skill thiết lập một lần, agent dùng lại, chia sẻ được.
- **Thiết kế skill:** `description` là phần duy nhất agent luôn đọc (quyết định trigger); workflow khoảng 5–8 bước, động từ đứng đầu; trỏ tới file chi tiết thay vì chép nội dung; **progressive disclosure**; SKILL.md dưới 200 dòng; nêu rõ output (đó chính là tiêu chí verification); **việc chính xác (đếm, validate, convert) giao cho script, việc suy luận giao cho LLM**; **bước cuối luôn là kiểm tra**, chỉ báo xong khi kiểm tra PASS.
- **Kiểm thử skill:** trigger, false-trigger, functional, quality, efficiency, safety.
- Năm lỗi thường gặp: SKILL.md khổng lồ, description mơ hồ, một skill ôm nhiều nhiệm vụ, bắt LLM làm việc của máy, thiếu bước kiểm tra.
- Cách tạo skill thực tế: chọn việc agent làm chưa tốt → làm cùng agent tới khi đạt → ghi lại cách làm → đóng gói → chạy lại nhiều trường hợp → quản lý như mã nguồn. Có thể để agent viết skill, nhưng **bắt buộc đọc lại**.

### 2.7. Buổi 6: RAG, knowledge harness
- RAG là lớp harness retrieval, quyết định model được đọc gì. So với fine-tuning và nhồi context, RAG cập nhật được tức thì, trích dẫn được và xoá được dữ liệu.
- **Kiến trúc hai pha:** nạp offline (load → clean → chunk + metadata → embed → index) và truy vấn online (query transformation → query embedding → hybrid retrieval → rerank → prompt assembly → generation → **citation verification**). **Hai pha bắt buộc dùng cùng một embedding model** (assert khoá model; đổi model thì phải ingest lại).
- **Chunking:** cắt theo cấu trúc (heading, endpoint, AST, section, nguyên issue), không cắt cố định theo ký tự. Tiền xử lý phải tất định và có log. Contextual Retrieval giảm khoảng 49% lỗi truy xuất (67% nếu có rerank).
- **Chunk = text + metadata** (source_type, path, version, line, heading_path, symbol, status, doc_id/chunk_id). Không có metadata thì không trích dẫn được. **Upsert idempotent:** xoá chunk cũ của tài liệu rồi mới ghi.
- **Embedding** mạnh với văn xuôi, yếu với định danh (mã lỗi, mã số). **Hybrid** = dense + BM25, hợp nhất bằng **RRF**: `Σ 1/(k + rank)` với k = 60. Không cộng thẳng điểm số của hai thang khác nhau.
- **Retrieval cascade:** lấy dư (khoảng 50 + 50) → RRF (khoảng 40) → **cross-encoder rerank** → giữ 3–5 chunk. Reranker chỉ sắp lại; chunk chưa lấy về thì không cứu được.
- **Query transformation:** rewriting, multi-query, step-back, HyDE, decomposition.
- **Grounding:** chỉ trả lời từ tài liệu, thiếu căn cứ thì từ chối (escape hatch). Năm quy tắc bám nguồn. **Citation phải kiểm chứng bằng chương trình.**
- **4 retrieval failure mode:** miss (Recall@k) · wrong chunk (Precision@k) · nguồn mâu thuẫn (version/status) · ảo giác dù có nguồn (Faithfulness, Abstention). Ngữ cảnh nửa vời nguy hiểm hơn không có ngữ cảnh.
- **Golden dataset** 20–30 câu: 1/3 khái niệm, 1/3 định danh, 1/3 bẫy, **cộng 3–5 câu không có đáp án**. Chỉ số: Recall@k, Precision@k, MRR, Faithfulness, Citation Existence (bắt buộc 100%), Abstention Rate.
- Just-in-time và agentic retrieval: đóng gói retrieval thành tool cho agent.
- **Bài tập của buổi này gắn thẳng vào đồ án:** làm trên branch `feature/rag`: ingest có metadata, hybrid + rerank có trích dẫn, golden dataset 20 câu (3–5 câu không đáp án), bảng so sánh **tối thiểu 2 cấu hình**, báo cáo có bảng số liệu và **một ca thất bại**.

### 2.8. Buổi 7: Memory, context engineering và prompt caching
Giảng viên: ThS. Ngô Ngọc Đăng Khoa, ngày 21/10/2026. Buổi học trả lời ba câu hỏi của harness: **Remember** (điều gì phải còn khi sang session mới), **Manage** (context chứa gì sau hàng trăm tool call), **Reuse** (phần tính toán nào dùng lại được qua hàng trăm lần gọi LLM). Tình huống xuyên suốt: một task kéo dài 3 ngày, đã đọc hàng trăm file và log, rồi user yêu cầu làm tiếp trên session mới.

**Phần I: Persistent memory**
- **LLM stateless, agent stateful.** Mỗi lần gọi API chỉ thấy dữ liệu của request đó. Harness quyết định lưu gì, truy xuất gì, đưa lại gì vào request kế tiếp.
- **Bốn khái niệm cần tách bạch:**

| Thành phần | Trả lời câu hỏi | Ví dụ |
|---|---|---|
| State | Đang làm đến đâu? | `current_step=run_tests` |
| History | Đã có tương tác gì? | Tin nhắn user và tool |
| Memory | Điều gì cần nhớ? | Project dùng PostgreSQL |
| Context | LLM thấy gì lúc này? | Rules, memory đã chọn và task |

- Memory nằm trên ổ đĩa **không tự vào context**: phải có bước retrieval và injection.
- **Ba loại memory:** session memory (mục tiêu, tiến độ, lỗi chưa xử lý, bước kế tiếp) · persistent memory (sở thích user, quy ước project, quyết định, bài học) · instructions và policies (rules bắt buộc, có phạm vi và độ ưu tiên). Không phải dòng chat nào cũng là memory.
- **Case study AGENTS.md / MEMORY.md:** `AGENTS.md` theo project và theo user; `MEMORY.md` là index ngắn luôn được nạp; chi tiết nằm ở file chủ đề (`memory/auth.md`…) và chỉ nạp khi cần. Nhồi toàn bộ memory mỗi lượt thì context bloat quay lại.
- **Memory lifecycle:** cần chính sách ghi, đọc, sửa và **quên**.
- **Memory sai và lỗi thời:** khi quy ước đổi (ví dụ JWT → session cookie), cách đúng là **đánh dấu bản cũ đã bị thay thế, lưu nguồn và thời điểm**; không giữ cả hai như quy định hiện hành, cũng không xoá sạch dấu vết. Memory phải giải quyết xung đột, không chỉ append.
- **Các mẫu kiến trúc:** Markdown instructions · memory tools (agent tự quyết lúc đọc, ghi) · progressive disclosure (đọc index trước) · file-system/searchable memory · out-of-band curation (phân tích nhiều session để cập nhật memory).

| Thiết kế lưu trữ | Điểm mạnh | Đổi lại |
|---|---|---|
| JSON, Markdown | Dễ làm, dễ kiểm tra | Khó tìm và khó xử lý xung đột khi lớn |
| SQLite + metadata | Truy vấn, update rõ ràng | Cần schema và migration |
| Vector retrieval | Tìm theo ngữ nghĩa | Chi phí embedding, khớp nhầm |
| Index + topic files | Lazy load, dễ đọc | Phải giữ index chính xác |

**Phần II: Giữ context nhỏ gọn (compaction và Code Mode)**
- **Context window là working set**, không phải kho dữ liệu. Gồm instructions, memory đã chọn, history, tool result, dữ liệu retrieve, và **phải chừa chỗ cho output**. Nhiều dữ liệu hơn không có nghĩa quyết định tốt hơn.
- **Tool-output bloat:** `read_file` 2.000 dòng, `run_tests` 7.000 dòng, `grep` 1.500 dòng, trong khi agent chỉ cần 3 test lỗi, nguyên nhân khả dĩ, file liên quan và thử nghiệm kế tiếp. Raw output nên archive ra ngoài, không nằm mãi trong context.
- **Compaction là checkpoint, không phải bản recap của chat.** Mục tiêu là đủ thông tin để agent làm tiếp chính xác.

| Kỹ thuật | Cách làm | Rủi ro |
|---|---|---|
| Truncation | Bỏ tin nhắn cũ | Mất ràng buộc |
| Tool-output pruning | Loại log thô, log trùng | Bỏ sót bằng chứng |
| Summary | LLM rút gọn history | Bịa, bỏ sót |
| Structured checkpoint | Lưu state theo schema | Thiếu trường quan trọng |
| Incremental summary | Nén theo từng giai đoạn | Lỗi tích luỹ |
| Selective keep/drop | Giữ nguyên các đoạn quan trọng | Chọn nhầm đoạn |

- **Structured checkpoint** gồm các trường `goal`, `current_state`, `constraints`, `findings`, `failed_attempts`, `files`, `next_action`. Kiểm chứng checkpoint bằng cách cho agent làm tiếp từ checkpoint đó.
- **Selective compaction:** KEEP quyết định thiết kế, lỗi chưa giải quyết, yêu cầu bắt buộc · TRUNCATE output test dài còn vài dòng lỗi chính · DROP log trùng, thử nghiệm thất bại đã có kết luận, dữ liệu dễ tái tạo. Nguyên tắc: giữ chính xác khi cần, nén khi có thể, loại khi an toàn.
- **Khi nào compact:** context vượt ngưỡng an toàn · tool output và history lặp nhiều · xong một milestone · trước khi cold-start một context rất lớn. **Không đợi context đầy mới compact.** Compaction là một "controlled reboot" của working context.
- **Code Mode:** model trả một tool call `run_code` kèm chương trình → runtime chạy chương trình, chương trình gọi các tool → model chỉ nhận kết quả đã xử lý. Tool giữ nguyên; khác ở chỗ **chương trình quyết định chuỗi lời gọi tool thay cho LLM**. Ví dụ trong slide: đọc 100 file trong runtime để đếm TODO, chỉ 5 kết quả đi vào LLM.
- Chạy code trong runtime riêng **chưa phải sandbox bảo mật**. Production cần sandbox, kiểm quyền, timeout, giới hạn tài nguyên.

**Bổ sung từ trang tương tác "Code-mode-explainer" (Moodle Buổi 7)**
- **Quy mô:** ví dụ đếm TODO thì Code Mode dùng 1 tool call `run_code` thay cho 101 tool call, và chỉ 2 LLM call (một lần viết code, một lần đọc kết quả). Với giả định 100 file × 1.200 token, native cần 102 LLM call, context đỉnh khoảng 127k token, tổng input khoảng 6,6M token (≈ 33 USD ở giá 5 USD/1M). Code Mode chỉ tốn khoảng 6.400 token (≈ 0,03 USD), ít hơn khoảng 1.000 lần. Gọi nhiều tool song song giảm được số LLM call nhưng không giảm context đỉnh. Prompt caching giảm giá phần prefix nhưng không giảm số token trong context.
- **Kiến trúc trong harness:** LLM viết code → **Dispatcher** nhận `run_code` → **Runtime** (V8 isolate, Deno, Web Worker, container Python) chạy code, biến trung gian chỉ sống ở đây → **proxy `tools.*`** gửi RPC về harness → **Permission** cho phép hoặc chặn → **tools thật** (file, API, DB). Dữ liệu thô dừng ở runtime; giá trị `return` đi qua **output cap** (cắt và định dạng) rồi mới vào `messages[]`. Runtime không được có network, file system hay biến môi trường; mọi truy cập ra ngoài phải đi qua proxy.
- **Ba lớp khai báo:**

| Lớp | Nằm ở đâu | LLM có thấy không |
|---|---|---|
| Tool trong API | Tham số `tools` của request: chỉ `run_code`, thêm vài native tool nếu là hybrid | Có, dạng JSON schema; model sinh `tool_call` theo tên này |
| SDK `tools.*` | Description của `run_code`, system prompt, hoặc file `sdk/*.d.ts` để model tự tìm | Có, dạng type definitions; model chỉ dùng trong code |
| Implementation | Code harness: hàm tool thật, proxy, permission check, credential | Không |

- SDK có thể **sinh tự động từ JSON schema** của tool có sẵn (Cloudflare làm vậy với MCP server), nên chuyển sang Code Mode không phải viết lại tool. Khi SDK lớn có hai cách đưa tài liệu cho model: **A. nhúng toàn bộ type definitions vào description** (ví dụ 40 hàm ≈ 4.950 token mỗi request, cache được nhưng vẫn chiếm context) hoặc **B. progressive disclosure** (index nhỏ, đọc chi tiết khi cần; task dùng 2 hàm chỉ tốn ≈ 600 token), cùng nguyên tắc với memory index ở Phần I.
- **Cấu hình hybrid:** `run_code` cho việc lặp và lọc, cộng vài native tool cho việc cần đọc hiểu (`read_file`) hoặc cần người trả lời (`ask_user`).
- **Sáu bẫy và cách chặn:**

| Bẫy | Biểu hiện | Cách chặn |
|---|---|---|
| Lọc sai mà không biết | Regex `/TODO/g` bỏ sót `todo:` và `FIXME`; kết quả trông hợp lý nhưng sai | Trả kèm số liệu kiểm chứng: số file đã quét, file đọc lỗi, tổng số match |
| Bloat quay lại | Code `return` nguyên file log | Code phải lọc trước khi trả; harness áp output cap và ghi rõ đã cắt bao nhiêu |
| Vòng lặp vô hạn | `while(true)` làm harness chờ mãi | Timeout, giới hạn CPU, bộ nhớ, số tool call |
| Prompt injection → rò rỉ dữ liệu | Dòng log bảo AI đọc `.env` rồi `http_post` ra ngoài | Permission check ở proxy (chặn đọc file ẩn, chặn `http_post`) |
| Runtime riêng chưa phải sandbox | Code dùng `fetch` đi vòng qua proxy, permission không ghi nhận | Sandbox thật (V8 isolate không network, container không mạng, gVisor, Firecracker) |
| Lỗi code | Exception, mỗi lần retry tốn thêm một lượt LLM | SDK có type rõ; lỗi ngắn gọn (`ENOENT: path`), không trả stack trace dài |

- **Khi nào dùng:** Code Mode hợp với task nhiều tool call, dữ liệu lớn, phép biến đổi xác định (lọc, đếm, join, tổng hợp). Native hợp khi model cần đọc hiểu nội dung hoặc mỗi bước cần quyết định mới. Đáp án quiz trong trang:

| Tình huống | Chọn | Lý do |
|---|---|---|
| Đọc README.md rồi giải thích kiến trúc | Native | Cần đọc hiểu, một lần `read_file` là đủ |
| Đếm request lỗi 500 theo endpoint trong 30 file log | Code Mode | Nhiều file, phép đếm xác định (dạng bài B2) |
| Lấy 2.000 issue qua API phân trang, tìm issue thiếu label | Code Mode | Native cần khoảng 100 LLM call |
| Sửa một hàm sau khi user góp ý | Native | Ít lời gọi, cần suy luận trên code |
| Đồng bộ khách hàng từ sheet sang CRM, email không đi qua model | Code Mode | Dữ liệu cá nhân đi trong runtime, model chỉ thấy số lượng |
| Debug test fail với 7.000 dòng output | Kết hợp | Code lọc còn vài test lỗi, rồi model đọc file và sửa bằng native |

- **Bash là Code Mode tối giản:** agent có tool bash thì model viết script, chỉ stdout vào context. Khác biệt với Code Mode đầy đủ: bash truy cập thẳng OS và network, phân quyền theo process, trace chỉ thấy lệnh và stdout, phải tự giữ credential; Code Mode đi qua proxy, phân quyền theo từng tool và tham số, trace từng tool call, credential nằm ở harness, nhưng phải tự dựng runtime và proxy. **Cách đo cho B2:** so `usage.input_tokens` giữa lần agent `read_file` từng log và lần agent chạy script.
- **Code Mode và compaction bổ sung cho nhau:** Code Mode làm context tăng chậm hơn nên ít phải compact. Mỗi lần compact bớt đi là bớt một lần mất cache prefix và một lần có nguy cơ mất thông tin khi tóm tắt.
- Nguồn trang dẫn: Cloudflare, *Code Mode: the better way to use MCP*; Anthropic, *Code execution with MCP: building more efficient AI agents*. Số token trong trang là ước lượng hoặc minh hoạ.

| Tiêu chí | Compaction | Code Mode |
|---|---|---|
| Thời điểm | Sau khi dữ liệu đã tích luỹ | Khi chạy tool |
| Mục tiêu | Rút gọn working context | Tránh đưa kết quả trung gian vào context |
| Rủi ro | Mất state, mất ràng buộc | Code lỗi, quyền truy cập |
| Kết hợp | Checkpoint cho session dài | Làm chậm tốc độ phình context |

**Phần III: Prompt caching và đổi model**
- **Prompt cache khác response cache.** Response cache trả lại câu trả lời cũ cho câu hỏi cũ; prompt cache (KV cache) dùng lại phần tính toán của input khi **prefix trùng khớp**. Token đã cache vẫn nằm trong context, chỉ rẻ và nhanh hơn khi cache hit.
- **Chi phí input tăng theo history:** ví dụ trong slide 51k → 55k → 59k → 87k token ở turn 1, 2, 3, 10. Input mỗi request tăng tuyến tính, nên tổng input qua n request tăng theo bậc hai.
- **Prefix cache invalidation:** thay đổi càng sớm trong prefix thì càng mất nhiều cache phía sau.
- **Thói quen thân thiện với cache:** phần tĩnh đặt trước, phần động đặt sau · giữ tool definitions ổn định · ưu tiên history append-only khi cần reuse · **đo `cached_tokens`, cache write, cache read, không đoán**.
- **Warm, cold, TTL:** mỗi provider có TTL và chính sách đọc/ghi cache riêng. Keep-alive request vẫn tính phí và không chắc gia hạn được toàn bộ cache, nên **cache warming là khoản đầu tư**: chỉ đáng khi lợi ích kỳ vọng lớn hơn phí keep-alive.
- **Compaction có thể phá cache prefix.** Giữ 50k token đã cache có thể rẻ hơn compact còn 12k nhưng prefix đổi; phải tính cả cache read/write, lượt gọi compaction, output và các lượt sau.
- **So sánh model bằng tổng chi phí để đạt cùng chất lượng**, không chỉ bằng giá niêm yết. Ba chiến lược: **A: giữ ấm model A** (phí keep-alive) · **B: để nguội rồi compact** (phí compact, mất thông tin) · **C: đổi sang model B** (prefill lại từ đầu, chịu chất lượng của B).
- Dữ liệu mô phỏng trong slide (USD / 1M token): Model A input 5,00, cached 0,50, output 20,00, đang có 50k token cache; Model B input 1,00, cached 0,10, output 5,00, chưa có cache. Request kế tiếp: 2k input mới, 1k output. *Nhóm tự tính:* A warm ≈ 0,025 + 0,010 + 0,020 = **0,055 USD**; B cold ≈ 0,052 + 0,005 = **0,057 USD**. Chênh khoảng 0,002 USD, nên keep-alive cho A phải rẻ hơn mức này mới có lời cho một lượt.

**Ba challenge trên lớp (mỗi bài 30 phút)**
- **A: persistent memory.** Agent nhớ quy ước dự án qua nhiều session và cập nhật khi quy ước đổi. Chứng minh bằng cách in ra phần memory đã inject vào context.
- **B: context management.** B1 compact một session dài mà agent vẫn nhớ lỗi đang điều tra, cách đã thử, bước tiếp. B2 dùng Code Mode trả lời câu hỏi trên nhiều file log mà raw log không vào context; đo input token qua `usage`.
- **C: cache-aware model router.** Chọn warm, compact hay switch cho các kịch bản user quay lại sau 3 phút, sau 7 phút, 60% quay lại trong 10 phút; tìm điểm đổi quyết định. Không cần gọi API.

**Áp dụng cho đồ án VietCite Studio** (chi tiết ở [KE_HOACH_DO_AN.md mục 4.7](KE_HOACH_DO_AN.md))
- **Làm (P0):** memory lifecycle và đánh dấu `superseded` cho brand memory và editorial lessons; memory index + topic file; ghi phần memory đã inject vào trace; archive trang web và compact thành `ResearchCheckpoint` cho Researcher và Fact-Checker; bố cục prompt thân thiện với cache và đo cache hit rate; phân biệt response cache với prompt cache.
- **Dự phòng (P1):** Code Mode bản hybrid (`run_analysis` trong Docker không mạng) cho việc quét nhiều trang bảng giá. Nếu bị trễ thì cắt mục này đầu tiên.
- **Không làm:** cache-aware model router; chỉ phân tích chi phí trong báo cáo.
- **Ảnh hưởng tới chấm điểm:** UC3 lên mức trọng tâm K6; thêm dataset D10 (memory qua nhiều session); thêm 4 câu hỏi vấn đáp.

### 2.9. Các buổi sắp học (8–11)
LangGraph orchestration (B8), verification và evaluation (B9), multi-agent và MCP (B10), security, governance, observability (B11). Đồ án cần đón trước các nội dung này: checkpoint và resume, interrupt chờ người duyệt, eval dataset và trajectory, MCP server/client, permission, audit log, chống prompt injection.

---

## 3. Yêu cầu đồ án cuối kỳ

### 3.1. Hình thức
- Nhóm 5 sinh viên, chọn 1 trong 10 nhóm đề tài: Coding Agent, Code review agent, Helpdesk Agent, **GEO content writer Agent**, Interview Agent, IELTS Learning Agent, Business Ops Agent, Tour Guide Agent, Analytics Agent, AI Training Agent.
- **Mốc thời gian:** xác nhận nhóm và đề tài trước tuần 4 → **báo cáo tiến độ sau tuần 7** → **nộp và vấn đáp sau tuần 11** (ước tính khoảng 24–30/11/2026).
- **Ba vòng chấm:** checklist repo → video demo → vấn đáp.
- Khi bảo vệ phải trả lời chính xác **ba câu hỏi phân loại** (mục 2.2) cho hệ thống của nhóm.

### 3.2. Đề tài của nhóm: GEO content writer Agent (TA phụ trách: DNPNam)
Nguyên văn yêu cầu:
> Agent viết bài tiếng Việt tối ưu để được các công cụ AI (ChatGPT, Gemini, Perplexity…) trích dẫn. Agent phân tích thương hiệu, sinh tập câu hỏi người dùng hay hỏi AI, nghiên cứu nguồn, viết theo giọng thương hiệu, có agent kiểm chứng số liệu và agent biên tập, sinh schema markup, đo mức độ được AI nhắc tới trước và sau khi có bài, xuất bản WordPress sau khi người duyệt.

Tách thành 10 yêu cầu chức năng, mỗi yêu cầu phải có trong sản phẩm cuối:

| # | Yêu cầu | Use case trong kế hoạch |
|---|---|---|
| R1 | Viết bài tiếng Việt tối ưu để được AI trích dẫn | UC4 |
| R2 | Phân tích thương hiệu | UC1 |
| R3 | Sinh tập câu hỏi người dùng hay hỏi AI | UC2 |
| R4 | Nghiên cứu nguồn | UC3 |
| R5 | Viết theo giọng thương hiệu | UC4 |
| R6 | Có **agent** kiểm chứng số liệu | UC5 (Fact-Checker) |
| R7 | Có **agent** biên tập | UC5 (Editor) |
| R8 | Sinh schema markup | UC6 |
| R9 | Đo mức độ được AI nhắc tới **trước và sau** khi có bài | UC7 |
| R10 | Xuất bản WordPress **sau khi người duyệt** | UC8 |

### 3.3. Barem chấm đồ án (thang 10, chiếm 50% điểm môn)

**Phần agent: tối đa 7,5 điểm**
- Mỗi use case **1,5 điểm**, chấm theo 3 tiêu chí, mỗi tiêu chí 0,5:
  - **Chức năng:** chạy đúng tiêu chí.
  - **Thiết kế harness:** đúng kỹ thuật.
  - **Kiểm chứng:** có eval và trace.
- **5 use case trọn điểm là đủ 7,5.** Làm thêm để bù use case chưa trọn điểm.

**Phần mềm: tối đa 2,5 điểm**

| Tiêu chí | Điểm |
|---|---|
| Sáng tạo | 0,5 |
| Độ phức tạp kỹ thuật | 0,75 |
| Độ hoàn thiện | 0,75 |
| Khối lượng | 0,5 |

Dạng desktop, web hoặc CLI; **phải tích hợp agent thật**.

**Điều kiện và điều chỉnh**
- **Phủ đủ 8 mảng kiến thức:** các use case nộp phải phủ K1–K8; **thiếu mỗi mảng trừ 0,5**.
- **Điểm cá nhân** = điểm nhóm × hệ số vấn đáp (0–1,0) của từng thành viên.
- **Vi phạm:** lộ API key **trừ 1,0**; sao chép hoặc gian lận thì **đồ án 0 điểm**.

### 3.4. Tám mảng kiến thức K1–K8 (bản suy luận, chưa có bản chính thức)
> ⚠️ Barem nhắc tới K1–K8 nhưng không có định nghĩa trong slide hay tài liệu của nhóm. Bảng dưới đây do nhóm suy ra từ lộ trình 11 buổi. **Cần hỏi TA để lấy bản chính thức** và sửa lại ma trận phủ trong kế hoạch.

| Mã | Mảng kiến thức (suy luận) | Buổi |
|---|---|---|
| K1 | Nền tảng LLM: prompt/context engineering, token và chi phí, structured output, function calling | B2 |
| K2 | Agent loop và mẫu suy luận: ReAct, plan-then-execute, reflection, điều kiện dừng, phát hiện lặp, debug | B3 |
| K3 | Harness engineering: 12 lớp, guides/sensors, middleware, budget, grounding, handoff | B1, B4 |
| K4 | Tools và Agent Skills | B4, B5 |
| K5 | RAG / knowledge harness | B6 |
| K6 | Memory, context management (compaction, Code Mode, prompt caching), state, workflow orchestration (LangGraph), human-in-the-loop | B7, B8 |
| K7 | Verification và evaluation | B9 |
| K8 | Multi-agent, MCP, bảo mật, governance, observability | B10, B11 |

### 3.5. Mỗi use case cần thể hiện được gì (để ăn trọn 1,5 điểm)
1. **Chức năng:** tiêu chí chấp nhận đo được, chạy được trong demo.
2. **Thiết kế harness:** chỉ ra các lớp harness đã dùng, vì sao dùng, ở file nào. Trả lời được ba câu phân loại cho use case đó.
3. **Kiểm chứng:** golden dataset, metric có ngưỡng, kết quả thực đo, trace mẫu, **ít nhất một ca thất bại** được phân tích theo quy trình debug 4 bước.

### 3.6. Những điều giám khảo sẽ kiểm tra (suy ra từ slide)
- **Repo:** dễ đọc cho người và cho agent (README, AGENTS.md), CI xanh, không có secret trong toàn bộ lịch sử git, commit history phản ánh đóng góp của từng người.
- **Video demo:** các use case chạy thật trên phần mềm có tích hợp agent thật.
- **Vấn đáp:** ba câu phân loại; giải thích một hàm bất kỳ; vì sao chọn workflow hay agent ở từng chỗ; điều kiện dừng; cách kiểm chứng; minh bạch phần nào dùng AI hỗ trợ.

---

## 4. Các quyết định đã chốt

| Vấn đề | Quyết định |
|---|---|
| Đề tài | GEO content writer Agent, tên sản phẩm **VietCite Studio** |
| Dự án 8D Copilot (hackathon cũ) | **Gạt bỏ hoàn toàn.** Không dùng code, không dùng làm thương hiệu demo. Đồ án viết mới từ đầu theo kế hoạch. |
| Miền demo | SaaS quản lý bán hàng và hoá đơn điện tử cho hộ kinh doanh. Thương hiệu chính **"Tallyo"** (giả lập) trong thị trường thật (KiotViet, Sapo, MISA eShop…). Thương hiệu phụ **"Lâm Viên Coffee"** (giả lập) để kiểm tra tổng quát hoá. |
| Giao diện | Web: FastAPI (Python) + React |
| Stack agent | Python, LangChain 1.x `create_agent`, LangGraph (đồng bộ với các lab của môn) |
| API | DeepSeek (LLM chính) · Jina (embedding, rerank, reader, search) · Gemini (probe có Google Search grounding, judge độc lập; tuỳ chọn) |
| Thời gian | Khoảng 5 tuần, nhóm 5 người |

Chi tiết use case, phase, lịch và phân công: xem [KE_HOACH_DO_AN.md](../KE_HOACH_DO_AN.md).

---

## 5. Các điểm còn mở
1. **Danh sách K1–K8 chính thức:** cần hỏi TA.
2. **Ngày báo cáo tiến độ và ngày nộp, vấn đáp chính xác:** cần xác nhận theo lịch lớp. Buổi 7 đã học ngày 21/10/2026, nên mốc "báo cáo tiến độ sau tuần 7" đang tới gần.
3. **R3 (sinh câu hỏi) và R8 (schema markup)** là yêu cầu đích danh của đề, nhưng trong kế hoạch UC2 và UC6 đang xếp mức dự phòng (P1). Nên cân nhắc nâng lên mức bắt buộc để không thiếu chức năng đề yêu cầu.
4. **R9 (đo "sau khi có bài" trên AI thật):** bài chỉ đăng trên WordPress local thì các engine thật không đọc được. Kế hoạch đo phần "sau" bằng engine giả lập SGE-vi; cần ghi rõ giới hạn này trong báo cáo, hoặc bổ sung bước đăng công khai nếu muốn đo trên engine thật.
