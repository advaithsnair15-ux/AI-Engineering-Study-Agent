# AI Engineering Study Agent

A Streamlit web application that routes an engineering student's request to one of four tools: topic explanation, MCQ generation, formula calculation, or study-plan creation.

## Features
- Explain engineering topics at different levels.
- Generate multiple-choice practice questions.
- Calculate selected formulas without using `eval()`.
- Create a revision schedule.
- Optional Gemini AI integration. The app also runs in demo mode without an API key.

## Run locally
1. Install Python 3.10 or later.
2. Download/clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Enable AI responses (optional)
1. Create a Gemini API key through Google AI Studio.
2. Set an environment variable named `GEMINI_API_KEY` to the key, or add it to Streamlit secrets:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
3. Never commit API keys to GitHub. Keep `.streamlit/secrets.toml` out of version control.

If no key is configured, the app uses fallback demo responses. The formula calculator supports heat transfer (`Q = m c ΔT`), Ohm's law (`V = I R`), and density (`ρ = m/V`).

## Project architecture
User input → Streamlit interface → AI agent/task router → selected tool → result displayed to user.

See `schema.png`.

## Suggested test cases
- Explain an engineering topic: `Otto cycle`
- Generate MCQ practice: `thermodynamics`
- Calculate heat transfer: formula `heat transfer`, values `m=2, c=4180, dt=15`
- Create a study plan: `manufacturing`, 5 days, 2 hours/day

## Limitations
- The demo calculator intentionally supports only a few named formulas.
- AI-generated explanations and questions can be incorrect; verify them with textbooks or course materials.
- This is an academic prototype, not a certified engineering calculation system.

## Author
Student project — AI Agent Development assignment.
