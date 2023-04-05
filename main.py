from flask import Flask, render_template, request, send_file
import subprocess
import ffmpeg
import stable_whisper
import sys
import flask

model = stable_whisper.load_model('base')

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload():

    video = request.files['video']
    if video.filename == '':
        return 'No video selected'
    video.save('static/videos/' + video.filename)
    try:
        video_path = 'static/videos/' + video.filename
        # extract audio from video
        audio_path = "static/audios/" + video.filename.split(".")[0] + '.mp3'
        subprocess.call('ffmpeg -i "{}" -vn "{}'.format(video_path, audio_path), shell=True)

        # generate srt file
        srt_path = "static/subtitles/" + video.filename.split(".")[0] + '.srt'
        transcript = model.transcribe(audio_path)
        transcript.to_srt_vtt(srt_path)
        
        # add srt to video (concat)
        output_path = "static/output/" + video.filename
        video = ffmpeg.input(video_path)
        audio = video.audio
        ffmpeg.concat(video.filter("subtitles", srt_path), audio, v=1, a=1).output(output_path).run()
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    
    
    return flask.jsonify({"success":"true"})
    

@app.route('/download/<filename>')
def download_file(filename):

	path = "static/output/" + filename

	return send_file(path, as_attachment=True)

    
if __name__ == '__main__':
    app.run(debug=True)