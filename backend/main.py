from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from hindsight_service import (
    remember_interaction,
    recall_deal,
    reflect_on_deal
)

from deal_store import get_deal, add_interaction


app = FastAPI(
    title="DealMind API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Interaction(BaseModel):
    deal_id: str
    interaction: str


class DealQuestion(BaseModel):
    deal_id: str
    question: str


class NewInteraction(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "DealMind API is running",
        "status": "ready"
    }


@app.get("/api/deals/{deal_id}")
def get_deal_data(deal_id: str):
    deal = get_deal(deal_id)

    if not deal:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return deal


@app.post("/api/deals/{deal_id}/interactions")
def create_interaction(deal_id: str, data: NewInteraction):
    if not data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Interaction cannot be empty"
        )

    # Store in Hindsight first.
    memory_result = remember_interaction(
        deal_id,
        data.text.strip()
    )

    # Also persist application data for the real timeline/dashboard.
    saved = add_interaction(
        deal_id,
        data.text.strip()
    )

    return {
        "success": True,
        "interaction": saved,
        "memory": memory_result
    }


@app.post("/api/interactions")
def add_interaction_legacy(data: Interaction):
    if not data.interaction.strip():
        raise HTTPException(
            status_code=400,
            detail="Interaction cannot be empty"
        )

    memory_result = remember_interaction(
        data.deal_id,
        data.interaction.strip()
    )

    saved = add_interaction(
        data.deal_id,
        data.interaction.strip()
    )

    return {
        "success": True,
        "interaction": saved,
        "memory": memory_result
    }


@app.post("/api/deals/recall")
def recall(data: DealQuestion):
    return recall_deal(
        data.deal_id,
        data.question
    )


@app.post("/api/deals/reflect")
def reflect(data: DealQuestion):
    return reflect_on_deal(
        data.deal_id,
        data.question
    )
