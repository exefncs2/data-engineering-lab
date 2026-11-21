"""RAG 測試 API 之 Pydantic v2 請求與回應模型。"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VectorBase(BaseModel):
    description: Optional[str] = None


class VectorCreate(VectorBase):
    name: str = Field(..., examples=["Vector Name"])


class VectorUpdate(VectorBase):
    name: Optional[str] = Field(None, examples=["New Vector Name"])


class Vector(VectorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: int


class TextProcessRequest(BaseModel):
    text: str = Field(..., examples=["Sample text to process."])
    chunk_size: Optional[int] = Field(default=512, examples=[512])


class GPTGenerateRequest(BaseModel):
    prompt: str = Field(..., examples=["Once upon a time,"])
    max_length: Optional[int] = Field(default=50, examples=[50])
    temperature: Optional[float] = Field(default=1.0, examples=[1.0])
