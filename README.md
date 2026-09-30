# All Chatbot Collection

This archive contains 10 independent Flask + Google Gemini API chatbots.

## Common stack
- Python 3.10+
- Flask
- google-genai
- python-dotenv
- Gunicorn
- Gemini model: `gemini-3.1-flash-lite`

## Run any chatbot

1. Open the chatbot folder.
2. Create/activate a virtual environment.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Put your Google Gemini API key in `.env`:
   `GEMINI_API_KEY=your_key_here`
5. Start locally:
   `python app.py`
6. Or with Gunicorn:
   `gunicorn app:app`

The API key must remain server-side. Do not commit `.env`.

Each chatbot has its topic restriction implemented in `chatbot_config.py` and reinforced by the server-side system instruction.
