import streamlit as st
import pandas as pd
import tempfile
import os

# Imports the backend flashcard generation function from app.py
from app import generate_flashcards


# Custom CSS used to slightly improve Streamlit's default file uploader layout
st.markdown(
    """
    <style>
    section[data-testid="stFileUploader"] {
        display: flex;
        justify-content: center;
    }

    section[data-testid="stFileUploader"] > div {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Main app title
st.markdown(
    """
    <h1 style='text-align: center;'>
        Flashcard Generator
    </h1>
    """,
    unsafe_allow_html=True
)


# Short user instruction text under the title
st.markdown(
    """
    <p style='text-align: center; font-size:18px;'>
        Upload a .txt or .docx file to generate flashcards.
    </p>
    """,
    unsafe_allow_html=True
)


# Centers the file uploader using Streamlit columns
left, center, right = st.columns([1, 4, 1])

with center:
    uploaded_file = st.file_uploader(
        label="",
        type=["txt", "docx"]
    )


# Runs only after a user uploads a supported file
if uploaded_file is not None:

    # Gets the uploaded file extension, such as .txt or .docx
    file_extension = os.path.splitext(uploaded_file.name)[1]

    # Saves uploaded file temporarily so the backend can process it by file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    # Calls the backend flashcard generation engine
    results = generate_flashcards(temp_file_path)

    if results is not None:
        cards = results["cards"]

        # Displays success message showing how many cards were created
        st.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 24px;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 15px;
                margin-top: 20px;
                margin-bottom: 20px;
            ">
                Generated {len(cards)} flashcards
            </div>
            """,
            unsafe_allow_html=True
        )

        skipped_lines = results["skipped_lines"]

        if skipped_lines:
            with st.expander(f"View Skipped lines ({len(skipped_lines)})"):
                for line in skipped_lines:
                    st.write(line)

        if cards:
            # Converts card list into a DataFrame for table preview and CSV export
            df = pd.DataFrame(cards)
            csv_data = df.to_csv(index=False).encode("utf-8")

            # Optional checkbox to reveal full generated table
            # Hidden by default to avoid showing all answers during study mode
            show_table = st.checkbox("Show generated flashcard table")

            # Adds spacing below checkbox
            st.markdown(
                """
                <div style="margin-bottom: 30px;"></div>
                """,
                unsafe_allow_html=True
            )

            if show_table:
                st.dataframe(df)

            # Stores which flashcard the user is currently viewing
            if "card_index" not in st.session_state:
                st.session_state.card_index = 0

            # Stores whether the answer side of the card is visible
            if "show_answer" not in st.session_state:
                st.session_state.show_answer = False

            # Prevents index errors if a new upload has fewer cards
            if st.session_state.card_index >= len(cards):
                st.session_state.card_index = 0

            # Navigation row: card counter on left, previous/next buttons centered
            nav_left, nav_center_1, nav_center_2, nav_right = st.columns([2.4, 1, 1, 2])

            with nav_left:
                st.markdown(
                    f"""
                    <div style="
                        font-size: 18px;
                        padding-top: 8px;
                    ">
                        Card {st.session_state.card_index + 1} of {len(cards)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Moves to previous card and wraps around to the last card if needed
            with nav_center_1:
                if st.button("Previous"):
                    st.session_state.card_index = (
                        st.session_state.card_index - 1
                    ) % len(cards)
                    st.session_state.show_answer = False
                    st.rerun()

            # Moves to next card and wraps around to the first card if needed
            with nav_center_2:
                if st.button("Next"):
                    st.session_state.card_index = (
                        st.session_state.card_index + 1
                    ) % len(cards)
                    st.session_state.show_answer = False
                    st.rerun()

            # Gets current card based on selected index
            current_card = cards[st.session_state.card_index]

            # Extracts the term from the generated front text
            front_text = current_card["front"]
            start = front_text.find('"') + 1
            end = front_text.rfind('"')
            term = front_text[start:end]

            # Displays the front of the flashcard with the term emphasized
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    font-size: 32px;
                    padding: 30px;
                    border: 2px solid #444;
                    border-radius: 14px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                ">
                    Define the term
                    <span style="
                        color: #4CAF50;
                        font-weight: bold;
                    ">
                        "{term}"
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Centers the answer toggle button
            left, center, right = st.columns([2.5, 2, 2])

            with center:
                if st.button("Show / Hide Answer"):
                    st.session_state.show_answer = not st.session_state.show_answer

            # Displays the back of the flashcard only when toggled on
            if st.session_state.show_answer:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        font-size: 28px;
                        padding: 24px;
                        border: 1px solid #ddd;
                        border-radius: 12px;
                        margin-top: 20px;
                    ">
                        {current_card["back"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Centers the CSV download button
            left, center, right = st.columns([2.1, 2, 2])

            with center:
                st.download_button(
                    label="Download flashcards as CSV",
                    data=csv_data,
                    file_name="flashcards.csv",
                    mime="text/csv"
                )