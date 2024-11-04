

class TranscriptionResult(BaseModel):
    request_id: str
    chunk_id: int
    timestamp: datetime
    transcription_text: str