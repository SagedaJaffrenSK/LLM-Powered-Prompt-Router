import os
from groq import Groq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CONFIDENCE_THRESHOLD

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_and_respond(message: str, intent_data: dict) -> str:
    try:
        intent = intent_data.get("intent", "unclear")
        confidence = intent_data.get("confidence", 0.0)

        if confidence < CONFIDENCE_THRESHOLD and intent != "unclear":
            print(f"[Router] Low confidence ({confidence:.2f}) for '{intent}' — routing to 'unclear'")
            intent = "unclear"

        for label in SYSTEM_PROMPTS:
            if message.lower().startswith(f"@{label}"):
                print(f"[Router] Manual override detected: routing to '{label}'")
                intent = label
                message = message[len(f"@{label}"):].strip()
                break

        system_prompt = SYSTEM_PROMPTS.get(intent, SYSTEM_PROMPTS["unclear"])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[Router Error] {e}")
        return "Sorry, I encountered an error generating a response. Please try again."