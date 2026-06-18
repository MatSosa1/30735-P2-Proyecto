from fastapi import FastAPI

from routes.products import router as products_router

app = FastAPI(title="Stock API", version="1.0.0")

app.include_router(products_router)


@app.get("/health")
def health():
  return {"status": "ok"}
