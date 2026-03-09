import json
from datetime import datetime


def log_route(
    user_message: str,
    intent: str,
    confidence: float,
    final_response: str,
    log_file: str = "route_log.jsonl"
):
    """
    Appends one JSON line to route_log.jsonl for every request.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_message": user_message,
        "intent": intent,
        "confidence": confidence,
        "final_response": final_response
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")