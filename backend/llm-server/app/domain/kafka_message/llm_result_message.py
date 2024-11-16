from datetime import datetime

from pydantic import BaseModel

class LLMResultMessage(BaseModel):
    request_id: str
    index_id: str
    content: str