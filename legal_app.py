import streamlit as st
from utils import find_best_match, load_data
import os

st.set_page_config(page_title="Legal Section Identifier", layout="wide")
st.title("📜 Legal Section Identifier")
st.write("Enter an incident description, and we’ll find the most relevant section from the Bharatiya Nyaya Sanhita (BNS).")

data = load_data("data/bns_sections.json")

user_input = st.text_area("📝 Describe the incident here:")

if st.button("🔍 Find Relevant Section"):
    if user_input.strip():
        result = find_best_match(user_input, data)

        st.success(f"📘 **Matched Section:** {result['section_number']} - {result['title']}")
        st.markdown(f"🔗 [View Full Section Online]({result['url']})", unsafe_allow_html=True)

        st.subheader("📜 Full Legal Description")
        st.markdown(result["description"].replace("\n", "<br>"), unsafe_allow_html=True)

        st.subheader("💡 Summary (Simple Explanation)")
        st.info(result["simple_summary"])
    else:
        st.warning("Please enter an incident description.")
