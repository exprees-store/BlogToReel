from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ArticleRequest(BaseModel):
    url: str

@app.post("/api/index")
@app.post("/")
async def process_article(data: ArticleRequest):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(data.url, headers=headers, timeout=10)
        
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Could not fetch URL (Status: {resp.status_code})")
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title Found"
        paragraphs = soup.find_all('p')
        text_snippet = " ".join([p.get_text() for p in paragraphs[:4]]) if paragraphs else "No paragraphs found."
        
        if len(text_snippet) > 300:
            text_snippet = text_snippet[:300] + "..."

        return {
            "status": "success",
            "title": title.strip(),
            "summary": f"Extracted text preview: {text_snippet}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
