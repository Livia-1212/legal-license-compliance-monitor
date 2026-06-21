from pathlib import Path

import streamlit as st


def load_css(css_path: str = "assets/styles.css") -> None:
    css_file = Path(css_path)

    if not css_file.exists():
        st.warning(f"CSS file not found: {css_path}")
        return

    st.markdown(
        f"<style>{css_file.read_text()}</style>",
        unsafe_allow_html=True,
    )