from streamlit.testing.v1 import AppTest


def test_app():
    at = AppTest.from_file("src/app.py").run()
    assert not at.exception
