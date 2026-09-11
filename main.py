from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import HttpUrl
from bs4 import BeautifulSoup
import requests
import pydantic

app = FastAPI(
    title="BlogToReel.ai API",
    description="Backend service for converting blog posts into viral short video scripts.",
    version="1.0.0"
)

# السماح للواجهة الأمامية بالاتصال (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(pydantic.BaseModel):
    url: HttpUrl

@app.get("/")
def read_root():
    return {"message": "Welcome to BlogToReel.ai Backend on Vercel! 🚀"}

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
