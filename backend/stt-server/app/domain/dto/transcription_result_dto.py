import datetime
from pydantic import BaseModel

class TranscriptionResult(BaseModel):
    chunk_id: int
    transcription_text: str