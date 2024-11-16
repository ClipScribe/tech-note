import json

from pydantic import BaseModel

class IndexMessage(BaseModel):
    videoId: str
    indices: str