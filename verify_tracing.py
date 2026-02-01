import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tracers.context import tracing_v2_enabled

# 1. Load your credentials
load_dotenv()

def test_trace():
    print(f"Checking project: {os.getenv('LANGCHAIN_PROJECT')}")
    
    # 2. Use the model we know works for your account
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 3. Run a simple call inside the tracing context
    # This 'with' block is the modern way to ensure the trace is captured
    try:
        with tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT")):
            print("Sending test message to Gemini...")
            response = llm.invoke("Confirming LangSmith telemetry for Sassafras.")
            print(f"Gemini Response: {response.content}")
            
        print("## Success! Waiting 5 seconds for telemetry upload...")
        time.sleep(5)
    except Exception as e:
        print(f"## Error during tracing test: {e}")

if __name__ == "__main__":
    test_trace()