import os
import sys
from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider
# from src.core.gemini_provider import GeminiProvider
# from src.core.local_provider import LocalProvider
from src.telemetry.logger import logger

def get_provider():
    load_dotenv()
    
    provider_name = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    
    if provider_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ Lỗi: OPENAI_API_KEY chưa được thiết lập trong file .env")
            sys.exit(1)
        return OpenAIProvider(model_name="gpt-4o", api_key=api_key)
        
    elif provider_name == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ Lỗi: GEMINI_API_KEY chưa được thiết lập trong file .env")
            sys.exit(1)
        return GeminiProvider(model_name="gemini-1.5-flash", api_key=api_key)
        
    elif provider_name == "local":
        model_path = os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
        if not os.path.exists(model_path):
            print(f"❌ Lỗi: Không tìm thấy model cục bộ tại {model_path}")
            sys.exit(1)
        return LocalProvider(model_path=model_path)
    
    else:
        print(f"❌ Lỗi: Provider '{provider_name}' không được hỗ trợ.")
        sys.exit(1)

def run_chatbot_baseline():
    print("🤖 Đang khởi tạo Chatbot Baseline...")
    provider = get_provider()
    
    print(f"✅ Đã kết nối thành công với Provider: {provider.__class__.__name__}")
    print("💡 Nhập 'quit' hoặc 'exit' để thoát.\n" + "-"*50)
    
    system_prompt = "You are a helpful assistant. You do NOT have access to any external tools. Answer the questions to the best of your ability."
    
    while True:
        try:
            user_input = input("\n🧑 User: ")
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Tạm biệt!")
                break
            if not user_input.strip():
                continue
            
            # Ghi log bắt đầu
            logger.log_event("CHATBOT_START", {"input": user_input, "model": provider.model_name})
            
            print("🤖 Chatbot: ", end="", flush=True)
            
            # In ra màn hình dạng stream
            full_response = ""
            for chunk in provider.stream(user_input, system_prompt=system_prompt):
                print(chunk, end="", flush=True)
                full_response += chunk
            print()
            
            # Để lấy metrics (Token usage, latency), ta gọi fake một lần generate không stream (nếu hệ thống strict),
            # hoặc vì provider.stream không trả metrics, ta có thể log đơn giản cho bản baseline
            logger.log_event("CHATBOT_END", {
                "output_length": len(full_response),
                "status": "success"
            })
            
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Đã xảy ra lỗi: {e}")
            logger.error(f"Chatbot run error: {e}")

if __name__ == "__main__":
    run_chatbot_baseline()
