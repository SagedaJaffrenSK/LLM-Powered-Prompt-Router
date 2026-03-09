import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CLASSIFIER_PROMPT = """Your task is to classify the user's intent.
Based on the user message below, choose one of the following labels:
  - code      → programming, debugging, software, scripts, algorithms
  - data      → data analysis, statistics, spreadsheets, SQL, numbers
  - writing   → editing, proofreading, tone, clarity, essays, paragraphs
  - career    → jobs, resumes, interviews, career decisions, cover letters
  - unclear   → anything that doesn't clearly fit the above

Respond with ONLY a single valid JSON object. No explanation, no markdown, no extra text.
Format: {"intent": "<label>", "confidence": <float between 0.0 and 1.0>}"""


def classify_intent(message: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.0,
            max_tokens=60
        )
        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "").strip()

        result = json.loads(raw)

        if "intent" not in result or "confidence" not in result:
            raise ValueError("Missing required keys.")

        result["intent"] = str(result["intent"]).lower()
        result["confidence"] = float(result["confidence"])
        return result

    except Exception as e:
        print(f"[Classifier Error] {e} — defaulting to 'unclear'")
        return {"intent": "unclear", "confidence": 0.0}