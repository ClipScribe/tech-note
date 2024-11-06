from pydantic import BaseModel
import io


class AudioChunk(BaseModel):
    chunk_id: int
    chunk_data: io.BytesIO

    class Config:
        arbitrary_types_allowed = True  # BytesIO와 같은 임의 타입을 허용