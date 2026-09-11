from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import HttpUrl
from bs4 import BeautifulSoup
import requests
import pydantic

app = FastAPI(
    title="BlogToReel.ai API",
    description="Backend service for converting blog posts into viral short video scripts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(pydantic.BaseModel):
    url: HttpUrl

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlogToReel - تحويل المقالات إلى فيديوهات</title>
    <style>
        body {
            font-family: Tahoma, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 20px;
            direction: rtl;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        input[type="url"] {
            width: 100%;
            padding: 12px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 25px;
            padding: 15px;
            background: #e9ecef;
            border-radius: 5px;
            display: none;
            word-break: break-word;
        }
        .loading {
            text-align: center;
            color: #007bff;
            display: none;
            margin-top: 15px;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>تحويل المقال إلى ريلز (BlogToReel)</h2>
    <div class="form-group">
        <label for="blogUrl">أدخل رابط المقال:</label>
        <input type="url" id="blogUrl" placeholder="https://example.com/article" required>
    </div>
    <button onclick="convertBlog()">تحويل المقال الآن</button>
    
    <div id="loading" class="loading">جاري معالجة المقال وصياغة السكربت... يرجى الانتظار</div>
    
    <div id="result">
        <h3>النتيجة:</h3>
        <p><strong>عنوان المقال:</strong> <span id="resTitle"></span></p>
        <p><strong>السكربت المقترح للفيديو:</strong> <span id="resScript" style="color: #d9534f; font-weight: bold;"></span></p>
    </div>
</div>

<script>
    async function convertBlog() {
        const urlInput = document.getElementById('blogUrl').value.trim();
        const resultDiv = document.getElementById('result');
        const loadingDiv = document.getElementById('loading');
        
        if (!urlInput) {
            alert('الرجاء إدخال رابط صحيح!');
            return;
        }

        resultDiv.style.display = 'none';
        loadingDiv.style.display = 'block';

        try {
            const response = await fetch('/api/convert-blog', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: urlInput })
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('resTitle').innerText = data.article_title;
                document.getElementById('resScript').innerText = data.generated_video_script;
                resultDiv.style.display = 'block';
            } else {
                alert('خطأ: ' + (data.detail || 'حدث مشكلة أثناء جلب المقال'));
            }
        } catch (error) {
            alert('تعذر الاتصال بالخادم السحابي. تأكد من صحة الرابط أو المحاولة لاحقاً.');
            console.error(error);
        } finally {
            loadingDiv.style.display = 'none';
        }
    }
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTML_CONTENT

@app.post("/api/convert-blog")
def convert_blog_to_script(payload: ArticleRequest):
    target_url = str(payload.url)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not fetch the article from the provided URL.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1')
        article_title = title.get_text().strip() if title else "Untitled Article"
        
        paragraphs = soup.find_all('p')
        content_text = " ".join([p.get_text() for p in paragraphs[:5]])
        
        if not content_text:
            content_text = "No readable content found on this page."

        video_script = f"Hook: Did you know this? -> {article_title[:60]}... Summary: {content_text[:150]}... Call to Action: Read the full article link in bio!"

        return {
            "status": "success",
            "article_title": article_title,
            "extracted_text_preview": content_text[:300] + "...",
            "generated_video_script": video_script,
            "message": "Blog processed successfully!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
