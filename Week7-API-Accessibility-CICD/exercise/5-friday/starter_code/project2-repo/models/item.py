from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt


class Item(BaseModel):
    """Request model (what we send)."""
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    category: Literal["office", "home", "electronics"]
    stock: int = Field(default=0, ge=0)


class ItemOut(Item):
    """Response model (what the API returns). Strict about extra fields and about number types."""
    model_config = ConfigDict(extra="forbid", strict=True)
    id: StrictInt = Field(ge=1)
    price: StrictFloat | StrictInt = Field(ge=0)
    stock: StrictInt = Field(ge=0)


class ItemList(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    page: int
    limit: int
    items: list[ItemOut]
