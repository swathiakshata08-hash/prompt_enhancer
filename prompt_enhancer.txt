
import streamlit as st
st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — General Prompt Enhancer")
st.caption("Demo Mode - Learn how to structure better prompts!")

st.subheader("Enter Role, Context, Task (RCT)")
role = st.text_input("Role", value="a helpful assistant")
context = st.text_area("Context", value="Audience: busy professional; Goal: clear and specific")
task = st.text_area("Task", value="Rewrite my draft for clarity and ask 1 clarifying question")

st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140)

if st.button("Enhance Prompt"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Demo output - shows structured approach
        instruction = (
            "Generate an enhanced, structured prompt using RCT.\n"
            "1) Improve clarity and completeness\n"
            "2) Ask ONE clarifying question\n"
            "3) Specify output format (3 bullets, ≤12 words each)\n"
        )
        demo_output = (
            f"ROLE: {role}\n"
            f"CONTEXT: {context}\n"
            f"TASK: {task}\n\n"
            f"USER DRAFT:\n{draft}\n\n"
            "OUTPUT FORMAT:\n- 3 concise bullets\n- 1 clarifying question"
        )
        
        st.success("Enhanced Prompt (Demo Mode)")
        st.code(instruction + "\n" + demo_output, language="markdown")
        
        st.info("💡 This is demo mode showing the RCT structure. In live mode, AI would generate the actual enhanced prompt!")
