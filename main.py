import streamlit as st
import os
from utils.session import init_session_state, clear_session
from utils.components import zen_header, navigation_menu
from views.login import show_login_page
from views.dashboard import show_dashboard
from views.degen_test import show_degen_test
from views.lesson import show_lesson
from views.profile import show_profile
from views.degen_explorer import show_degen_explorer
<<<<<<< HEAD
from views.skills_new import show_skill_tree  # Zaktualizowane na nowy interfejs skills
=======
from views.skills import show_skill_tree  # Dodaj ten import
>>>>>>> a526237cc52a37f7735f8688de6dce465045e2d2
from config.settings import PAGE_CONFIG

# Configure the page and hide page names in sidebar
st.set_page_config(
    **PAGE_CONFIG,
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Załaduj plik CSS
def load_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    return css

# Ścieżka do pliku CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "css", "style.css")
css = load_css(css_path)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state
    init_session_state()
    
    # Sidebar for logged-in users
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown(f"### Witaj, {st.session_state.username}!")
            
            # Nawigacja
            navigation_menu()
            
            # Przycisk wylogowania na dole sidebara
            if st.button("Wyloguj się", key="logout_button"):
                clear_session()
                st.rerun()
    
    # Page routing
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.page == 'dashboard':
            show_dashboard()
        elif st.session_state.page == 'degen_test':
            show_degen_test()
        elif st.session_state.page == 'lesson':
            show_lesson()
        elif st.session_state.page == 'profile':
            show_profile()
        elif st.session_state.page == 'degen_explorer':
            show_degen_explorer()
        elif st.session_state.page == 'skills':  # Dodaj tę sekcję
            show_skill_tree()

st.markdown("<style>div.stButton > button { margin-bottom: 1px; }</style>", unsafe_allow_html=True)
if __name__ == "__main__":
    main()