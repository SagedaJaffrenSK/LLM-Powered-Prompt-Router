from classifier import classify_intent
from router import route_and_respond
from logger import log_route

# ── 15 required test messages ─────────────────────────────────────────────────
TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose.",
]


def process_message(message: str) -> None:
    print("\n" + "═" * 60)
    print(f"📨 User: {message}")

    # Step 1: Classify
    intent_data = classify_intent(message)
    print(f"🔍 Intent: {intent_data['intent']}  |  Confidence: {intent_data['confidence']:.2f}")

    # Step 2: Route & Respond
    response = route_and_respond(message, intent_data)
    print(f"🤖 Response:\n{response}")

    # Step 3: Log
    log_route(
        user_message=message,
        intent=intent_data["intent"],
        confidence=intent_data["confidence"],
        final_response=response
    )


def interactive_mode():
    print("\n🚀 LLM Prompt Router — Interactive Mode")
    print("Type 'quit' to exit. Prefix with @code, @data, @writing, or @career to override routing.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if user_input:
            process_message(user_input)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running all 15 test messages...\n")
        for msg in TEST_MESSAGES:
            process_message(msg)
    else:
        interactive_mode()