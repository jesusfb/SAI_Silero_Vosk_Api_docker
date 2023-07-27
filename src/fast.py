from fastapi import FastAPI, File, UploadFile, Response
from pydantic import BaseModel
from stt import transcribe
from tts import speak

app = FastAPI()


class TranscribeRequest(BaseModel):
    audio: bytes


class TTSRequest(BaseModel):
    text: str
    speaker: str


@app.post("/transcribe")
async def transcribe(request: TranscribeRequest):
    audio = request.audio
    text = transcribe(audio)
    return {"text": text}


@app.post("/tts")
async def tts(request: TTSRequest):
    audio = speak(request.text, request.speaker)
    return Response(audio, media_type="audio/mpeg")


if __name__ == "__main__":
    print("FastAPI starting")
    import uvicorn

    uvicorn.run("app:app", port=8000)