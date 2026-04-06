# Individual Report: Lab 3 - Chatbot vs ReAct Agent

**Student Name:** Bùi Quang Hải\
**Student ID:** 2A202600006\
**Date:** 2026-04-06

------------------------------------------------------------------------

# I. Technical Contribution (15 Points)

Trong project này, em tập trung vào việc **mở rộng khả năng tính toán và
tích hợp tool cho ReAct Agent** thay vì để LLM tự xử lý toàn bộ logic.

**Modules Implemented:**\
- src/tools/ecommerce_tools.py\
- src/agent/agent.py\
- System Prompt

**Code Highlights:**\
- Xây dựng tool: def calc_total_price(price: float, quantity: int) -\>
str\
→ Giúp tính tổng tiền một cách deterministic, tránh việc LLM tự tính dễ
sai.

-   Đăng ký tool vào: ECOMMERCE_TOOLS_SPEC\
    → Cho phép Agent nhận diện và gọi tool đúng chuẩn ReAct.

-   Implement logic trong: \_execute_tool (class ReActAgent)\
    → Parse Action → gọi tool → trả về Observation cho vòng lặp tiếp
    theo.

**Documentation:**\
Đóng góp chính của em là chuyển phần **logic tính toán từ LLM sang Tool
layer**.\
Điều này giúp: - Giảm hallucination\
- Tăng độ chính xác\
- Làm rõ separation giữa reasoning (LLM) và execution (tool)

------------------------------------------------------------------------

# II. Debugging Case Study (10 Points)

**Problem Description:**\
Agent bị kẹt vòng lặp vô hạn do output không đúng format, cụ thể là
thiếu prefix **Action:**.

**Log Source:**\
logs/agent_telemetry.log

Ví dụ: {"event": "AGENT_ERROR_FORMAT", "data": {"content": "Thought: ...
Action: None required"}}

**Diagnosis:**\
- System Prompt chưa đủ strict\
- Few-shot examples chưa nhấn mạnh format\
- LLM sinh output tự nhiên thay vì tuân thủ schema

→ Parser (dựa trên RegEx) không đọc được → Agent fail loop

**Solution:**

-   Fix 1: Cải tiến System Prompt\
    → Bắt buộc dùng: Final Answer: nếu không cần tool

-   Fix 2: Feedback loop thông minh\
    → Khi lỗi format, không crash mà:

    -   Inject lỗi vào Observation\
    -   Cho LLM cơ hội tự sửa ở bước tiếp theo

 Sau khi fix: - Giảm vòng lặp vô hạn\
- Agent hội tụ nhanh hơn

------------------------------------------------------------------------

# III. Personal Insights: Chatbot vs ReAct (10 Points)

**Reasoning:**\
ReAct Agent vượt trội Chatbot nhờ khả năng **suy nghĩ từng bước
(Thought)**.

Ví dụ: - Chatbot: tự "bịa" giá, phí ship\
- Agent: 1. Check kho\
2. Áp dụng mã giảm giá\
3. Gọi tool tính tiền

→ Minh bạch và đúng logic hơn

------------------------------------------------------------------------

**Reliability:**\
Điểm yếu của ReAct: - Dễ lỗi format\
- Phụ thuộc tool\
- Latency cao

Trong khi: - Chatbot ổn định hơn\
- Nhưng thiếu khả năng xử lý bài toán phức tạp

------------------------------------------------------------------------

**Observation:**\
Observation đóng vai trò cực kỳ quan trọng: - Là feedback trực tiếp từ
environment\
- Nếu sai → Agent tự sửa\
- Nếu đúng → Agent tiếp tục reasoning

 Đây là điểm khác biệt lớn nhất so với chatbot truyền thống

------------------------------------------------------------------------

# IV. Future Improvements (5 Points)

**Scalability:**\
- Áp dụng async (Celery/Kafka)\
- Tránh block khi gọi API hoặc DB

**Safety:**\
- Thêm Supervisor LLM\
- Validate action arguments trước khi execute

**Performance:**\
- Dùng Vector DB + RAG\
- Chỉ load tool cần thiết\
→ Tránh vượt context window

------------------------------------------------------------------------

#  Final Reflection

Đóng góp chính của em không chỉ là viết tool, mà là: - **Định hình lại
cách Agent xử lý bài toán** - Tách rõ: - LLM → reasoning\
- Tool → execution

 Đây là bước quan trọng để đưa hệ thống từ demo sang production.
