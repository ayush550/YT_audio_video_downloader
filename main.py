from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import os
import tempfile
import zipfile
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'mp3')  # 'mp3' or 'mp4' or 'txt'

    if not url or format_type not in ['mp3', 'mp4', 'txt']:
        # return jsonify({'error': 'Invalid URL or format'}), 400
        render_template('fallback.html')

    try:
        # Create a persistent directory for downloads
        temp_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(temp_dir, exist_ok=True)

        # Create a unique subdirectory for this request
        session_dir = tempfile.mkdtemp(dir=temp_dir)
        output_template = os.path.join(session_dir, '%(title)s.%(ext)s')

        # Set options based on format
        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'geo_bypass': True,
                'retries': 10,
                'socket_timeout': 60,
                'connect_timeout': 60,
                'quiet': True
            }
        else:  # mp4
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'quiet': True
            }

        # Download using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Zip the directory
        zip_path = os.path.join(session_dir, 'playlist.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(session_dir):
                if file != 'playlist.zip':
                    zipf.write(os.path.join(session_dir, file), arcname=file)

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
