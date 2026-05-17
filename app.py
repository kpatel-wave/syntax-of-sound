import streamlit as st
from labeler import analyze

st.set_page_config(page_title="Syntax of Sound", page_icon="🎼", layout="centered")

st.title("Syntax of Sound")
st.write(
    "A tiny rule-based tagger for structural features in short orchestral music descriptions."
)

default_text = "Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%"

description = st.text_area(
    "Describe a musical moment:",
    value=default_text,
    height=120,
    help="Include composer, movement, tempo, instruments, and anything about risk, dissonance, or texture.",
)

if st.button("Analyze"):
    if not description.strip():
        st.warning("Please enter a description first.")
    else:
        result = analyze(description)

        st.subheader("Parsed fields")
        parsed = result["parsed"]
        st.json(parsed)

        st.subheader("Labels")
        labels = result["labels"]
        if labels:
            for tag in labels:
                st.markdown(f"- `{tag}`")
        else:
            st.write("No labels assigned for this description yet.")
else:
    st.caption("Press **Analyze** to see how this moment is tagged.")
