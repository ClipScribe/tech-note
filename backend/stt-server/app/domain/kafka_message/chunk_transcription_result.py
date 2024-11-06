import datetime
from pydantic import BaseModel

class TranscriptionResultMessage(BaseModel):
    request_id: str
    chunk_id: int
    transcription_text: str