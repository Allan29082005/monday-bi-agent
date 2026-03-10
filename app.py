import streamlit as st
from monday_api import get_board_data
from data_processing import board_to_dataframe
from agent import ask_agent

DEALS_BOARD_ID = 5027109173
WORK_ORDERS_BOARD_ID = 5027109146


def main():

    st.set_page_config(
        page_title="Monday BI Agent",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Monday.com Business Intelligence Agent")
    st.caption("Ask founder-level questions about your pipeline and operations.")

    # -------- CSS Styling --------
    st.markdown("""
    <style>

    /* Lavender expander header (sidebar question bar) */
    section[data-testid="stSidebar"] details summary {
        background: linear-gradient(135deg,#C4B5FD,#A78BFA);
        border-radius: 10px;
        padding: 8px;
        color: #1F2937;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] details summary:hover {
        background: linear-gradient(135deg,#B4A5F5,#9279F3);
    }

    /* Lime green answer preview */
    .sidebar-answer {
        padding:10px;
        border-radius:10px;
        background:linear-gradient(135deg,#BBF7D0,#86EFAC);
        color:#064E3B;
        font-size:13px;
        margin-top:8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------- Session State --------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "history" not in st.session_state:
        st.session_state.history = []

    # -------- Sidebar --------
    st.sidebar.markdown("### 🕘 Previous Questions")

    for i, item in enumerate(st.session_state.history):

        with st.sidebar.expander(f"💬 {item['question']}", expanded=False):

            st.markdown(
                f"<div class='sidebar-answer'>📊 {item['short_answer']}</div>",
                unsafe_allow_html=True
            )

            if st.button("Open Conversation", key=f"open_{i}"):

                st.session_state.messages = item["conversation"].copy()

    if st.sidebar.button("🗑 Clear History"):
        st.session_state.history = []
        st.session_state.messages = []

    # -------- Chat Display --------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -------- Chat Input --------
    question = st.chat_input("Ask a business question")

    if question:

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Analyzing business data..."):

            deals_data = get_board_data(DEALS_BOARD_ID)
            work_data = get_board_data(WORK_ORDERS_BOARD_ID)

            deals_df = board_to_dataframe(deals_data)
            work_df = board_to_dataframe(work_data)

            answer = ask_agent(question, deals_df, work_df)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)

        # Save history snapshot
        st.session_state.history.append(
            {
                "question": question,
                "short_answer": answer[:120] + "...",
                "conversation": st.session_state.messages.copy()
            }
        )


if __name__ == "__main__":
    main()