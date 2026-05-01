"""
LLM CORE - Word Level Model with Context & Quality
Bas itna - kuch extra nahi
"""

import os
import json
import random
import re
from collections import defaultdict, Counter

class LLMModel:
    def __init__(self, name, n_gram=2):
        self.name = name
        self.n = n_gram
        self.weights = {}
        self.vocab = set()
        self.start_words = []
        self.temperature = 0.7
        self.context_history = []  # last 3 exchanges yaad rakhega
        
    def tokenize(self, text):
        """Text ko words mein tod"""
        text = text.lower()
        text = re.sub(r'[^\w\s\.\?\!]', '', text)
        words = text.split()
        return words
    
    def train_from_folder(self, folder_path, progress_callback=None):
        """Folder se train - word level"""
        all_words = []
        files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        total_files = len(files)
        
        for idx, filename in enumerate(files):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                words = self.tokenize(text)
                all_words.extend(words)
            
            if progress_callback:
                progress_callback(idx+1, total_files, filename, len(words))
        
        # Word n-grams
        ngram_counts = defaultdict(Counter)
        for i in range(len(all_words) - self.n):
            prefix = ' '.join(all_words[i:i+self.n])
            next_word = all_words[i+self.n]
            ngram_counts[prefix][next_word] += 1
        
        # Sentence starters
        for i, word in enumerate(all_words):
            if i == 0 or all_words[i-1] in ['.', '!', '?']:
                self.start_words.append(word)
        
        # Convert to probabilities
        for prefix, counter in ngram_counts.items():
            total = sum(counter.values())
            self.weights[prefix] = {w: c/total for w, c in counter.items()}
        
        self.vocab = set(all_words)
        return total_files, len(all_words), len(self.weights)
    
    def add_to_context(self, user_msg, bot_response):
        """Context mein add karo (last 3 exchanges)"""
        self.context_history.append({
            'user': user_msg,
            'bot': bot_response
        })
        # Sirf last 3 rakho
        if len(self.context_history) > 3:
            self.context_history.pop(0)
    
    def get_context_string(self):
        """Context ko string mein convert for generation"""
        if not self.context_history:
            return ""
        context = []
        for exchange in self.context_history[-3:]:
            context.append(exchange['user'])
            context.append(exchange['bot'])
        return ' '.join(context)
    
    def is_quality_response(self, response, min_words=3):
        """Check if response is good quality"""
        words = response.split()
        # Check if too short
        if len(words) < min_words:
            return False
        # Check if repeating same word
        if len(set(words)) < 2:
            return False
        # Check if has meaningful words
        if len(response) < 10:
            return False
        return True
    
    def generate(self, seed="", max_words=50, max_retries=3):
        """Generate response with quality check"""
        if not seed:
            seed = random.choice(self.start_words) if self.start_words else "the"
        
        # Add context to seed
        context = self.get_context_string()
        if context:
            seed = context + " " + seed
        
        for attempt in range(max_retries):
            words = seed.lower().split()
            
            for _ in range(max_words - len(words)):
                if len(words) >= self.n:
                    context = ' '.join(words[-self.n:])
                else:
                    context = ' '.join(words)
                
                if context in self.weights:
                    candidates = list(self.weights[context].keys())
                    probs = list(self.weights[context].values())
                    
                    if self.temperature != 1.0:
                        probs = [p ** (1/self.temperature) for p in probs]
                        s = sum(probs)
                        probs = [p/s for p in probs]
                    
                    next_word = random.choices(candidates, weights=probs)[0]
                    words.append(next_word)
                else:
                    break
            
            result = ' '.join(words)
            # Capitalize first letter
            if result:
                result = result[0].upper() + result[1:]
            
            # Quality check
            if self.is_quality_response(result):
                return result
        
        # If all retries failed, return last attempt
        return result
    
    def save(self, models_dir="saved_models"):
        os.makedirs(models_dir, exist_ok=True)
        path = os.path.join(models_dir, f"{self.name}.json")
        data = {
            'name': self.name,
            'n': self.n,
            'weights': {k: dict(v) for k, v in self.weights.items()},
            'vocab': list(self.vocab),
            'start_words': self.start_words
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    
    @classmethod
    def load(cls, name, models_dir="saved_models"):
        path = os.path.join(models_dir, f"{name}.json")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model = cls(data['name'], data['n'])
        model.weights = data['weights']
        model.vocab = set(data['vocab'])
        model.start_words = data['start_words']
        return model

def list_models(models_dir="saved_models"):
    if not os.path.exists(models_dir):
        return []
    return [f.replace('.json', '') for f in os.listdir(models_dir) if f.endswith('.json')]