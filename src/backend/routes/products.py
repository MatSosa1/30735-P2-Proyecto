from fastapi import APIRouter, HTTPException

from database import get_client
from models import Product, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

TABLE = "products"


@router.get("", response_model=list[Product])
def list_products():
  res = get_client().table(TABLE).select("*").order("id").execute()
  return res.data


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
  res = get_client().table(TABLE).select("*").eq("id", product_id).execute()
  if not res.data:
    raise HTTPException(status_code=404, detail="Product not found")
  return res.data[0]


@router.post("", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
  existing = get_client().table(TABLE).select("id").eq("sku", product.sku).execute()
  if existing.data:
    raise HTTPException(status_code=409, detail="SKU already exists")
  res = get_client().table(TABLE).insert(product.model_dump()).execute()
  return res.data[0]


@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate):
  updates = product.model_dump(exclude_unset=True)
  if not updates:
    raise HTTPException(status_code=400, detail="No fields to update")
  res = get_client().table(TABLE).update(updates).eq("id", product_id).execute()
  if not res.data:
    raise HTTPException(status_code=404, detail="Product not found")
  return res.data[0]


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
  res = get_client().table(TABLE).delete().eq("id", product_id).execute()
  if not res.data:
    raise HTTPException(status_code=404, detail="Product not found")
