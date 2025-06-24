from flask import Flask, render_template, request, send_from_directory
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        format_choice = request.form['format']
        if video:
            filename = str(uuid.uuid4()) + os.path.splitext(video.filename)[1]
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(video_path)

            # Extract audio
            audio_filename = filename.rsplit('.', 1)[0] + f'.{format_choice}'
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path)

            return render_template('index.html', audio_file=audio_filename)

    return render_template('index.html')

@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
