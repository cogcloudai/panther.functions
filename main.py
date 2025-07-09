import streamlit as st
from openai import OpenAI
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Panther Functions: Exponential Decay", 
    page_icon="📉",
    layout="wide"
)

# --- Initialize Session State ---
if 'ask_drx' not in st.session_state:
    st.session_state.ask_drx = False
if 'get_drx_reflection' not in st.session_state:
    st.session_state.get_drx_reflection = False

# --- Helper Functions ---
def calculate_function(func_type, x_val):
    """Calculate function output based on type and input"""
    if func_type.startswith("Linear"):
        return 2 * x_val + 1
    elif func_type.startswith("Quadratic"):
        return x_val ** 2
    elif func_type.startswith("Exponential"):
        return 3 ** x_val
    elif func_type.startswith("Decay"):
        return 100 * (0.9 ** x_val)
    return 0

def create_function_chart(func_type, current_x):
    """Create matplotlib chart for the selected function"""
    x_vals = np.linspace(0, 10, 100)
    
    if func_type.startswith("Linear"):
        y_vals = 2 * x_vals + 1
        title = "Linear Function: f(x) = 2x + 1"
        color = 'blue'
    elif func_type.startswith("Quadratic"):
        y_vals = x_vals ** 2
        title = "Quadratic Function: f(x) = x²"
        color = 'green'
    elif func_type.startswith("Exponential"):
        y_vals = 3 ** x_vals
        title = "Exponential Function: f(x) = 3^x"
        color = 'orange'
    elif func_type.startswith("Decay"):
        y_vals = 100 * (0.9 ** x_vals)
        title = "Exponential Decay: f(x) = 100(0.9)^x"
        color = 'red'
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot function curve
    ax.plot(x_vals, y_vals, color=color, linewidth=3, label='Function')
    
    # Plot current point
    current_y = calculate_function(func_type, current_x)
    ax.plot(current_x, current_y, 'ro', markersize=10, label=f'f({current_x}) = {current_y:.2f}')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Input (x)', fontsize=12)
    ax.set_ylabel('Output f(x)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    return fig

# --- Main App ---
st.title("🐾 Panthers Learn Functions")
st.markdown("Welcome, Englewood STEM Panthers! Enter your name and choose an avatar to begin.")

# --- Student Info ---
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Enter your name:")
with col2:
    avatar = st.selectbox(
        "Choose your multidimensional shape avatar:", 
        ["🔺 Tetrahedron", "🚘 Dodecahedron", "🪒 Cube", "🌀 Torus"]
    )

if name:
    st.success(f"Welcome, {name} {avatar}! Let's begin exploring functions.")

    # --- Ask Dr. X Section ---
    st.markdown("## 🧠 Ask Dr. X: What is your interpretation of a function?")
    st.write("Dr. X wants to hear how YOU understand the concept of a function.")

    # Simplified chat interface
    user_question = st.text_input("Ask Dr. X a question about functions:")
    
    if st.button("Ask Dr. X") and user_question:
        with st.spinner("Dr. X is thinking..."):
            try:
                if 'OPENAI_API_KEY' in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system", 
                                "content": "You're Dr. X, an enthusiastic AI tutor helping students understand mathematical functions. Keep responses concise, encouraging, and age-appropriate for high school students."
                            },
                            {
                                "role": "user", 
                                "content": f"Student question about functions: {user_question}"
                            }
                        ],
                        max_tokens=200
                    )
                    st.markdown("### 🧠 Dr. X replies:")
                    st.info(response.choices[0].message.content)
                else:
                    st.markdown("### 🧠 Dr. X replies:")
                    st.info("Great question! A function is like a machine that takes an input and gives you exactly one output following a specific rule. Think of it like a vending machine - you put in money (input) and get a specific snack (output) based on which button you press (the rule)!")
            except Exception as e:
                st.error(f"Dr. X is having technical difficulties: {str(e)}")

    # --- Tutorial Section ---
    st.markdown("---")
    st.header("📘 What is a Function?")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("A **function** is a rule that gives exactly one output for each input.")
        st.latex(r"f(x) = x + 3")
        st.write("If x = 2, then f(x) = 5")
        
        st.markdown("**Think of it like:**")
        st.write("🍎 **Input Machine**: You put in a number")
        st.write("⚙️ **Processing**: The function applies its rule")  
        st.write("📤 **Output**: You get exactly one result")
    
    with col2:
        st.markdown("**Key Terms:**")
        st.write("• **Input (x)**: what goes in")
        st.write("• **Output (f(x))**: what comes out")
        st.write("• **Rule**: how the output is calculated")

    # --- Interactive Function Playground ---
    st.markdown("---")
    st.header("🔄 Function Playground")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("Choose a function type and input value to see the output.")
        
        func_type = st.selectbox(
            "Function type:", 
            [
                "Linear: f(x)=2x+1", 
                "Quadratic: f(x)=x²", 
                "Exponential: f(x)=3^x", 
                "Decay: f(x)=100(0.9)^x"
            ]
        )
        
        x_val = st.slider("Choose an input x:", 0, 10, 2)
        
        fx = calculate_function(func_type, x_val)
        st.success(f"f({x_val}) = {fx:.2f}")
        
        # Show the calculation steps
        if func_type.startswith("Linear"):
            st.write(f"**Calculation:** f({x_val}) = 2({x_val}) + 1 = {fx}")
        elif func_type.startswith("Quadratic"):
            st.write(f"**Calculation:** f({x_val}) = {x_val}² = {fx}")
        elif func_type.startswith("Exponential"):
            st.write(f"**Calculation:** f({x_val}) = 3^{x_val} = {fx}")
        elif func_type.startswith("Decay"):
            st.write(f"**Calculation:** f({x_val}) = 100 × (0.9)^{x_val} = {fx:.2f}")
    
    with col2:
        # Display matplotlib chart
        try:
            fig = create_function_chart(func_type, x_val)
            st.pyplot(fig)
        except Exception as e:
            st.write("📊 Chart would display here")
            st.write(f"Current point: ({x_val}, {fx:.2f})")

    # --- Exponential Decay Focus ---
    st.markdown("---")
    st.header("📉 Dive Deeper: Exponential Decay")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.latex(r"f(x) = 100 \cdot (0.9)^x")
        st.write("• **100** = Starting value")
        st.write("• **0.9** = Decay factor (10% decrease each step)")
        st.write("• **x** = Time steps")
        st.write("**What happens as x increases?** The value gets smaller and smaller!")
        
        st.markdown("### 🤔 Think About It:")
        st.write("- After 1 step: 90% remains (10% lost)")
        st.write("- After 2 steps: 81% remains (19% lost total)")
        st.write("- After 3 steps: 72.9% remains (27.1% lost total)")
    
    with col2:
        # Show decay table
        st.write("**Decay Table:**")
        decay_data = []
        for i in range(11):
            value = 100 * (0.9 ** i)
            percent_remaining = value
            decay_data.append({
                "Time (x)": i, 
                "Value f(x)": f"{value:.1f}",
                "% Remaining": f"{percent_remaining:.1f}%"
            })
        
        df = pd.DataFrame(decay_data)
        st.dataframe(df, height=300)

    # --- Real World Examples ---
    st.markdown("### 🌍 Real World Examples of Exponential Decay:")
    
    examples_col1, examples_col2 = st.columns(2)
    
    with examples_col1:
        st.write("**Technology & Daily Life:**")
        st.write("📱 Phone battery losing charge")
        st.write("🌡️ Hot coffee cooling down")
        st.write("🚗 Car value depreciating")
        st.write("📡 WiFi signal getting weaker with distance")
        
    with examples_col2:
        st.write("**Science & Medicine:**")
        st.write("☢️ Radioactive materials breaking down")
        st.write("💊 Medicine leaving your body")
        st.write("🧬 Population decline in endangered species")
        st.write("🌊 Sound waves getting quieter")

    # --- Interactive Decay Example ---
    st.markdown("---")
    st.subheader("🔋 Interactive Example: Phone Battery")
    
    battery_col1, battery_col2 = st.columns(2)
    
    with battery_col1:
        hours = st.slider("Hours since full charge:", 0, 24, 8)
        battery_percent = 100 * (0.92 ** hours)  # 8% loss per hour
        
        st.write(f"**After {hours} hours:**")
        st.write(f"Battery: {battery_percent:.1f}%")
        
        # Visual battery indicator
        if battery_percent > 75:
            st.success(f"🔋🔋🔋🔋 {battery_percent:.1f}%")
        elif battery_percent > 50:
            st.warning(f"🔋🔋🔋 {battery_percent:.1f}%")
        elif battery_percent > 25:
            st.warning(f"🔋🔋 {battery_percent:.1f}%")
        else:
            st.error(f"🔋 {battery_percent:.1f}%")
    
    with battery_col2:
        st.write("**Battery Decay Function:**")
        st.latex(r"f(x) = 100 \cdot (0.92)^x")
        st.write("Where x = hours since full charge")
        st.write("**Decay rate:** 8% per hour")
        st.write("**Decay factor:** 0.92 (92% remains each hour)")

    # --- Reflection Section ---
    st.markdown("---")
    st.header("🎓 Reflection with Dr. X")
    
    st.write("**Reflection Questions:**")
    st.write("1. How does exponential decay differ from linear change?")
    st.write("2. What's something in real life that decays exponentially?")
    st.write("3. Why might this be important to understand?")
    
    reflection = st.text_area("Write your thoughts here:", height=100)

    if st.button("Get Dr. X Feedback on Reflection") and reflection:
        with st.spinner("Dr. X is reviewing your reflection..."):
            try:
                if 'OPENAI_API_KEY' in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system", 
                                "content": "You're Dr. X, providing encouraging feedback on student reflections about exponential decay functions. Give constructive, positive feedback that builds understanding."
                            },
                            {
                                "role": "user", 
                                "content": f"Student reflection on exponential decay: {reflection}"
                            }
                        ],
                        max_tokens=250
                    )
                    st.markdown("### 🧠 Dr. X's Feedback:")
                    st.success(response.choices[0].message.content)
                else:
                    st.markdown("### 🧠 Dr. X's Feedback:")
                    st.success("Great thinking! Exponential decay is different from linear change because the rate of decrease gets smaller over time, but the percentage decrease stays constant. This is super important in real life - from understanding how medications work in your body to managing phone battery life!")
            except Exception as e:
                st.error(f"Dr. X feedback error: {str(e)}")

    # --- Quiz Section ---
    st.markdown("---")
    st.header("🧮 Quick Quiz")
    
    quiz_question = st.radio(
        "If f(x) = 50(0.8)^x represents the amount of medicine in your body, what happens every hour?",
        [
            "The amount increases by 20%",
            "The amount decreases by 20%", 
            "The amount stays the same",
            "The amount doubles"
        ]
    )
    
    if st.button("Check Answer"):
        if "decreases by 20%" in quiz_question:
            st.success("🎉 Correct! The decay factor 0.8 means 80% remains, so 20% is lost each hour.")
            st.balloons()
        else:
            st.error("❌ Not quite. Remember: 0.8 means 80% remains, so 20% is lost each hour!")
            
    # Bonus quiz
    st.markdown("**Bonus Question:**")
    bonus_answer = st.number_input("After 3 hours, how much medicine remains? (Start with 50mg)", min_value=0.0, step=0.1)
    
    if st.button("Check Bonus Answer"):
        correct_answer = 50 * (0.8 ** 3)  # 25.6mg
        if abs(bonus_answer - correct_answer) < 0.5:
            st.success(f"🎉 Excellent! The correct answer is {correct_answer:.1f}mg")
            st.balloons()
        else:
            st.error(f"Close, but the correct answer is {correct_answer:.1f}mg. Try: 50 × (0.8)³")

# --- Footer ---
st.markdown("---")
st.markdown(
    "### 🧠 MathCraft Lesson: *Panther.Functions* — developed by Xavier Honablue, M.Ed",
    help="An interactive learning experience for understanding mathematical functions"
)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)
