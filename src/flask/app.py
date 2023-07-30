from flask import Flask, request, Response
from stt import transcribe
#from tts import speak

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
  print("Тестовый запрос получен.")


@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():

  audio = request.files['audio']

  text = transcribe(audio)

  return {'text': text}


#@app.route('/tts', methods=['POST'])
#def tts_endpoint():

  #text = request.form['text']
  #speaker = request.form['speaker']

  #audio = speak(text, speaker)

  return Response(audio, mimetype='audio/wav')

if __name__ == "__main__":
  print("load app")
  app.run(host='0.0.0.0', port=8000)
  print("app ready to work.")