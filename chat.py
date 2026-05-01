#!/usr/bin/env python3
"""
CHAT - With context memory & quality responses
"""

import os
from llm_core import LLMModel, list_models

def main():
    print("\n" + "="*50)
    print("    💬 DESI LLM - CHAT")
    print("="*50)
    
    existing = list_models()
    if not existing:
        print("❌ No models found! Run trainer.py first.")
        return
    
    print("\n📦 Available models:")
    for i, m in enumerate(existing, 1):
        print(f"   {i}. {m}")
    
    choice = input(f"\nSelect (1-{len(existing)}): ").strip()
    if not choice.isdigit():
        print("Invalid")
        return
    idx = int(choice)
    if idx < 1 or idx > len(existing):
        print("Invalid")
        return
    
    model_name = existing[idx-1]
    print(f"📀 Loading {model_name}...")
    model = LLMModel.load(model_name)
    print(f"✅ Ready! Vocabulary: {len(model.vocab)} words, Patterns: {len(model.weights)}")
    
    print("\n🎚️ Temperature (0.3=focused, 1.0=creative):")
    temp = input(f"Current {model.temperature}, Enter to keep or new: ").strip()
    if temp:
        try:
            model.temperature = float(temp)
        except:
            pass
    
    print("\n" + "="*50)
    print("💡 Commands:")
    print("   Type your message and press Enter")
    print("   Type 'temp X' to change temperature")
    print("   Type 'clear' to clear conversation memory")
    print("   Type 'quit' to exit")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ('quit', 'exit', 'q'):
            print("Goodbye! 👋")
            break
        
        if user_input.lower() == 'clear':
            model.context_history = []
            print("🧹 Conversation memory cleared!\n")
            continue
        
        if user_input.lower().startswith('temp '):
            try:
                new_temp = float(user_input.split()[1])
                model.temperature = new_temp
                print(f"🎚️ Temperature = {new_temp}")
            except:
                print("❌ Usage: temp 0.7")
            continue
        
        if not user_input:
            continue
        
        response = model.generate(seed=user_input, max_words=60)
        print(f"🤖: {response}\n")
        
        # Save to context
        model.add_to_context(user_input, response)

if __name__ == "__main__":
    main()