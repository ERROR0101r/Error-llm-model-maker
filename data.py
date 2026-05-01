"""
SIMPLE WEB SCRAPER - Sirf visible text nikaalega
Same folder mein save karega
"""

import urllib.request
import urllib.parse
import re
import os
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    """HTML tags hataane wala parser"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    
    def handle_data(self, d):
        self.text.append(d)
    
    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    """HTML se tags hatao"""
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_text(text):
    """Text ko clean karo (extra spaces, lines, etc.)"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove common non-text garbage
    text = re.sub(r'\{[^}]*\}', '', text)  # JSON objects
    text = re.sub(r'\[[^\]]*\]', '', text)  # Arrays
    text = re.sub(r'javascript:[^;]*;', '', text)  # JS code
    return text.strip()

def download_and_extract(url):
    """URL se sirf visible text nikaalo"""
    try:
        # Browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Remove script aur style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<[^>]+>', ' ', html)  # Remove all tags
        
        # Clean up
        text = strip_tags(html)
        text = clean_text(text)
        
        if len(text) < 100:
            return False, "Text bahut chhota hai (100 chars se kam)"
        
        return True, text
        
    except Exception as e:
        return False, str(e)

def save_text(text, filename):
    """Text ko file mein save karo"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✅ Saved: {filename} ({len(text):,} characters)")

def get_next_filename():
    """Next number wala filename do"""
    num = 1
    while True:
        filename = f"dataset_{num}.txt"
        if not os.path.exists(filename):
            return filename
        num += 1

def main():
    print("\n" + "="*60)
    print("   📥 SIMPLE WEB SCRAPER - Sirf Text Nikaalega")
    print("="*60)
    print("\nBas URL daal, visible text save hoga same folder mein!")
    print("Type 'list' to see saved files")
    print("Type 'quit' to exit")
    print("="*60)
    
    saved_files = []
    
    while True:
        print(f"\n📁 Files saved: {len(saved_files)}")
        url = input("\n🌐 Enter URL: ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            print("\n" + "="*60)
            print(f"✅ Total {len(saved_files)} files saved in current folder:")
            for f in saved_files:
                print(f"   📄 {f}")
            print("="*60)
            break
        
        if url.lower() == 'list':
            if saved_files:
                print("\n📚 Your files:")
                for f in saved_files:
                    size = os.path.getsize(f)
                    print(f"   - {f} ({size:,} bytes)")
            else:
                print("   No files yet. Download something first!")
            continue
        
        if not url.startswith(('http://', 'https://')):
            print("❌ Invalid! URL must start with http:// or https://")
            continue
        
        print("⏳ Scraping and extracting text...")
        success, result = download_and_extract(url)
        
        if success:
            filename = get_next_filename()
            save_text(result, filename)
            saved_files.append(filename)
            
            # Preview dikhao
            preview = result[:200] + "..." if len(result) > 200 else result
            print(f"\n📖 Preview:\n{preview}\n")
        else:
            print(f"❌ Failed: {result}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user. Goodbye!")