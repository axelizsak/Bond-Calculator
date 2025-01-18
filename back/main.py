from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from .bond_calculator import BondCalculator
from .agent import agent_executor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "CONNECT"],
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

@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            message = await websocket.receive_text()
            
            try:
                # Utiliser l'agent pour générer une réponse
                result = await agent_executor.ainvoke(
                    {"input": message}
                )
                
                # Extraire la réponse de manière plus propre
                if isinstance(result, dict) and "output" in result:
                    # Nettoyer la sortie
                    output = result["output"]
                    # Enlever les répétitions potentielles
                    if isinstance(output, str):
                        # Diviser sur les points pour ne garder que la première phrase complète
                        sentences = output.split('.')
                        output = sentences[0] + '.' if sentences else output
                else:
                    output = "Je suis désolé, je n'ai pas pu traiter votre demande."
                
                await websocket.send_text(output)
                
            except Exception as e:
                print(f"Agent error: {str(e)}")
                await websocket.send_text("Je suis désolé, pouvez-vous reformuler votre question ?")
            
        except Exception as e:
            print(f"WebSocket error: {str(e)}")
            break