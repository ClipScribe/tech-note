from pydantic import BaseModel

class STTChunkResultMessage(BaseModel):
    request_id: str
    chunk_id: int
    transcription_text: str