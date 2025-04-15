
from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        return f"Downloaded: {yt.title}"
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_streams', methods=['POST'])
def get_streams():
    url = request.form['url']
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    audio_stream = yt.streams.filter(only_audio=True).first()

    return render_template('index.html', url=url, streams=streams, audio_stream=audio_stream, title=yt.title)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    stream_itag = request.form['itag']
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(stream_itag)
    
    filename = f"{uuid.uuid4()}.mp4" if "video" in stream.mime_type else f"{uuid.uuid4()}.mp3"
    filepath = stream.download(filename=filename)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
