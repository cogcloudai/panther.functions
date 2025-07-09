import streamlit as st
import openai

# --- Page Config ---
st.set_page_config(page_title="Panther Functions: Exponential Decay", page_icon="📉")

# --- Title ---
st.title("🐾 Panthers Learn Functions")
st.markdown("Welcome, Englewood STEM Panthers! Enter your name and choose an avatar to begin.")

# --- Student Info ---
name = st.text_input("Enter your name:")
avatar = st.selectbox("Choose your multidimensional shape avatar:", ["🔺 Tetrahedron", "🛸 Dodecahedron", "🧊 Cube", "🌀 Torus"])

if name:
    st.success(f"Welcome, {name}! Let's begin exploring functions.")

    # --- Ask Dr. X (LLM Initial Prompt) ---
    st.markdown("## 🧠 Ask Dr. X: What is your interpretation of a function?")
    st.write("Dr. X wants to hear how YOU understand the concept of a function.")

    user_thought = st.text_area("What do YOU think a function is?")

    if st.button("🔍 Ask Dr. X") and user_thought:
        with st.spinner("Dr. X is thinking..."):
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are Dr. X, a helpful AI teacher."},
                        {"role": "user", "content": f"The student says: '{user_thought}'. Help clarify or support their idea of a function."}
                    ]
                )
                st.markdown("### 🤖 Dr. X says:")
                st.write(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"LLM Error: {e}")

    # --- Tutorial ---
    st.markdown("---")
    st.header("📘 What is a Function?")
    st.write("A **function** is a rule that gives one output for each input. For example:")
    st.latex(r"f(x) = x + 3")
    st.write("If x = 2, then f(x) = 5")

    st.markdown("**Key Terms:**")
    st.write("- **Input (x)**: what goes in")
    st.write("- **Output (f(x))**: what comes out")
    st.write("- **Rule**: how the output is calculated")

    # --- Toggle Functions ---
    st.markdown("---")
    st.header("🔄 Function Playground")
    st.write("Choose a function type and input value to see the output.")

    func_type = st.selectbox("Function type:", ["Linear: f(x)=2x+1", "Quadratic: f(x)=x²", "Exponential: f(x)=3^x", "Decay: f(x)=100(0.9)^x"])
    x_val = st.slider("Choose an input x:", 0, 10, 2)

    if func_type.startswith("Linear"):
        fx = 2 * x_val + 1
    elif func_type.startswith("Quadratic"):
        fx = x_val ** 2
    elif func_type.startswith("Exponential"):
        fx = 3 ** x_val
    elif func_type.startswith("Decay"):
        fx = 100 * (0.9 ** x_val)

    st.success(f"f({x_val}) = {fx:.2f}")

    # --- Exponential Decay Focus ---
    st.markdown("---")
    st.header("📉 Dive Deeper: Exponential Decay")
    st.latex(r"f(x) = 100 \cdot (0.9)^x")

    st.write("- 100 = Starting value")
    st.write("- 0.9 = Decay factor (10% decrease)")
    st.write("- x = Time steps")

    st.write("**What happens as x increases?** Try different values above to observe the shrinking.")

    # --- Reflection Prompt ---
    st.markdown("---")
    st.header("🎓 Reflection with Dr. X")
    reflection = st.text_area("How does decay differ from linear change? What's something in real life that decays?")

    if st.button("📩 Get Dr. X's Thoughts") and reflection:
        with st.spinner("Dr. X is thinking..."):
            try:
                response2 = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You're Dr. X, a mentor for students learning functions."},
                        {"role": "user", "content": reflection}
                    ]
                )
                st.markdown("### 🤖 Dr. X replies:")
                st.write(response2['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"LLM Error: {e}")

# --- Footer Attribution ---
st.markdown("---")
st.markdown("### 🧠 MathCraft Lesson: *Panther.Functions* — developed by Xavier Honablue, M.Ed")
