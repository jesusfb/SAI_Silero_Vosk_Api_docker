# tts.py

import torch
import torchaudio
import io

device = None
model = None


# Инициализация при первом вызове
def initialize():
    global device, model
    device = torch.device('cpu')
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                              model='silero_tts',
                              language='ru',
                              speaker='aidar')
    model.to(device)


# Метод синтеза речи
def speak(text):
    global model

    if not model:
        initialize()

    audio = model.apply_tts(text=text)

    buffer = io.BytesIO()
    torchaudio.save(buffer, audio, format='wav')
    buffer.seek(0)

    return buffer