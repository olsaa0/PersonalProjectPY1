from fastapi import FastAPI
from routers import prices
from database import init_db

app = FastAPI(title="Crypto Arbitrage API")


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(prices.router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Crypto Arbitrage Backend is Running!"}
