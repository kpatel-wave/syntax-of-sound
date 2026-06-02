import streamlit as st
from labeler import analyze

# User-facing names for labels
LABEL_DISPLAY = {
    "slow-exposed-strings": "Slow, exposed string writing",
    "exposed-brass-solo": "Exposed brass solo",
    "high-tempo": "High tempo / edge-of-control",
    "rhythmic-ostinato-backdrop": "Ostinato / motor rhythm",
    "structural-boundary": "Structural boundary / sudden change",
    "sustained-dissonance": "Sustained dissonance / tension",
    "chorale-brass-entry": "Chorale-style brass entry",
    "unclassified-pattern": "No specific risk pattern detected",
}


st.set_page_config(
    page_title="Syntax of Sound",
    page_icon="🎼",
    layout="centered",
)

st.title("Syntax of Sound")
st.write(
    "Describe a specific moment in a piece (or paste a program-note style description). "
    "This tool analyzes your text and highlights likely performance risks and practice ideas."
)

st.markdown("---")

# Text input
user_text = st.text_area(
    "Describe the musical moment:",
    height=200,
    placeholder=(
        "Example: In Holst’s The Planets, the trumpets and horns have a loud, exposed solo at ♩ = 132 bpm "
        "over the full orchestra driving underneath..."
    ),
)

if st.button("Analyze"):
    if not user_text.strip():
        st.warning("Please enter a description of a musical moment first.")
    else:
        # Run the analysis
        result = analyze(user_text)

        parsed = result.get("parsed", {})
        labels = result.get("labels", [])
        summary = result.get("summary", "")
        tips = result.get("tips", [])

        st.markdown("### Parsed details")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Composer:** {parsed.get('composer', 'Unknown')}")
            tempo = parsed.get("tempo")
            if tempo is not None:
                st.write(f"**Tempo:** {tempo} bpm")
            else:
                st.write("**Tempo:** Not detected")

        with col2:
            instruments = parsed.get("instruments", [])
            if instruments:
                st.write("**Instruments detected:**")
                st.write(", ".join(instruments))
            else:
                st.write("**Instruments detected:** None")

        st.markdown("### Risk factors")
        if labels:
            for label in labels:
                pretty = LABEL_DISPLAY.get(label, label)
                st.markdown(f"- {pretty}")
        else:
            st.write("No specific patterns detected by the current rules.")

        st.markdown("### What this passage is like")
        if summary:
            st.write(summary)
        else:
            st.write("No summary available.")

        st.markdown("### Practice / rehearsal tips")
        if tips:
            for tip in tips:
                st.markdown(f"- {tip}")
        else:
            st.write("No specific practice tips available yet.")
else:
    st.info("Enter a description above and click **Analyze** to get started.")
