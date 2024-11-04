from pydantic import BaseModel

class AudioChunk(BaseModel):
    chunk_id: int
    chunk_data: bytes