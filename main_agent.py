import os
from dotenv import load_dotenv
from chatbot import get_provider
from src.agent.agent import ReActAgent
from src.tools.ecommerce_tools import ECOMMERCE_TOOLS_SPEC

def main():
    print("🚀 Đang khởi tạo ReAct Agent v1...")
    
    provider = get_provider()
    
    agent = ReActAgent(
        llm=provider,
        tools=ECOMMERCE_TOOLS_SPEC,
        max_steps=7 
    )
    
    # Kịch bản E-commerce khó
    test_case = "I want to buy 2 iPhones using code 'WINNER' and ship to Hanoi. I assume 1 iphone weights 0.3 kg. What is the total price? Note: 1 iphone cost 10000000 VNĐ. Check stock first."
    
    print("="*60)
    print(f"👤 USER: {test_case}")
    print("="*60)
    
    final_response = agent.run(test_case)
    
    print("="*60)
    print(f"🏆 FINAL ANSWER: {final_response}")
    print("="*60)
    print("✅ Hoàn tất bài Test! Vui lòng vào thư mục logs/ để kiểm tra Trace.")

if __name__ == "__main__":
    main()
