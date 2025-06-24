from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format_type = data.get('format', 'best')

    try:
        yt = YouTube(url)
        title_safe = yt.title.replace(' ', '_').replace('/', '_')
        output_path = os.path.join(DOWNLOAD_FOLDER, title_safe)

        if format_type == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
            filename = output_path + '.mp3'
        elif format_type == '720p':
            stream = yt.streams.filter(progressive=True, res='720p').first()
            filename = output_path + '.mp4'
        elif format_type == '480p':
            stream = yt.streams.filter(progressive=True, res='480p').first()
            filename = output_path + '.mp4'
        elif format_type == 'webm':
            stream = yt.streams.filter(file_extension='webm').first()
            filename = output_path + '.webm'
        else:
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            filename = output_path + '.mp4'

        if not stream:
            return jsonify({'error': 'Nema streama za taj format.'}), 400

        stream.download(output_path=DOWNLOAD_FOLDER, filename=os.path.basename(filename))

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
