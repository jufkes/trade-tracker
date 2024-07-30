from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from handlers import strategies

app = FastAPI()

class Strategy(BaseModel):
    name: str
    description: Optional[str] = None
    links: Optional[list] = None

@app.get("/")
async def root():
    return {"Hello": "World"}
@app.get("/strategies/")
async def get_strategies():
    return strategies.get_all_strategies()

@app.post("/strategies/strategy")
async def create_strategy(strategy: Strategy):
    return strategies.create_strategy(strategy)

@app.get("/strategies/{strategy}")
async def get_strategy(strategy):
    return strategies.get_strategy(strategy)