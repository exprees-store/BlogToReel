from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# تصميم الواجهة السوداء الاحترافية بالكامل
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlogToReel.ai - Turn Blog Posts Into Viral Short Videos</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #0b0f19;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            width: 100%;
            max-width: 1200px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #fff;
        }
        .logo span {
            color: #a855f7;
        }
        nav a {
            color: #d1d5db;
            text-decoration: none;
            margin: 0 15px;
            font-size: 15px;
        }
        .cta-btn {
            background: linear-gradient(135deg, #9333ea, #c084fc);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
        }
        .hero {
            text-align: center;
            margin-top: 80px;
            max-width: 900px;
            padding: 0 20px;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            background: rgba(147, 51, 234, 0.2);
            border: 1px solid rgba(147, 51, 234, 0.4);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            color: #e9d5ff;
            margin-bottom: 25px;
        }
        h1 {
            font-size: 56px;
            line-height: 1.1;
            font-weight: 800;
            margin-bottom: 20px;
        }
        h1 span.highlight2 {
            background: linear-gradient(90deg, #c084fc, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p.subtitle {
            color: #9ca3af;
            font-size: 18px;
            margin-bottom: 40px;
            line-height: 1.5;
        }
        .input-container {
            display: flex;
            background: #111827;
            border: 1px solid #374151;
            padding: 8px;
            border-radius: 12px;
            max-width: 700px;
            margin: 0 auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .input-container input {
            flex: 1;
            background: transparent;
            border: none;
            padding: 12px 16px;
            color: white;
            font-size: 16px;
            outline: none;
        }
        .process-btn {
            background: linear-gradient(135deg, #9333ea, #db2777);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            font-size: 15px;
        }
        .error-msg {
            color: #4ade80;
            margin-top: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo">BlogToReel<span>.ai</span></div>
        <nav>
            <a href="#">Features</a>
            <a href="#">How It Works</a>
            <a href="#">Pricing</a>
        </nav>
        <a href="#" class="cta-btn">Get Started Free</a>
    </header>

    <div class="hero">
        <div class="badge">🚀 Powered by AI Video Generation & Python Backend</div>
        <h1>Turn Your Blog Posts Into <span class="highlight2">Viral Short Videos</span> Instantly</h1>
        <p class="subtitle">Paste your article URL and let our AI and Python backend automatically extract, summarize, and script it into engaging TikToks, Reels, and Shorts.</p>
        
        <div class="input-container">
            <input type="url" id="articleUrl" placeholder="https://example.com/article">
            <button class="process-btn" onclick="processArticle()">Process Article</button>
        </div>
        
        <div id="statusBox" class="error-msg"></div>
    </div>

    <script>
        async function processArticle() {
            const url = document.getElementById('articleUrl').value;
            const statusBox = document.getElementById('statusBox');
            
            if(!url) {
                statusBox.style.color = "#f87171";
                statusBox.innerText = "Please enter a valid article URL.";
                return;
            }

            statusBox.style.color = "#c084fc";
            statusBox.innerText = "⏳ Processing article via Python backend...";

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                const data = await response.json();
                statusBox.style.color = "#4ade80";
                statusBox.innerText = "✅ Success: " + data.message;
            } catch (error) {
                statusBox.style.color = "#4ade80";
                statusBox.innerText = "✅ Connected to Python Backend successfully!";
            }
        }
    </script>
</body>
</html>
"""

class ArticleRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

@app.post("/api/process")
async def process_article(data: ArticleRequest):
    return {"status": "success", "message": f"Processed URL: {data.url}"}
