import streamlit as st

st.set_page_config(page_title="CCSCR Prompt Builder", page_icon="🧩")
st.title("🧩 Prompt Engineer — CCSCR Prompt Builder")
st.caption("Demo Mode - Learn how to structure prompts with CCSCR!")

# --- CCSCR Inputs ---
st.subheader("Enter CCSCR Elements")

context = st.text_area("Context", value="Example: Audience is students preparing for exams")
constraint = st.text_area("Constraint", value="Example: Keep answers under 100 words")
structure = st.text_area("Structure", value="Example: Bullet points followed by a summary")
checkpoint = st.text_area("Checkpoint", value="Example: Ensure at least 3 key facts are included")
review = st.text_area("Review", value="Example: Revise tone to be encouraging and motivating")

# --- Draft Prompt ---
st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140)

# --- Button Action ---
if st.button("Build CCSCR Prompt"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Demo instructional output
        instruction = (
            "Generate an enhanced, structured prompt using CCSCR.\n"
            "1) Integrate all 5 CCSCR elements clearly\n"
            "2) Ensure readability and precision\n"
            "3) Provide a short reviewer’s note\n"
        )
        
        demo_output = (
            f"CONTEXT: {context}\n"
            f"CONSTRAINT: {constraint}\n"
            f"STRUCTURE: {structure}\n"
            f"CHECKPOINT: {checkpoint}\n"
            f"REVIEW: {review}\n\n"
            f"USER DRAFT:\n{draft}\n\n"
            "OUTPUT FORMAT:\n- 3–4 bullet summary\n- 1 reviewer’s note"
        )
        
        st.success("Enhanced Prompt (Demo Mode)")
        st.code(instruction + "\n" + demo_output, language="markdown")
        
        st.info("💡 This is demo mode showing the CCSCR structure. In live mode, AI would generate the actual enhanced prompt!")
