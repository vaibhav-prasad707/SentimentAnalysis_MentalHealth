# app.py
import streamlit as st
from main import init_components, SimpleAgentPlanner, get_emotion_response
import warnings
warnings.filterwarnings("ignore")

def main():
    st.title("TherAIpist - Your AI Mental Health Companion")

    # Disclaimer
    st.warning("""
    ⚠️ **IMPORTANT DISCLAIMER**: 
    This is a demo system for educational purposes only. 
    It is NOT a replacement for professional mental health care.
    If you're in crisis, please contact a mental health professional or crisis hotline immediately.
    """)

    # Initialize components
    emotion_analyzer, collection = init_components()
    planner = SimpleAgentPlanner()

    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # User input
    user_input = st.text_area("How are you feeling today?", height=100)

    if st.button("Get Support") and user_input:
        with st.spinner("Analyzing your message..."):
            # Step 1: Emotion Analysis
            emotions = emotion_analyzer(user_input)
            top_emotion = emotions[0]
            emotion_name = top_emotion['label'].lower()
            emotion_score = top_emotion['score']

            st.write(f"**Detected Emotion**: {emotion_name.title()} (confidence: {emotion_score:.2f})")

            # Step 2: Agent Planning
            plan = planner.plan(emotion_name, emotion_score, user_input)

            if plan["priority"] == "CRISIS":
                st.error("🚨 **Crisis Detected**")
                st.error(plan["message"])
                st.info("""
                **Crisis Resources:**
                - National Suicide Prevention Lifeline: 988
                - Crisis Text Line: Text HOME to 741741
                - Emergency Services: 911
                """)
                return

            # Step 3: Generate Response
            response = get_emotion_response(emotion_name, emotion_score)

            # Step 4: Display Results
            st.success("**AI Response:**")
            st.write(response)

            with st.expander("🔍 System Reasoning (Demo)"):
                st.json({
                    "emotion_detected": emotion_name,
                    "confidence": float(emotion_score),
                    "plan_priority": plan["priority"],
                    "response_strategy": f"Provide {emotion_name} support"
                })

            # Store conversation
            st.session_state.conversation_history.append({
                "user": user_input,
                "emotion": emotion_name,
                "response": response
            })

    # History
    if st.session_state.conversation_history:
        st.subheader("💬 Conversation History")
        for i, conv in enumerate(st.session_state.conversation_history):
            with st.expander(f"Exchange {i+1} - {conv['emotion'].title()}"):
                st.write(f"**You:** {conv['user']}")
                st.write(f"**AI:** {conv['response']}")

if __name__ == "__main__":
    main()
