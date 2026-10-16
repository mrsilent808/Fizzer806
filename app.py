import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fizzer - Free YouTube Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); width: 100%; max-width: 450px; text-align: center; }
        h1 { color: #38bdf8; margin-bottom: 10px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
        input[type="text"] { width: 100%; padding: 12px; border: 1px solid #334155; background: #0f172a; color: #fff; border-radius: 6px; margin-bottom: 15px; box-sizing: border-box; }
        button { background: #0284c7; color: white; border: none; padding: 12px; width: 100%; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #0369a1; }
        .footer { margin-top: 20px; font-size: 12px; color: #64748b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Fizzer</h1>
        <p>Free YouTube Video & Audio Downloader</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube URL here..." required>
            <button type="submit">Download Now</button>
        </form>
        <div class="footer">Hosted on Hugging Face Spaces | 100% Free</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "URL missing", 400
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}", 500

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
