import streamlit as st
import openai

# App title
st.set_page_config(page_title="Panther Functions: Exponential Decay", page_icon="📉")
st.title("🐾 Panthers Learn Functions")
st.subheader("📉 Exponential Decay Model Lesson")

# Student input
name = st.text_input("Enter your name:")
avatar = st.selectbox("Choose your multidimensional shape avatar:", ["🔺 Tetrahedron", "🛸 Dodecahedron", "🧊 Cube", "🌀 Torus"])

if name:
    st.success(f"Welcome, {name}! Let's explore exponential decay.")
    st.markdown(f"**Avatar:** {avatar}")

# Lesson display
st.markdown("---")
st.markdown("### 📚 What is Exponential Decay?")
st.markdown("A function that decreases by a consistent ratio over time.")
st.latex(r"f(t) = a \cdot (1 - r)^t")
st.write("Where:")
st.write("- `a` = starting value")
st.write("- `r` = decay rate (as a decimal)")
st.write("- `t` = time")

st.markdown("#### Example Table (90% of previous value each time):")
st.table({
    "Time (t)": [0, 1, 2, 3],
    "Value ($)": [100, 90, 81, 72.9]
})

# ---- LLM Assistant Prompt ----
st.markdown("---")
st.markdown("## 🧠 Ask Dr. X: Guided Exploration")
st.write("Dr. X will now ask you a few questions to activate your prior knowledge.")

# OpenAI setup (replace with your key)
openai.api_key = st.secrets.get("OPENAI_API_KEY")  # Use .streamlit/secrets.toml or env var

# Initial LLM prompt
intro_prompt = f"""
The student named {name} has selected the avatar {avatar}. You're Dr. X, a curious AI educator.
Ask 2-3 short, friendly questions that activate prior knowledge of exponential decay functions.

Start with:
- "What do you already know about exponential change?"
- Use friendly tone, emojis encouraged. Be brief.
"""

if st.button("🧠 Generate Questions"):
    with st.spinner("Dr. X is thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": intro_prompt}]
            )
            st.markdown("### 🤖 Dr. X asks:")
            st.write(response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"LLM error: {e}")

