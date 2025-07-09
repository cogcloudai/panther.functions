import streamlit as st
from openai import OpenAI
import numpy as np
import plotly.graph_objects as go

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
def mark_ask_drx():
    st.session_state.ask_drx = True

def mark_get_drx_reflection():
    st.session_state.get_drx_reflection = True

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

def create_function_plot(func_type, current_x):
    """Create interactive plot for the selected function"""
    x_vals = np.linspace(0, 10, 100)
    
    if func_type.startswith("Linear"):
        y_vals = 2 * x_vals + 1
        title = "Linear Function: f(x) = 2x + 1"
    elif func_type.startswith("Quadratic"):
        y_vals = x_vals ** 2
        title = "Quadratic Function: f(x) = x²"
    elif func_type.startswith("Exponential"):
        y_vals = 3 ** x_vals
        title = "Exponential Function: f(x) = 3^x"
    elif func_type.startswith("Decay"):
        y_vals = 100 * (0.9 ** x_vals)
        title = "Exponential Decay: f(x) = 100(0.9)^x"
    
    fig = go.Figure()
    
    # Add function curve
    fig.add_trace(go.Scatter(
        x=x_vals, 
        y=y_vals,
        mode='lines',
        name='Function',
        line=dict(color='blue', width=3)
    ))
    
    # Add current point
    current_y = calculate_function(func_type, current_x)
    fig.add_trace(go.Scatter(
        x=[current_x], 
        y=[current_y],
        mode='markers',
        name=f'f({current_x}) = {current_y:.2f}',
        marker=dict(color='red', size=12)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Input (x)",
        yaxis_title="Output f(x)",
        showlegend=True,
        height=400
    )
    
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
                    st.warning("OpenAI API key not configured. Dr. X is taking a break!")
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
            st.write(f"Calculation: f({x_val}) = 2({x_val}) + 1 = {fx}")
        elif func_type.startswith("Quadratic"):
            st.write(f"Calculation: f({x_val}) = {x_val}² = {fx}")
        elif func_type.startswith("Exponential"):
            st.write(f"Calculation: f({x_val}) = 3^{x_val} = {fx}")
        elif func_type.startswith("Decay"):
            st.write(f"Calculation: f({x_val}) = 100 × (0.9)^{x_val} = {fx:.2f}")
    
    with col2:
        # Display interactive plot
        fig = create_function_plot(func_type, x_val)
        st.plotly_chart(fig, use_container_width=True)

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
    
    with col2:
        # Show decay table
        st.write("**Decay Table:**")
        decay_data = []
        for i in range(6):
            value = 100 * (0.9 ** i)
            decay_data.append({"Time (x)": i, "Value f(x)": f"{value:.2f}"})
        st.table(decay_data)

    # --- Real World Examples ---
    st.markdown("### 🌍 Real World Examples of Exponential Decay:")
    examples = [
        "📱 **Phone battery** losing charge over time",
        "☢️ **Radioactive materials** breaking down",
        "🏠 **Car value** depreciating each year",
        "🌡️ **Hot coffee** cooling down",
        "💊 **Medicine** leaving your body"
    ]
    
    for example in examples:
        st.write(example)

    # --- Reflection Section ---
    st.markdown("---")
    st.header("🎓 Reflection with Dr. X")
    
    reflection = st.text_area(
        "Reflection Questions:",
        placeholder="1. How does exponential decay differ from linear change?\n2. What's something in real life that decays exponentially?\n3. Why might this be important to understand?",
        height=100
    )

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
                    st.warning("OpenAI API key not configured for feedback.")
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
        else:
            st.error("❌ Not quite. Remember: 0.8 means 80% remains, so 20% is lost!")

# --- Footer ---
st.markdown("---")
st.markdown(
    "### 🧠 MathCraft Lesson: *Panther.Functions* — developed by Xavier Honablue, M.Ed",
    help="An interactive learning experience for understanding mathematical functions"
)
