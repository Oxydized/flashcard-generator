import streamlit as st
import pandas as pd
import tempfile
import os

from app import generate_flashcards


st.title("Flashcard Generator")

st.write("Upload a .txt or .docx file to generate flashcards.")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["txt", "docx"]
)

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    results = generate_flashcards(temp_file_path)

    if results is not None:
        cards = results["cards"]

        st.success(f"Generated {len(cards)} flashcards.")

        if cards:
            df = pd.DataFrame(cards)
            st.dataframe(df)

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download flashcards as CSV",
                data=csv_data,
                file_name="flashcards.csv",
                mime="text/csv"
            )