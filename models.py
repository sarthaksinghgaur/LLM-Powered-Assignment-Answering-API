from pydantic import BaseModel
from typing import List

class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str