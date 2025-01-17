from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from back.bond_calculator import BondCalculator
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

class BondInput(BaseModel):
    principal: float
    coupon_rate: float
    ytm: float
    maturity_date: str

@app.post("/calculate")
async def calculate_bond(bond_input: BondInput):
    calculator = BondCalculator(
        principal=bond_input.principal,
        coupon_rate=bond_input.coupon_rate,
        ytm=bond_input.ytm,
        maturity_date=bond_input.maturity_date
    )
    return calculator.get_all_metrics()

@app.get("/")
async def root():
    return {"message": "API Bond Calculator"}