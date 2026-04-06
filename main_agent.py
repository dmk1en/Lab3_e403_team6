import os
import time
from dotenv import load_dotenv
from chatbot import get_provider
from src.agent.agent import ReActAgent
from src.tools.ecommerce_tools import ECOMMERCE_TOOLS_SPEC

def run_tests():
    print("🚀 Đang khởi tạo ReAct Agent v1...")
    provider = get_provider()
    agent = ReActAgent(llm=provider, tools=ECOMMERCE_TOOLS_SPEC, max_steps=7)
    
    # 5 Kịch bản (Test Cases) phủ đủ độ khó từ Dễ đến Ảo Giác
    test_cases = [
        {
            "id": 1,
            "level": "Dễ",
            "desc": "Truy vấn 1 công cụ (Single Tool)",
            "query": "Kiểm tra giúp tôi xem kho còn điện thoại iPhone không?"
        },
        {
            "id": 2,
            "level": "Trung bình",
            "desc": "Kết hợp 2 công cụ rời rạc",
            "query": "Tôi có mã giảm giá TET. Nếu kiện hàng của tôi nặng 2kg và muốn ship về HCM, thì mã giảm giá là mấy phần trăm và phí giao hàng là bao nhiêu tiền?"
        },
        {
            "id": 3,
            "level": "Khó",
            "desc": "Luồng mua hàng hoàn chỉnh (Full Flow)",
            "query": "Hàng Macbook còn không? Nếu còn thì tính tổng tiền hóa đơn cho tôi biết: Mua 2 cái Macbook, tổng nặng 4kg, chuyển về Hà Nội. Gắn thêm mã giảm WINNER. (Lưu ý giá 1 chiếc là 30 triệu VND)."
        },
        {
            "id": 4,
            "level": "Bẫy Ảo Giác",
            "desc": "Sản phẩm không có trong quy định",
            "query": "Tôi muốn mua đôi giày Sneaker Nike nặng 1kg ship về Hà Nội. Check kho cho tôi."
        },
        {
            "id": 5,
            "level": "Ngoại lệ",
            "desc": "Hội thoại thông thường không cần Tool",
            "query": "Chào em, dạo này em bán hàng có tốt không? Có hay bị kẹt đơn không?"
        }
    ]

    while True:
        print("\n" + "="*60)
        print("📋 MENU CHỌN TEST CASE ".center(60, "="))
        for tc in test_cases:
            print(f"[{tc['id']}] Khúc {tc['level']} - {tc['desc']}")
        print("[0] Chạy TẤT CẢ 5 Test Cases lần lượt")
        print("[q] Thoát chương trình")
        print("="*60)
        
        choice = input("👉 Mời nhập ID (0-5, hoặc 'q'): ").strip().lower()
        
        if choice == 'q' or choice == 'quit':
            print("👋 Đã thoát test.")
            break
            
        try:
            choice_int = int(choice)
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ.")
            continue
            
        if choice_int == 0:
            target_cases = test_cases
        elif 1 <= choice_int <= 5:
            target_cases = [test_cases[choice_int - 1]]
        else:
            print("❌ Không có test case này. Vui lòng nhập từ 0-5.")
            continue

        for tc in target_cases:
            print("\n" + "="*80)
            print(f"🔥 ĐANG CHẠY TEST CASE {tc['id']} | Độ khó: [{tc['level']}] - {tc['desc']}")
            print(f"👤 USER: {tc['query']}")
            print("="*80)
            
            # Khởi chạy Agent thay vì phải reset history (vì logic lab 3 mỗi run là 1 query mới)
            final_response = agent.run(tc['query'])
            
            print("\n" + "*"*80)
            print(f"🏆 FINAL ANSWER {tc['id']}:\n {final_response}")
            print("*"*80 + "\n")
            
            if choice_int == 0:  # Pause một chút nếu chạy toàn bộ 5 case để API đỡ nóng
                import time
                time.sleep(1.5)

if __name__ == "__main__":
    run_tests()
