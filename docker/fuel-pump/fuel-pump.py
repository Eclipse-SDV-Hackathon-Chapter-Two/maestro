from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import time

app = FastAPI()

FUEL_STATE_FILE = 'fuel_state.json'

class FuelUpdate(BaseModel):
    current_fuel: int
    target: int

def load_fuel_state():
    if os.path.exists(FUEL_STATE_FILE):
        with open(FUEL_STATE_FILE, 'r') as file:
            return json.load(file)
    return {"fuel_percent": 0}

def save_fuel_state(state):
    with open(FUEL_STATE_FILE, 'w') as file:
        json.dump(state, file)

fuel_state = load_fuel_state()

@app.get("/fuel")
def get_fuel_state():
    return fuel_state

@app.post("/fuel")
def update_fuel_state(update: FuelUpdate):
    if update.current_fuel < 0 or update.target <= 0:
        raise HTTPException(status_code=400, detail="Invalid fuel values")#
    while update.current_fuel < update.target:
        update.current_fuel += 1
        save_fuel_state(fuel_state)
        time.sleep(1)
    return fuel_state