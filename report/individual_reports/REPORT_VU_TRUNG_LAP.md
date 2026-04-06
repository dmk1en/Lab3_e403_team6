# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Vũ Trung Lập
- **Student ID**: 2A202600347
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

_Trách nhiệm chính của tôi trong Nhóm là xây dựng vòng lặp tư duy ReAct lõi (Core Engine), cơ chế phân phối công cụ thông minh (Dispatcher) và tích hợp API Internet giao dịch thực tế._

- **Modules Implemented**:
  - `src/agent/agent.py` (Quy hoạch và logic hóa hàm `run` và `_execute_tool`)
  - `src/tools/ecommerce_tools.py` (Lập trình hàm tĩnh `convert_currency` call network request)
  - `main_agent.py` (Xây dựng sơ bộ kiến trúc và Menu giao diện Terminal cho các Test Case)
- **Code Highlights**:
  - Xây dựng thành công vòng lặp ReAct trong hàm `run()` kết hợp RegEx Parser để bóc tách chính xác khối `Action` và `Thought`.
  - Đặc biệt, đã hiện thực hóa kỹ năng **Auto-Retry (Fail-Safe)**: Tại hàm `run()`, nếu Tool quăng lỗi param, không đánh sập hệ thống ngay mà đẩy `SYSTEM WARNING` vào Prompt bắt LLM tự nhận lỗi và sửa nhờ cờ `consecutive_errors`.
  - Tích hợp Tool `convert_currency()`: Bắn request qua `urllib.request` lên `api.exchangerate-api.com` parse JSON tỷ giá ngoại tệ theo Real-time để nâng độ khó cho các Test-cases phân tích kinh doanh.

- **Documentation**: Mối tương quan của luồng code là: Hàm `run()` đóng vai trò "Nhạc trưởng", điều phối LLM sinh text, cắt gọt lấy chuỗi `Action` và truyền đầu vào cho hàm `_execute_tool` map với danh mục hàm Python độc lập. Cuối cùng biến kết quả thành chuỗi `Observation` chèn ngược lại vào Cửa sổ Ngữ cảnh (Prompt) để LLM "giác ngộ" và suy diễn bước quyết định.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Trong lúc test tính năng nâng cao bằng API Tỷ Giá, Agent liên tục kẹt vào ngõ cụt khi LLM xảo quyệt đưa ra lệnh `Action: convert_currency(35000000, "VND")`. Nó bỏ quên tham số thứ 3, khiến khối Python bắn ra Exception.
- **Log Source**: Trích xuất log ghi nhận: `{"timestamp": "...", "event": "AGENT_ERROR_RETRY", "data": {"error": "ERROR: convert_currency cần đúng 3 tham số...", "retry": 1}}`.
- **Diagnosis**:
  - Nguyên nhân nằm ở chính User Prompt mồi ("Đổi 35 triệu VNĐ ra đô la"). Mô hình ngôn ngữ ngầm hiểu là ra USD nhưng chủ quan và lười biếng, quên mất định dạng Tool Spec ngặt nghèo đòi tận 3 biến. Nó mớm sai số lượng arguments vào Regex bắt chuỗi.
  - Vòng lặp `max_steps` ban đầu bị hao mòn vô ích mỗi lần lỗi, và nhanh chóng chạm trần 7 lần dẫn đến hệ thống bị sập (crash) mà không chốt được đơn bảo vệ cho khách.
- **Solution**:
  - Tôi tái cấu trúc luồng Catching của hàm `_execute_tool` và vòng lặp `run()`. Thay vì đẩy `max_steps += 1`, tôi lập trình cụm rẽ nhánh: phát hiện chuỗi bắt đầu bằng "ERROR:" sẽ gắn thẻ `consecutive_errors += 1` và đẩy chèn ngữ cảnh `SYSTEM WARNING: Lỗi gọi hàm! Yêu cầu tuân thủ đúng số lượng...` sau đó dùng lệnh `continue`.
  - Nhờ cơ chế này, ở vòng kế tiếp, LLM đã thức tỉnh và điền đầy đủ `convert_currency(35000000, "VND", "USD")` thành công.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: Việc hệ thống ép Model LLM phải in ra chữ `Thought:` trước khi hành động khiến mô hình sở hữu luồng rành mạch "Chain-of-Thought". Nhờ đó, tính logic toán học được phơi bày rõ, khắc phục triệt để điểm yếu mù quáng lao vào chém gió con số "tổng tiền hư ảo" của bản Chatbot Baseline.
2. **Reliability**: Điểm trừ chí mạng duy nhất của hệ thống Agent nằm ở khâu giao tiếp "Small Talk". Vì bộ lọc hệ thống ReAct Agent luôn đóng đinh ám ảnh LLM phải nhả định dạng chứa `Action:` ở mỗi Turn, nên khi khách hàng chỉ chào buổi sáng hay trêu đùa vài câu, LLM có xu hướng bối rối và làm ô nhiễm log (nhả error format lãng phí token). Trong khi bản thân Chatbot có thể uyển chuyển đối đáp ở phần này ngay tắp lự.
3. **Observation**: Khối `Observation` là giác quan mang lại "sự tiệm cận thực tế" cho Agent. Nhờ các quan sát số liệu sống từ DB nhả về (Ví dụ: `0.1` chiết khấu từ get_discount, hay `25500` tỷ giá USD), LLM có nền Grounding kiên cố để tổng hợp `Final Answer` - tiêu diệt tính nhảm nhí ảo giác tự suy diễn của mô hình GenAI.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Nâng cấp module quản lý công cụ (Tool Registry). Nếu kho Tools mở rộng lên hàng nghìn Tools phức tạp, hệ thống không thể nhét mù quáng toàn file JSON vào đầu Model gây tràn Context Window. Cần dùng hệ CSDL Vector (FAISS/Chroma) làm Retriever - chỉ moi top 3 Tools khớp Semantic Similarity nhất đưa cho LLM tại tời điểm real-time.
- **Safety**: Xây dựng cơ chế thanh tra kép (Supervisor Agent Evaluator). Audit - rà soát chéo lại biến `Final Answer` với các `Observation` đã nhận xem LLM Worker kia có lén lút tính láo phí Ship hay cố tình lách mã giảm giá trước khi Output gửi ra luồng Checkout thanh toán hay không.
- **Performance**: Phân rã luồng I/O độc lập thành Asynchronous Runtime (như `asyncio.gather`). Giúp Agent có thể gọi song song nhiều Tool cồng kềnh (Call mạng ngoại tệ tỷ giá và Call Query DB Check Inventory cùng một chu kỳ Tick) giúp giảm mạnh Latency - nâng cấp trải nghiệm tốc độ cho người dùng.
