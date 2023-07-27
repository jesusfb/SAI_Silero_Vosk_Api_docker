import torch
import torchaudio
import io

SPEAKERS = ['aidar', 'kseniya', 'baya']

# Словарь для хранения моделей
models = {}


# Загрузка моделей при импорте
def load_models():
    device = torch.device('cpu')

    for speaker in SPEAKERS:
        model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                  model='silero_tts',
                                  language='ru',
                                  speaker=speaker)
        model.to(device)
        models[speaker] = model


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
load_models()