from pydantic import BaseModel

class InitiateRequestMessage(BaseModel):
    request_id: str
    total_chunk_num: int
    explanation_level: str