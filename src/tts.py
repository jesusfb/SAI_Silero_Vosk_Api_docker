import torch
import torchaudio
import io

print("tts: silero module start initialize.")

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000 # 48000
speaker = 'aidar' # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu') # cpu или gpu


SPEAKERS = ['aidar', 'kseniya', 'baya']

# Словарь для хранения моделей
models = {}

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                  model='silero_tts',
                                  language='ru',
                                  speaker='kseniya')
model.to(device)

print("tts: silero complete loading model")


# Загрузка моделей при импорте
def load_models():
    device = torch.device("cpu")

    print("tts: start loading models")
    for speaker in SPEAKERS:
        model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                  model='silero_tts',
                                  language='ru',
                                  speaker=speaker)
        model.to(device)
        models[speaker] = model
        print("tts: silero complete loading model: " + speaker)


# Метод синтеза речи
def speak(text, speaker=None):
    # Выбор модели
    if not speaker:
        speaker = 'kseniya'

    model = models[speaker]

    # Генерация аудио
    audio = model.apply_tts(text=text,
                            speaker=speaker)

    # Сохранение в буфер
    buffer = io.BytesIO()
    torchaudio.save(buffer, audio, format='wav')
    buffer.seek(0)

    return buffer


# Загрузка моделей
#load_models()

print("tts: silero module complete initialize.")