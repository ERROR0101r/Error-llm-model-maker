# clean_data.py - Remove garbage from text files
import os
import re

folder = "data"

print("\n🧹 Cleaning text files...\n")

for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        path = os.path.join(folder, filename)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Remove garbage patterns
        text = re.sub(r'\b\w+:', ' ', text)
        text = re.sub(r':\w+', ' ', text)
        text = re.sub(r'[{}[\]()<>]', ' ', text)
        text = re.sub(r'[_\-=|\\/*+]', ' ', text)
        text = re.sub(r'retrieval[_a-z]*', ' ', text, flags=re.I)
        text = re.sub(r'labels[_a-z]*', ' ', text, flags=re.I)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Cleaned: {filename}")

print("\n🎉 Done! Run trainer.py now.")