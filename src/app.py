import streamlit as st

from src.interface.state import initialize_app_state


def main():
    # 共通のページ設定
    st.set_page_config(
        page_title="Survey Data Cleaning App",
        page_icon="📊",
    )

    # アプリケーションの状態を初期化
    initialize_app_state()

    home_page = st.Page(
        "contents/01_home.py", title="Home", icon=":material/home:", default=True
    )
    cleaning_page = st.Page("contents/02_cleaning.py", title="Data Cleaning", icon="🧹")
    manipulation_page = st.Page(
        "contents/03_manipulation.py", title="Data Manipulation", icon="🔧"
    )
    visualization_page = st.Page(
        "contents/04_visualization.py", title="Data Visualization", icon="📊"
    )

    pg = st.navigation([home_page, cleaning_page, manipulation_page, visualization_page])
    st.session_state.current_page = pg.title
    pg.run()


if __name__ == "__main__":
    main()
