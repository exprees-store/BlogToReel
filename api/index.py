from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

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
            margin-top: 60px;
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
            font-size: 48px;
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
            font-size: 17px;
            margin-bottom: 30px;
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
        .result-box {
            margin-top: 25px;
            text-align: left;
            background: #111827;
            border: 1px solid #374151;
            padding: 20px;
            border-radius: 12px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            display: none;
        }
        .result-box h3 {
            color: #c084fc;
            margin-bottom: 10px;
        }
        .result-box p {
            color: #d1d5db;
            font-size: 14px;
            line-height: 1.6;
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
        
        <div id="resultBox" class="result-box">
            <h3 id="resTitle"></h3>
            <p id="resDesc"></p>
        </div>
    </div>

    <script>
        async function processArticle() {
            const url = document.getElementById('articleUrl').value;
            const resultBox = document.getElementById('resultBox');
            const resTitle = document.getElementById('resTitle');
            const resDesc = document.getElementById('resDesc');
            
            if(!url) {
                alert("Please enter a valid article URL.");
                return;
            }

            resTitle.innerText = "⏳ Extracting article content...";
            resDesc.innerText = "Connecting to Python backend to scrape and analyze the blog post...";
            resultBox.style.display = "block";

            try {
                // استخدام طريقة GET الآمنة عبر تمرير الرابط في الـ URL لتفادي قيود Vercel للـ POST
                const res = await fetch(`/api/scrape?url=${encodeURIComponent(url)}`);
                const data = await res.json();
                
                if(res.ok) {
                    resTitle.innerText = "✅ Successfully Extracted: " + data.title;
                    resDesc.innerText = data.summary;
                } else {
                    resTitle.innerText = "❌ Error";
                    resDesc.innerText = data.detail || "Failed to process the article.";
                }
            } catch (error) {
                resTitle.innerText = "❌ Connection Error";
                resDesc.innerText = "Could not reach the Python backend server. Details: " + error.message;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

@app.get("/api/scrape")
async def scrape_article(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Could not fetch URL (Status code: {resp.status_code})")
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title Found"
        paragraphs = soup.find_all('p')
        text_snippet = " ".join([p.get_text() for p in paragraphs[:4]]) if paragraphs else "No content paragraphs found."
        
        if len(text_snippet) > 300:
            text_snippet = text_snippet[:300] + "..."

        return {
            "status": "success",
            "title": title.strip(),
            "summary": f"Extracted text preview: {text_snippet}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
