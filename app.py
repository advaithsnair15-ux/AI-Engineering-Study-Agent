import os
import re
import streamlit as st

# Optional AI provider. The app still runs in demo mode without an API key.
try:
    from google import genai
except ImportError:
    genai = None

st.set_page_config(page_title="AI Engineering Study Agent", page_icon="⚙️", layout="centered")

st.title("⚙️ AI Engineering Study Agent")
st.caption("A beginner-friendly study assistant for engineering students.")
st.info("Choose a task, enter your details, and click Run Agent. For AI-generated explanations and questions, add a Gemini API key in Streamlit Secrets. Demo mode works without a key.")

def get_gemini_client():
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        key = None
    key = key or os.getenv("GEMINI_API_KEY")
    if key and genai:
        try:
            return genai.Client(api_key=key)
        except Exception:
            return None
    return None

def ask_ai(prompt):
    client = get_gemini_client()
    if not client:
        return None
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text
    except Exception as exc:
        return "The AI service could not respond. Check your Gemini API key and internet connection. Details: " + str(exc)

def explain_topic(topic, level):
    prompt = f"""You are an accurate engineering tutor. Explain this topic for an engineering student at {level} level: {topic}.
Use clear headings, a simple explanation, key equations with symbols defined, one practical example, and 3 quick revision points.
If the topic is ambiguous, state your assumption. Do not invent numerical facts."""
    ai = ask_ai(prompt)
    if ai:
        return ai
    topic_l = topic.lower()
    if "otto" in topic_l:
        return """## Otto cycle (demo explanation)
The ideal Otto cycle models spark-ignition petrol engines. It has four ideal processes:
1. **1–2: Isentropic compression** — air is compressed; pressure and temperature rise.
2. **2–3: Constant-volume heat addition** — combustion is idealized as heat entering at fixed volume.
3. **3–4: Isentropic expansion** — hot gas expands and produces work.
4. **4–1: Constant-volume heat rejection** — heat leaves the working fluid.

**Air-standard efficiency:** η = 1 − 1/(r^(γ−1)), where r is compression ratio and γ = Cp/Cv.
**Practical link:** Petrol engines are approximated by the Otto cycle.
**Remember:** compression, heat addition, expansion, heat rejection."""
    return f"""## {topic}
**Core idea:** {topic} is an engineering concept whose meaning depends on the specific course context.

**Study it in this order:**
1. Write the definition in your own words.
2. Identify the physical principle and assumptions.
3. List the governing equations and define every symbol.
4. Work through one example with units.
5. Check limiting cases and common mistakes.

**Demo mode note:** Add a Gemini API key to receive a topic-specific AI explanation. This generic guide is provided as a fallback."""

def generate_mcqs(topic, count, difficulty):
    prompt = f"""Create {count} multiple-choice questions for an engineering student on {topic}, difficulty {difficulty}.
Each question must have four options A-D, one correct answer, and a one-sentence explanation. Avoid ambiguous questions. Format clearly."""
    ai = ask_ai(prompt)
    if ai:
        return ai
    return f"""## Practice MCQs: {topic}
**Demo mode:** Add a Gemini API key for automatically generated topic-specific questions.

1. Which is the best first step when solving an engineering numerical?
   A. Substitute numbers immediately
   B. Identify known values and the required quantity
   C. Ignore units
   D. Guess the formula
   **Answer: B.** Listing knowns and unknowns helps select the correct relationship.

2. Why should units be checked in a calculation?
   A. To make the answer longer
   B. To avoid writing equations
   C. To detect inconsistent quantities
   D. Units are never useful
   **Answer: C.** Dimensional consistency can reveal many mistakes.

For full {count}-question, topic-specific practice, configure Gemini API access."""

def calculate_formula(formula, values_text):
    # Safe, explicit supported calculations; no eval() is used.
    values = {}
    for part in values_text.split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            try:
                values[k.strip().lower()] = float(v.strip())
            except ValueError:
                pass
    f = formula.lower().strip()
    if f in ("heat transfer", "q=mcΔt", "q=m*c*dt"):
        needed = ("m", "c", "dt")
        if all(k in values for k in needed):
            q = values["m"] * values["c"] * values["dt"]
            return f"**Result:** Q = m × c × ΔT = **{q:g}** (units depend on the input units)."
        return "For Q = m c ΔT, enter values like `m=2, c=4180, dt=15`."
    if f in ("ohm's law", "ohms law", "v=ir"):
        if "i" in values and "r" in values:
            return f"**Voltage:** V = I × R = **{values['i']*values['r']:g} V**"
        if "v" in values and "r" in values and values["r"] != 0:
            return f"**Current:** I = V / R = **{values['v']/values['r']:g} A**"
        return "For Ohm's law, enter `i=2, r=5` to calculate voltage, or `v=10, r=5` to calculate current."
    if f in ("density", "rho=m/v", "rho=m/v"):
        if "m" in values and "v" in values and values["v"] != 0:
            return f"**Density:** ρ = m / V = **{values['m']/values['v']:g}** (input-dependent units)."
        return "For density, enter `m=10, v=2`."
    return "Supported demo calculations: `heat transfer` (Q = mcΔT), `Ohm's law` (V = IR), and `density` (ρ = m/V). Use the exact formula name and enter values as comma-separated key=value pairs."

def make_study_plan(topic, days, hours):
    prompt = f"""Create a realistic {days}-day revision plan for an engineering student studying {topic}, with {hours} study hours per day. Include daily goals, practice questions, breaks, and a final review."""
    ai = ask_ai(prompt)
    if ai:
        return ai
    per_day = max(1, int(hours))
    lines = [f"## {days}-day revision plan: {topic}", f"Target: about {hours} study hours per day."]
    for day in range(1, int(days)+1):
        if day == int(days):
            task = "Revise summaries, solve a mixed practice set, and review mistakes."
        elif day == 1:
            task = "Review fundamentals, definitions, assumptions, and core formulas."
        elif day == 2:
            task = "Study worked examples and create a one-page formula sheet."
        else:
            task = "Practise problems/MCQs, revisit weak areas, and explain key ideas aloud."
        lines.append(f"- **Day {day}:** {task} ({per_day} focused hour(s), with short breaks).")
    lines.append("\\n**Demo mode:** Add a Gemini API key for a more detailed personalized plan.")
    return "\\n".join(lines)

with st.sidebar:
    st.header("Agent tools")
    st.write("The agent routes your request to one of four tools:")
    st.markdown("- Explain a topic\\n- Generate MCQs\\n- Calculate a formula\\n- Create a study plan")
    st.caption("API key is optional for demo mode.")

task = st.selectbox(
    "What do you want the agent to do?",
    ["Explain an engineering topic", "Generate MCQ practice", "Calculate an engineering formula", "Create a study plan"]
)

if task == "Explain an engineering topic":
    topic = st.text_input("Topic", placeholder="e.g., Otto cycle, heat transfer, CNC turning")
    level = st.selectbox("Explanation level", ["Beginner", "Exam revision", "Intermediate"])
    count = difficulty = None
elif task == "Generate MCQ practice":
    topic = st.text_input("Topic", placeholder="e.g., thermodynamics, manufacturing")
    count = st.slider("Number of questions", 3, 15, 5)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    level = None
elif task == "Calculate an engineering formula":
    topic = st.selectbox("Formula", ["heat transfer", "Ohm's law", "density"])
    values_text = st.text_input("Values (comma-separated)", placeholder="e.g., m=2, c=4180, dt=15")
    level = count = difficulty = None
else:
    topic = st.text_input("Subject or topic", placeholder="e.g., thermodynamics")
    days = st.slider("Number of days", 1, 14, 5)
    hours = st.slider("Study hours per day", 1, 8, 2)
    level = count = difficulty = None

if st.button("▶ Run Agent", type="primary", use_container_width=True):
    if task != "Calculate an engineering formula" and not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Agent is selecting and running the appropriate tool..."):
            if task == "Explain an engineering topic":
                result = explain_topic(topic, level)
            elif task == "Generate MCQ practice":
                result = generate_mcqs(topic, count, difficulty)
            elif task == "Calculate an engineering formula":
                result = calculate_formula(topic, values_text)
            else:
                result = make_study_plan(topic, days, hours)
        st.subheader("Agent result")
        st.markdown(result)

st.divider()
st.caption("Academic prototype. Verify AI-generated content and calculations before relying on them.")
