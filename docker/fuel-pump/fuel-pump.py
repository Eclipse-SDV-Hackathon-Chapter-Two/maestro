from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import time
import threading

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

fuel_lock = threading.Lock()
fuel_thread = None
fuel_state = load_fuel_state()

def fill_fuel(update: FuelUpdate):
    global fuel_state
    while update.current_fuel < update.target:
        with fuel_lock:
            update.current_fuel += 1
            fuel_state['fuel_percent'] = update.current_fuel
            save_fuel_state(fuel_state)
        time.sleep(1)        


@app.get("/fuel")
def get_fuel_state():
    return fuel_state

@app.post("/fuel")
def update_fuel_state(update: FuelUpdate):
    if update.current_fuel < 0 or update.target <= 0:
        raise HTTPException(status_code=400, detail="Invalid fuel values")#
    global fuel_thread
    if fuel_thread is None or not fuel_thread.is_alive():
        fuel_thread = threading.Thread(target=fill_fuel, args=(update,))
        fuel_thread.start()
    else:
        raise HTTPException(status_code=400, detail="Fuel update already in progress")
    return 200