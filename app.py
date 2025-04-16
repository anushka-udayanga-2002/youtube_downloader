from flask import Flask, request, render_template, send_file
import os
import uuid
import yt_dlp

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url or "youtube.com" not in url:
            return render_template('index.html', error="Please enter a valid YouTube URL.")

        try:
            filename = f"{uuid.uuid4()}.mp4"
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            ydl_opts = {
                'format': 'best',
                'outtmpl': filepath,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(filepath, as_attachment=True)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
