import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types

from chatbot_config import CHATBOT_TITLE, MODEL_NAME, SYSTEM_PROMPT

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file.")

client = genai.Client(api_key=API_KEY)
app = Flask(__name__, template_folder=str(BASE_DIR))


@app.get("/")
def home():
    return render_template("index.html", chatbot_title=CHATBOT_TITLE)


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    # Keep the context bounded so the browser cannot send an unbounded transcript.
    safe_history = []
    if isinstance(history, list):
        for item in history[-12:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                safe_history.append(f"{role.upper()}: {content[:4000]}")

    conversation = "\n".join(safe_history)
    prompt = (
        f"Conversation so far:\n{conversation}\n\n"
        f"USER: {message}\n\n"
        "Respond to the latest USER message. Stay strictly within your configured scope."
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            ),
        )
        answer = (response.text or "").strip()
        if not answer:
            answer = "I couldn't generate a response. Please try again."
        return jsonify({"answer": answer})
    except Exception as exc:
        app.logger.exception("Gemini API error")
        return jsonify({"error": "Gemini API request failed. Check your API key and server logs."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
