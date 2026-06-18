from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
  sku: str = Field(min_length=1, max_length=64)
  name: str = Field(min_length=1, max_length=200)
  description: str | None = Field(default=None, max_length=2000)
  quantity: int = Field(ge=0)
  price: float = Field(ge=0)


class ProductUpdate(BaseModel):
  sku: str | None = Field(default=None, min_length=1, max_length=64)
  name: str | None = Field(default=None, min_length=1, max_length=200)
  description: str | None = Field(default=None, max_length=2000)
  quantity: int | None = Field(default=None, ge=0)
  price: float | None = Field(default=None, ge=0)


class Product(ProductCreate):
  id: int
