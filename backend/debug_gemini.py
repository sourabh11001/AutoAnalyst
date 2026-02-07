import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERROR: No API Key found in .env")
    exit()

print(f"🔑 Key found: {api_key[:5]}... (checking access)")
genai.configure(api_key=api_key)

print("\n📡 Connecting to Google servers to list models...")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   ✅ Found: {m.name}")
            available_models.append(m.name)
            
    if not available_models:
        print("\n❌ CRITICAL: No text generation models found for this key!")
        print("   Solution: Your API key might be restricted or invalid.")
    else:
        print(f"\n🎉 SUCCESS: You have access to {len(available_models)} models.")
        print(f"   Recommended Model String: '{available_models[0]}'")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")
