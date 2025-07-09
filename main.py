import streamlit as st
from openai import OpenAI

# --- Page Config ---
st.set_page_config(page_title="Panther Functions: Exponential Decay", page_icon="📉")

# --- Define State Flags ---
def mark_ask_drx():
    st.session_state.ask_drx = True

def mark_get_drx_reflection():
    st.session_state.get_drx_reflection = True

# --- Title ---
st.title("🐾 Panthers Learn Functions")
st.markdown("Welcome, Englewood STEM Panthers! Enter your name and choose an avatar to begin.")

# --- Student Info ---
name = st.text_input("Enter your name:")
avatar = st.selectbox("Choose your multidimensional shape avatar:", ["🔺 Tetrahedron", "🚘 Dodecahedron", "🪒 Cube", "🌀 Torus"])

if name:
    st.success(f"Welcome, {name}! Let's begin exploring functions.")

    # --- Ask Dr. X (LLM Initial Prompt) ---
    st.markdown("## 🧠 Ask Dr. X: What is your interpretation of a function?")
    st.write("Dr. X wants to hear how YOU understand the concept of a function.")

    # --- Embed External HTML Chat Widget ---
    st.components.v1.html('''
        <!-- Ask Dr. X Widget - Embedded -->
        <div id="ask-drx-widget" style="max-width: 600px; margin: 2rem auto; padding: 1.5rem; background: white; border: 2px solid #ddd; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
          <h3 style="text-align: center; color: #333; margin-bottom: 1rem; font-size: 1.5rem;">
            Ask Dr. X <span style="font-size: 2.2rem;">👓</span>
          </h3>
          <div id="drx-chat-box" style="border: 1px solid #ccc; border-radius: 8px; padding: 1rem; height: 300px; overflow-y: auto; background: #fafafa; margin-bottom: 1rem;">
            <div style="color: #333; font-weight: bold; margin-bottom: 0.5rem;">Dr. X: Hello! I'm your AI tutor. What would you like to learn today?</div>
          </div>
          <div style="display: flex; gap: 0.5rem;">
            <input 
              id="drx-user-input" 
              type="text" 
              placeholder="Ask me anything..." 
              style="flex: 1; padding: 0.75rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem;"
              onkeypress="if(event.key==='Enter') sendToDrX()"
            />
            <button 
              onclick="sendToDrX()" 
              style="padding: 0.75rem 1.5rem; background: #333; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem;"
            >
              Send
            </button>
          </div>
        </div>

        <script>
        async function sendToDrX() {
          const input = document.getElementById('drx-user-input');
          const message = input.value.trim();
          if (!message) return;
          const chatBox = document.getElementById('drx-chat-box');
          chatBox.innerHTML += `<div style="color: #007bff; font-weight: bold; margin-bottom: 0.5rem;">You: ${message}</div>`;
          input.value = "";
          chatBox.innerHTML += `<div id="thinking" style="color: #666; font-style: italic; margin-bottom: 0.5rem;">Dr. X is thinking...</div>`;
          chatBox.scrollTop = chatBox.scrollHeight;
          try {
            const response = await fetch('https://ask-drx-730124987572.us-central1.run.app', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message }),
            });
            const data = await response.json();
            document.getElementById('thinking').remove();
            chatBox.innerHTML += `<div style="color: #333; font-weight: bold; margin-bottom: 0.5rem;">Dr. X: ${data.reply}</div>`;
          } catch (error) {
            document.getElementById('thinking').remove();
            chatBox.innerHTML += `<div style="color: #333; font-weight: bold; margin-bottom: 0.5rem;">Dr. X: Sorry, I'm having trouble connecting right now. Please try again.</div>`;
          }
          chatBox.scrollTop = chatBox.scrollHeight;
        }
        </script>
    ''', height=500)

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
    st.latex(r"f(x) = 100 \\cdot (0.9)^x")

    st.write("- 100 = Starting value")
    st.write("- 0.9 = Decay factor (10% decrease)")
    st.write("- x = Time steps")

    st.write("**What happens as x increases?** Try different values above to observe the shrinking.")

    # --- Reflection Prompt ---
    st.markdown("---")
    st.header("🎓 Reflection with Dr. X")
    reflection = st.text_area(
        "How does decay differ from linear change? What's something in real life that decays?",
        on_change=mark_get_drx_reflection,
        key="reflection_input"
    )

    if st.session_state.get("get_drx_reflection") and reflection:
        with st.spinner("Dr. X is thinking..."):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response2 = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're Dr. X, a mentor for students learning functions."},
                        {"role": "user", "content": reflection}
                    ]
                )
                st.markdown("### 🧠 Dr. X replies:")
                st.write(response2.choices[0].message.content)
            except Exception as e:
                st.error(f"LLM Error: {e}")

# --- Footer Attribution ---
st.markdown("---")
st.markdown("### 🧠 MathCraft Lesson: *Panther.Functions* — developed by Xavier Honablue, M.Ed")
