from flask import Flask, request, Response
from stt import transcribe
from tts import speak

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():

  audio = request.files['audio']

  text = transcribe(audio)

  return {'text': text}


@app.route('/tts', methods=['POST'])
def tts_endpoint():

  text = request.form['text']
  speaker = request.form['speaker']

  audio = speak(text, speaker)

  return Response(audio, mimetype='audio/wav')

if __name__ == "__main__":
    app.run()