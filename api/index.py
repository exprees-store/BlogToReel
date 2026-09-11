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
                const response = await window.location.origin + '/api/process';
                const res = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                
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
