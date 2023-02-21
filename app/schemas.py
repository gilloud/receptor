from typing import Any
from pydantic import BaseModel



class Wdp4EventPushed(BaseModel):
    content: Any

class WyresDecodedPayload(BaseModel):
    content: Any
