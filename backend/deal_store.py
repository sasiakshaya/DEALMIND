import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).parent / "deal_data.json"

SEED_DEAL = {
    "deal_id": "acme-001",
    "company": "ACME Corp",
    "product": "Enterprise Analytics Platform",
    "stage": "Proposal",
    "interactions": [
        {
            "id": 1,
            "date": "2026-09-24",
            "text": "ACME Corp is interested in our enterprise analytics platform because they need better visibility into sales performance and reporting."
        },
        {
            "id": 2,
            "date": "2026-09-25",
            "text": "The customer said our pricing is too high and asked whether we can offer a discount."
        },
        {
            "id": 3,
            "date": "2026-09-26",
            "text": "ACME Corp is also evaluating Salesforce as an alternative solution."
        },
        {
            "id": 4,
            "date": "2026-09-27",
            "text": "The CTO will be the final technical decision maker. The CTO is particularly concerned about integration effort and implementation risk."
        },
        {
            "id": 5,
            "date": "2026-09-28",
            "text": "ACME Corp requested a revised proposal with flexible pricing before the next meeting."
        }
    ]
}


def _load():
    if not DATA_FILE.exists():
        _save({"deals": {"acme-001": SEED_DEAL}})

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_deal(deal_id):
    data = _load()

    deal = data["deals"].get(deal_id)

    if not deal:
        return None

    return deal


def add_interaction(deal_id, text):
    data = _load()

    if deal_id not in data["deals"]:
        data["deals"][deal_id] = {
            "deal_id": deal_id,
            "company": "Unknown Company",
            "product": "Unknown Product",
            "stage": "New",
            "interactions": []
        }

    interactions = data["deals"][deal_id]["interactions"]

    next_id = max([x["id"] for x in interactions], default=0) + 1

    interactions.append({
        "id": next_id,
        "date": date.today().isoformat(),
        "text": text
    })

    _save(data)

    return interactions[-1]
