#!/usr/bin/env python3
"""
API - Simple HTTP server (no extra features)
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from llm_core import LLMModel, list_models

current_model = None
models_dir = "saved_models"

class LLMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        
        elif path == '/api/models':
            models = list_models(models_dir)
            self.send_json({'models': models})
        
        elif path == '/api/load':
            params = parse_qs(parsed.query)
            name = params.get('name', [None])[0]
            if name and name in list_models(models_dir):
                global current_model
                current_model = LLMModel.load(name, models_dir)
                self.send_json({'status': 'ok', 'model': name, 'patterns': len(current_model.weights)})
            else:
                self.send_json({'status': 'error', 'message': 'Model not found'}, 404)
        
        elif path == '/api/generate':
            if current_model is None:
                self.send_json({'error': 'No model loaded'}, 400)
                return
            params = parse_qs(parsed.query)
            seed = params.get('seed', [''])[0]
            words = int(params.get('words', ['50'])[0])
            temp = float(params.get('temp', ['0.7'])[0])
            current_model.temperature = temp
            text = current_model.generate(seed, words)
            self.send_json({'seed': seed, 'generated': text, 'temperature': temp})
        
        else:
            self.send_error(404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # Silent mode

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Desi LLM</title>
<style>
body{font-family:monospace;max-width:800px;margin:auto;padding:20px;background:#f0f0f0}
.card{background:white;padding:20px;border-radius:10px;margin-bottom:20px}
textarea{width:100%;height:200px;padding:10px}
button{padding:10px 20px;margin:5px;cursor:pointer}
input{width:100%;padding:10px;margin:10px 0}
</style>
</head>
<body>
<h1>🤖 Desi LLM</h1>
<div class="card">
<h2>📦 Load Model</h2>
<select id="modelSelect"></select>
<button onclick="loadModel()">Load</button>
<p id="modelStatus">No model loaded</p>
</div>
<div class="card">
<h2>✍️ Generate</h2>
<input type="text" id="seed" placeholder="Seed text">
<button onclick="generate()">Generate</button>
<textarea id="output" readonly placeholder="Output..."></textarea>
</div>
<script>
fetch('/api/models').then(r=>r.json()).then(data=>{
    let sel=document.getElementById('modelSelect');
    data.models.forEach(m=>{let opt=document.createElement('option');opt.value=m;opt.text=m;sel.appendChild(opt)});
});
function loadModel(){
    let name=document.getElementById('modelSelect').value;
    fetch(`/api/load?name=${name}`).then(r=>r.json()).then(data=>{
        document.getElementById('modelStatus').innerText=`✅ Loaded ${name} (${data.patterns} patterns)`;
    });
}
function generate(){
    let seed=document.getElementById('seed').value;
    fetch(`/api/generate?seed=${encodeURIComponent(seed)}&words=60`).then(r=>r.json()).then(data=>{
        document.getElementById('output').value=data.generated;
    });
}
</script>
</body>
</html>
"""

def main():
    global models_dir
    os.makedirs(models_dir, exist_ok=True)
    
    port = 8000
    server = HTTPServer(('0.0.0.0', port), LLMHandler)
    print(f"🚀 API Server on http://localhost:{port}")
    print("   GET /api/models - List models")
    print("   GET /api/load?name=X - Load model")
    print("   GET /api/generate?seed=hello&words=50 - Generate")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main()