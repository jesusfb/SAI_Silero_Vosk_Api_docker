import vosk
import json

model = vosk.Model("model")
samplerate = 16000
device = 1

# Распознаватель Kaldi
rec = vosk.KaldiRecognizer(model, 16000)


# Метод распознавания
def transcribe(audio_file):
    rec.AcceptWaveform(audio_file)
    result = rec.FinalResult()

    text = json.loads(result)['text']

    return text