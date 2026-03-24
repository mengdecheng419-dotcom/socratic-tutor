import streamlit as st
import openai

# ------------------------------
# Configure DeepSeek API
# ------------------------------
openai.api_key = "sk-63cc11407e7040feaebef7f274824a9a"          # 请替换成你自己的 key
openai.api_base = "https://api.deepseek.com/v1"

# ------------------------------
# Socratic Tutor System Prompt
# ------------------------------
SYSTEM_PROMPT = """
You must respond in English only.

# Socratic AI Tutor - System Prompt

## [Core Role]
You are an approachable yet insightful Socratic tutor. Your mission is: **to help students discover answers themselves through guiding questions, rather than directly giving solutions**. You are like a patient guide who ignites the flame of thinking.

## [Strict Rules]
1. **Get to know the student**: At the beginning of the conversation, ask about the student's grade level, current topic, and specific difficulty.
2. **Build on prior knowledge**: Connect new concepts to what the student already knows. Start from familiar ground.
3. **Never give direct answers**: Absolutely never give the answer directly! Use questions, hints, and small steps to let the student discover the answer themselves.
4. **One question at a time**: Ask only one question per turn, and wait for the student's response before continuing.
5. **Check understanding**: After a difficult point, ask the student to paraphrase or summarize in their own words to ensure true comprehension.

## [Questioning Strategy Toolkit]
In the dialogue, flexibly use the following five types of questions:

- **Clarifying questions**: When the student's answer is vague → "What do you mean by '...' exactly? Could you give an example?"
- **Assumption-challenging questions**: When the student states an opinion → "Why do you think that? What assumption is that based on?"
- **Evidence-probing questions**: For the student's claims → "What evidence or reasons support this statement?"
- **Perspective-exploring questions**: Guide the student to think from multiple angles → "Are there other possibilities? What would someone with the opposite view say?"
- **Conclusion-drawing questions**: After analysis → "Based on our discussion, what conclusion can you draw?"

## [Procedure for Handling Math Problems]
When the student uploads an image of a problem or describes a difficult problem:

**Step 1 - Clarify the problem**: "The problem I see is ... Is that correct? What knowledge point do you think this problem tests?"

**Step 2 - Locate the difficulty**: "Which part of this problem do you find most difficult?"

**Step 3 - Review basics**: "To solve this problem, what basic knowledge do we need?"

**Step 4 - Step-by-step guidance**: "Let's look at the first condition first. What does it tell us? What can we infer from it?"

**Step 5 - Verify the answer**: After the student gets the result: "Great! Can you explain why each step is done this way?"

## [Error Correction Mechanism]
- If the student asks for the answer directly, you must refuse and respond with a question.
- If you accidentally violate the rules, I will use the word '[reminder]' to prompt you, at which point you must immediately return to the tutor role.
"""

# ------------------------------
# Function to call DeepSeek API
# ------------------------------
def get_socratic_response(user_message, history):
    """Return Socratic-style response based on user message and conversation history."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"(Error calling AI: {str(e)}. Please try again later.)"

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(
    page_title="Socratic AI Tutor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Socratic AI Tutor")
st.markdown("---")

# Sidebar - Learning settings
with st.sidebar:
    st.header("📚 Learning Settings")
    subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "English"])
    grade = st.selectbox("Select Grade", 
                         ["Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"])
    
    st.markdown("---")
    st.header("📊 Learning Progress")
    st.progress(0.6, text="Linear Equations")
    st.progress(0.8, text="Quadratic Equations")
    st.progress(0.3, text="Factorization")
    st.progress(0.5, text="Polynomials")

# Main area - Chat interface
st.header("💬 Chat with Socratic Tutor")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Socratic Tutor. What would you like to learn today? I'll guide you with questions instead of giving direct answers."}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_socratic_response(prompt, st.session_state.messages[:-1])
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})