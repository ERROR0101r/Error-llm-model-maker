#!/usr/bin/env python3
"""
TRAINER - Same as before
"""

import os
import time
from llm_core import LLMModel, list_models

def show_progress(current, total, filename, words):
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current // total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r📄 [{bar}] {percent:.1f}%  File {current}/{total}: {filename} ({words} words)", end='', flush=True)

def main():
    print("\n" + "="*50)
    print("    🤖 DESI LLM - TRAINER")
    print("="*50)
    
    models_dir = "saved_models"
    os.makedirs(models_dir, exist_ok=True)
    
    existing = list_models(models_dir)
    if existing:
        print("\n📦 Existing models:")
        for i, m in enumerate(existing, 1):
            print(f"   {i}. {m}")
        print(f"   {len(existing)+1}. Create new model")
        choice = input(f"\nSelect (1-{len(existing)+1}): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(existing):
                model_name = existing[idx-1]
                print(f"✅ Loading '{model_name}'...")
                model = LLMModel.load(model_name, models_dir)
            elif idx == len(existing)+1:
                model_name = input("Enter new model name: ").strip()
                if not model_name:
                    print("❌ Name required!")
                    return
                model = LLMModel(model_name)
            else:
                print("❌ Invalid")
                return
        else:
            print("❌ Invalid")
            return
    else:
        print("\n🆕 No models found. Create new one.")
        model_name = input("Enter model name: ").strip()
        if not model_name:
            print("❌ Name required!")
            return
        model = LLMModel(model_name)
    
    folder = input("\n📁 Enter folder path with .txt files: ").strip()
    if not os.path.exists(folder):
        print(f"❌ Folder '{folder}' not found!")
        return
    
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not txt_files:
        print("❌ No .txt files found!")
        return
    
    print(f"\n📚 Found {len(txt_files)} text files. Train? (y/n): ", end='')
    if input().strip().lower() != 'y':
        print("Aborted.")
        return
    
    print("\n🚀 Training started...\n")
    start_time = time.time()
    
    try:
        total_files, total_words, patterns = model.train_from_folder(folder, show_progress)
        elapsed = time.time() - start_time
        
        print(f"\n\n✅ Training complete in {elapsed:.2f} seconds!")
        print(f"   - Files: {total_files}")
        print(f"   - Total words: {total_words}")
        print(f"   - Patterns: {patterns}")
        print(f"   - Vocabulary: {len(model.vocab)} words")
        
        path = model.save(models_dir)
        print(f"\n💾 Model saved: {path}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()