from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_items():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data = sorted(data, key=lambda x: x["created_at"], reverse=True)[:100]

   # Build simple HTML table
    html = """
    <html>
    <head>
        <title>Live Internet Tracker</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f9f9f9; }
            h1 { color: #333; }
            a { text-decoration: none; color: #007acc; }
            a:hover { text-decoration: underline; }
            .item { padding: 8px; background: #fff; margin-bottom: 8px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>🌍 New Things on GitHub</h1>
    """

    for item in data:
        html += f"""
        <div class='item'>
            <b>{item['title']}</b><br>
            <a href='{item['url']}' target='_blank'>{item['url']}</a><br>
            <small>Author: {item['author']['name']} | {item['created_at']}</small>
        </div>
        """

    html += "</body></html>"
    return html