import streamlit as st


def main():
    # 共通のページ設定
    st.set_page_config(
        page_title="Survey Data Cleaning App",
        page_icon="📊",
    )

    home_page = st.Page(
        "contents/01_home.py", title="Home", icon=":material/home:", default=True
    )
    cleaning_page = st.Page("contents/02_cleaning.py", title="Data Cleaning", icon="🧹")
    manipulation_page = st.Page(
        "contents/03_manipulation.py", title="Data Manipulation", icon="🔧"
    )

    pg = st.navigation([home_page, cleaning_page, manipulation_page])
    pg.run()


if __name__ == "__main__":
    main()
