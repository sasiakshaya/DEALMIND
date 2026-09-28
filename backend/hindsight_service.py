import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv(".env")

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "dealmind")


def remember_interaction(deal_id, interaction):
    client.retain(
        bank_id=BANK_ID,
        content=interaction,
        metadata={"deal_id": deal_id}
    )

    return {
        "success": True,
        "deal_id": deal_id,
        "message": "Interaction stored in Hindsight"
    }


def recall_deal(deal_id, query):
    result = client.recall(
        bank_id=BANK_ID,
        query=query,
        max_tokens=1000
    )

    memories = []

    for item in result.results:
        metadata = item.metadata or {}

        if metadata.get("deal_id") == deal_id:
            memories.append({
                "text": item.text,
                "type": item.type
            })

    return {
        "deal_id": deal_id,
        "question": query,
        "memories": memories,
        "memory_count": len(memories)
    }


def reflect_on_deal(deal_id, question):
    # First retrieve the actual memories for this deal.
    recalled = recall_deal(
        deal_id,
        "Important facts, customer concerns, decision makers, competitors, requests, risks, and upcoming actions for this deal"
    )

    memory_text = "\n".join(
        f"- {item['text']}"
        for item in recalled["memories"]
    )

    if not memory_text:
        memory_text = "No verified deal memories were found."

    grounded_question = f"""
Prepare a meeting brief for deal {deal_id}.

Use ONLY the verified deal memories below.

VERIFIED DEAL MEMORIES:
{memory_text}

RULES:
1. Do not invent dates, schedules, deadlines, names, numbers, commitments, or events.
2. Do not assume that "next week" means a specific date range.
3. Do not add facts that are not present in the verified memories.
4. If something is unknown, explicitly say it is not available in the stored memory.
5. Clearly separate known facts from recommendations.
6. NEVER convert relative dates such as "next week", "tomorrow", or "later" into calendar dates.
7. Only output an exact calendar date when that exact date is explicitly present in verified deal memories.
8. If the memory says "next week", write "next week".
9. Give:
   - What I should know
   - Main risks
   - Recommended actions
   - Important unknowns
"""

    result = client.reflect(
        bank_id=BANK_ID,
        query=grounded_question,
        context=memory_text,
        budget="low"
    )

    return {
        "deal_id": deal_id,
        "question": question,
        "answer": result.text
    }