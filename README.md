# 🎭 Moody Talk

<img width="959" height="391" alt="image" src="https://github.com/user-attachments/assets/61b25a02-fe1b-4ced-9d55-eae9d336adbe" />

A mood-based AI chatbot built with **LangChain**, **Mistral AI**, and a **Streamlit** UI. Pick a mood — sad, funny, or angry — and chat with an AI that responds entirely in that tone.

## Features

- Three selectable AI moods, each with a distinct system prompt:
  - 😢 **Sad** — responds in a depressed, emotional tone
  - 😂 **Funny** — responds with humor and jokes
  - 😡 **Angry** — responds aggressively and impatiently
- Clean chat interface built with Streamlit's native chat components
- Mood-specific colors, avatars, and backgrounds
- Option to switch moods or clear the conversation mid-session
- Also includes a simple CLI version (`chat.py`) for terminal-based chatting

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — chat message orchestration
- [Mistral AI](https://mistral.ai/) (`mistral-small-2506`) — language model
- `python-dotenv` — environment variable management

## Files

| File | Description |
|---|---|
| `UIchatbot.py` | Streamlit web app with mood selection and chat UI |
| `chat.py` | Command-line version of the chatbot |
| `requirements.txt` | Python dependencies |

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/prekkkk/moody-talk.git
   cd moody-talk
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

## Usage

**Streamlit app:**
```bash
streamlit run UIchatbot.py
```

**CLI version:**
```bash
python chat.py
```
Type `0` at any point to exit the conversation.

## Note

This project is for learning/demo purposes. Model responses are generated live via the Mistral API, so a valid API key is required to run it.
